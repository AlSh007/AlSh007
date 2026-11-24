#!/usr/bin/env python3
"""Build the profile's SVG assets (terminal card + open-source impact card).

Stdlib only. Needs GITHUB_TOKEN (or GH_TOKEN) for the GitHub APIs.
Run from the repo root: python3 scripts/build_assets.py
"""
import json, os, urllib.parse, urllib.request
from xml.sax.saxutils import escape
from collections import Counter

USER = "AlSh007"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

# Contributions the search API can't see (co-authored or adopted into others' PRs).
EXTRA = {"BerriAI/litellm": (1, "co-author"), "JuliusBrussee/caveman": (5, "adopted")}
LABELS = {"vllm-project/aibrix": "AIBrix", "vllm-project/semantic-router": "vLLM semantic-router",
          "theopenco/llmgateway": "llmgateway", "tabloy/keygate": "keygate", "llm-d/llm-d": "llm-d",
          "theagentrouter/agent-router": "agent-router", "BerriAI/litellm": "LiteLLM",
          "JuliusBrussee/caveman": "caveman"}

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", text="#e6edf3", muted="#8b949e",
                 grid="#21262d", a1="#36bcf7", a2="#a371f7", a3="#3fb950", track="#21262d"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#59636e",
                  grid="#eaeef2", a1="#0969da", a2="#8250df", a3="#1a7f37", track="#eaeef2"),
}
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def api(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {TOKEN}",
                                          "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def fetch():
    q = urllib.parse.quote(f"is:pr is:merged author:{USER} -user:{USER}")
    items, page = [], 1
    while True:
        res = api(f"https://api.github.com/search/issues?q={q}&per_page=100&page={page}")
        items += res["items"]
        if len(items) >= res["total_count"] or not res["items"]:
            break
        page += 1
    latest = max(items, key=lambda i: i["closed_at"])
    per_repo = Counter(i["repository_url"].split("/repos/")[1] for i in items)
    gql = api("https://api.github.com/graphql", {"query": f'''{{user(login:"{USER}"){{
      contributionsCollection{{contributionCalendar{{totalContributions}} totalCommitContributions}}}}}}'''})
    cc = gql["data"]["user"]["contributionsCollection"]
    return dict(merged=len(items), per_repo=per_repo,
                latest=dict(repo=latest["repository_url"].split("/repos/")[1], number=latest["number"], title=latest["title"]),
                contributions=cc["contributionCalendar"]["totalContributions"],
                commits=cc["totalCommitContributions"])


def impact(t, d):
    rows = [(LABELS.get(r, r), n, "merged") for r, n in d["per_repo"].most_common()]
    rows += [(LABELS[r], n, note) for r, (n, note) in EXTRA.items()]
    rows.sort(key=lambda r: -r[1])
    projects = len(d["per_repo"]) + len(EXTRA)
    tiles = [(str(d["merged"]), "merged upstream PRs", t["a1"]), (str(projects), "projects", t["a2"]),
             (str(d["commits"]), "commits, last 12 mo", t["a3"]), (str(d["contributions"]), "contributions, last 12 mo", t["a1"])]
    W, top = 900, 196
    H = top + 34 * len(rows) + 28
    out = []
    for i, (num, label, col) in enumerate(tiles):
        x = 32 + i * 212
        out.append(f'<g class="fade" style="animation-delay:{i*0.12:.2f}s"><rect x="{x}" y="72" width="198" height="96" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>'
                   f'<text x="{x+18}" y="122" style="font:800 36px {SANS};fill:{col}">{num}</text>'
                   f'<text x="{x+18}" y="150" style="font:500 13px {SANS};fill:{t["muted"]}">{label}</text></g>')
    mx = max(r[1] for r in rows)
    cols = [t["a1"], t["a2"], t["a3"]]
    for i, (name, n, note) in enumerate(rows):
        y = top + 34 * i
        w = 430 * n / mx
        out.append(f'<text x="32" y="{y+17}" style="font:600 14px {SANS};fill:{t["text"]}">{name}</text>'
                   f'<rect x="250" y="{y+4}" width="430" height="16" rx="8" fill="{t["track"]}"/>'
                   f'<rect x="250" y="{y+4}" width="{w:.1f}" height="16" rx="8" fill="{cols[i % 3]}" class="bar" style="animation-delay:{0.3+i*0.08:.2f}s"/>'
                   f'<text x="696" y="{y+17}" style="font:600 14px {MONO};fill:{t["text"]}">{n}</text>'
                   f'<text x="724" y="{y+17}" style="font:400 13px {SANS};fill:{t["muted"]}">{note}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Open source impact: {d['merged']} merged upstream PRs across {projects} projects">
<style>
 .fade{{opacity:0;animation:in .6s ease-out forwards}} @keyframes in{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
 .bar{{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:grow 1s cubic-bezier(.2,.8,.2,1) forwards}}
 @keyframes grow{{to{{transform:scaleX(1)}}}}
</style>
<rect width="{W}" height="{H}" rx="16" fill="{t['bg']}"/><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{t['border']}"/>
<text x="32" y="44" style="font:800 20px {SANS};fill:{t['text']}">Open source impact</text>
<text x="{W-32}" y="44" style="font:400 13px {MONO};fill:{t['muted']};text-anchor:end">bug fixes with tests · refreshed weekly</text>
{''.join(out)}
</svg>'''


def terminal(t, d):
    """A terminal window that types out a short session. Plays once, then the cursor blinks."""
    lt = d["latest"]
    title = lt["title"] if len(lt["title"]) <= 70 else lt["title"][:67] + "..."
    projects = len(d["per_repo"]) + len(EXTRA)
    lines = [  # (kind, text) - cmd lines are typed, out lines fade in
        ("cmd", "whoami"),
        ("out", "alok sharma · forward deployed engineer @ future path · india"),
        ("cmd", "cat focus.txt"),
        ("out", "llm routing · inference infra · rag · agents · evals & guardrails"),
        ("cmd", f"gh search prs --author={USER} --merged -- -user:{USER} | wc -l"),
        ("hi",  f"{d['merged']}   merged upstream fixes across {projects} projects"),
        ("cmd", "gh search prs --author=@me --merged --sort=updated --limit=1"),
        ("out", f"{lt['repo']}#{lt['number']}  {title}"),
        ("cmd", "echo $STATUS"),
        ("ok",  "open to opportunities ✓"),
    ]
    W, lh, top = 900, 27, 76
    H = top + lh * (len(lines) + 1) + 20
    body, clips, at = [], [], 0.4
    for i, (kind, text) in enumerate(lines):
        y = top + lh * i
        if kind == "cmd":
            dur = max(0.5, 0.045 * len(text))
            clips.append(f'<clipPath id="c{i}"><rect x="58" y="{y-18}" height="26" width="0">'
                         f'<animate attributeName="width" from="0" to="{9.1*len(text)+4:.0f}" begin="{at:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>')
            body.append(f'<text x="32" y="{y}" class="p">$</text>'
                        f'<text x="58" y="{y}" class="cmd" clip-path="url(#c{i})">{escape(text)}</text>')
            at += dur + 0.25
        else:
            cls = {"out": "out", "hi": "hi", "ok": "ok"}[kind]
            body.append(f'<text x="58" y="{y}" class="{cls} show" style="animation-delay:{at:.2f}s">{escape(text)}</text>')
            at += 0.35
    y = top + lh * len(lines)
    body.append(f'<g class="show" style="animation-delay:{at:.2f}s"><text x="32" y="{y}" class="p">$</text>'
                f'<rect x="58" y="{y-15}" width="10" height="19" fill="{t["a1"]}" class="blink"/></g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Terminal: Alok Sharma, {d['merged']} merged upstream PRs, open to opportunities">
<defs>{''.join(clips)}</defs>
<style>
 text{{font:15px {MONO};white-space:pre}}
 .p{{fill:{t['a3']};font-weight:700}} .cmd{{fill:{t['text']}}} .out{{fill:{t['muted']}}}
 .hi{{fill:{t['a1']};font-weight:700}} .ok{{fill:{t['a3']};font-weight:700}}
 .show{{opacity:0;animation:show .01s linear forwards}} @keyframes show{{to{{opacity:1}}}}
 .blink{{animation:blink 1.1s steps(1) infinite}} @keyframes blink{{50%{{opacity:0}}}}
</style>
<rect width="{W}" height="{H}" rx="14" fill="{t['bg']}"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{t['border']}"/>
<path d="M14 .5h{W-28}a13.5 13.5 0 0 1 13.5 13.5v26H.5V14A13.5 13.5 0 0 1 14 .5z" fill="{t['panel']}"/>
<line x1="0" y1="40.5" x2="{W}" y2="40.5" stroke="{t['border']}"/>
<circle cx="24" cy="20" r="6.5" fill="#ff5f57"/><circle cx="46" cy="20" r="6.5" fill="#febc2e"/><circle cx="68" cy="20" r="6.5" fill="#28c840"/>
<text x="{W/2}" y="25" text-anchor="middle" style="font:500 13px {MONO};fill:{t['muted']}">alok@futurepath: ~</text>
{''.join(body)}
</svg>'''


def main():
    os.makedirs(OUT, exist_ok=True)
    data = fetch()
    for name, t in THEMES.items():
        open(os.path.join(OUT, f"terminal-{name}.svg"), "w").write(terminal(t, data))
        open(os.path.join(OUT, f"impact-{name}.svg"), "w").write(impact(t, data))
    print(json.dumps({k: v for k, v in data.items() if k not in ("per_repo",)}), dict(data["per_repo"]))


if __name__ == "__main__":
    main()
