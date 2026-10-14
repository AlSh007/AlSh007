# Fixing code that was never called: wiring up eviction in AIBrix's prefix-cache index

*A merged contribution to [vllm-project/aibrix](https://github.com/vllm-project/aibrix) ([#2846](https://github.com/vllm-project/aibrix/pull/2846)), and what the review taught me about turning on code that has never run.*

## The system

AIBrix routes LLM requests across inference pods. One of its routing strategies is prefix-cache aware: it keeps an index of which pod holds which prompt prefix in its KV cache, so a request can go to the pod most likely to already have the work done. That index lives in `SyncPrefixHashTable`. It is keyed by `(model, LoRA)` context, and each context has a map from prefix hash to the pods that hold it.

An index like this grows, so it needs eviction. This one had it. On paper.

## The bug: two safety mechanisms with no callers

While reading the indexer I noticed two functions that were fully written and never called:

- `enforceContextLimit` was meant to trim the oldest contexts when the count exceeds `AIBRIX_SYNC_MAX_CONTEXTS`.
- `evictExpiredPodsInBatch` was meant to drop a pod's entry once its `LastAccessTime` goes stale.

`performEviction` had three phases. Phases 1 and 2 removed contexts idle past `evictionDuration`. Phase 3 ranged over the surviving contexts and did nothing: it returned `true` for every entry. The `maxContexts` check in `getOrCreateContextData` only set a flag asking for another eviction pass, and that pass never compared the count to the cap.

Two consequences:

1. **Unbounded growth.** A workload with many distinct `(model, lora)` contexts that are all in active use never trips the idle check, so `contextMap` grows past the configured cap without limit.
2. **Stale credit.** A pod that stopped serving a prefix stayed in that context's `prefixMap` as long as some other pod kept the context alive. Prefix hits kept being credited to a pod that no longer had the prefix.

I wrote two tests that fail on `main` (one per symptom), wired both functions into `performEviction`, and had a first version up. The fix was about 40 lines of logic.

## The review: activating dead code changes behavior

The interesting part started after that. A maintainer reviewed the PR and pointed out something I had not weighed enough: these functions had never executed in production. Calling them for the first time did not just add a feature, it activated behavior nobody had validated. They found three problems.

**1. Phase 3 could drop pods that still held the block.**
Phase 3 expires pods by `PodInfo.LastAccessTime`. That timestamp was only written when a prefix was added or re-stored. Nothing refreshed it while the pod kept the block cached, and a match did not touch it either. So a pod could report `BlockStored`, keep the block warm, and after 20 minutes be deleted from the index anyway. Before my PR Phase 3 was a no-op, so long-lived cached prefixes stayed routable. After it, a heavily used prefix would expire just as fast as an unused one. That is a regression I would have introduced.

**2. The cap evicted the wrong contexts.**
`enforceContextLimit` ranks by `prefixStore.lastAccess`, which KV events never updated. A context fed constantly by events, but rarely through `AddPrefix`, looked as old as its creation time and was evicted first, taking its event-derived mappings with it.

**3. Cap eviction left debris.**
It deleted from `contextMap` without setting `markedForEviction` (Phase 2 did) and without cleaning that context's `blockIndex` entries. Under model churn (evict, recreate, evict) `blockIndex` could grow without bound. The slice sizing also came from a counter that is updated separately from the map, so it could briefly disagree with it, and a negative value would panic in `make`.

## What I changed

- `MatchPrefix` now refreshes the matched pod's own `LastAccessTime`. A hit is real use of that cached block, and nothing else records it.
- `ProcessBlockStored` and `ProcessBlockRemoved` refresh the context's `lastAccess`, so contexts fed only by KV events stop looking idle.
- A shared `dropContextBlockIndex` helper runs from both Phase 2 and `enforceContextLimit`, and cap eviction now marks the context first, matching Phase 2.
- The `ages` slice is a plain `append`-grown slice, so it cannot panic and costs no more than the pre-sized version did (every active context is appended regardless of `excess`).

Each fix got its own test that fails on the previous commit: `TestMatchPrefixRefreshesPodLastAccessTime`, `TestProcessBlockStoredRefreshesContextLastAccess`, `TestProcessBlockRemovedRefreshesContextLastAccess` and `TestEnforceContextLimitDropsBlockIndex`. The package passes under `-race`, run five times.

## What I deliberately left out

The reviewer also noted a deeper race: a goroutine that already loaded a `*ContextData` can keep writing to it after it is deleted from the map. I did not fix that here. Phase 1 and 2's idle eviction already had the same shape, and my change alters how often eviction runs, not whether the race exists. Closing it needs a liveness check before every context write, which is a larger change with its own risk. I said so in the thread, scoped it out, and offered to file it as a follow-up. I think knowing where a PR's boundary is matters as much as the fixes inside it.

Same reasoning for orphaned `hashMapping` entries when a pod disappears with no `BlockRemoved`: that gap exists in the current code and is not something Phase 3 introduces.

## Takeaways

- **Dead code is not safe code.** Zero callers means zero validation. Wiring it in is a behavior change, so I now ask, for each function I activate, "what state does it assume, and who writes that state?" The answer to that question was a missing timestamp refresh, and it was the bug.
- **Ranking and expiry depend on a field being kept current.** Both `lastAccess` and `LastAccessTime` were maintained on some paths and not others. Tracing every writer of a field before relying on it would have caught all three review comments.
- **Write the failing test first, then one test per review comment.** It made the review round fast and left a record of exactly what each change protects.
- **Say what you did not fix, and why.** Scoping out a larger race, in writing, was better than quietly widening the PR.

## Disclosure

I used Claude to help find the dead code paths and draft the first version. I reviewed the code, ran the tests, including with the race detector, and wrote the review responses and follow-up fixes myself. The PR description says this up front.

Merged 2026-09-29. Files touched: `sync_hash.go` and `sync_hash_test.go` in `pkg/utils/syncprefixcacheindexer/`.
