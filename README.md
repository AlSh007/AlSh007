<h1 align="center">Hi 👋, I'm Alok Sharma</h1>
<h3 align="center">Forward Deployed Engineer · Taking AI from messy workflows to production · India 🇮🇳</h3>

<p align="center">
  <a href="https://alsh007.github.io" target="_blank"><img src="https://img.shields.io/badge/Portfolio-0e75b6?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Portfolio"/></a>
  <a href="https://www.linkedin.com/in/alok-sharma-talks-ai" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
  <a href="https://leetcode.com/alshphoenix" target="_blank"><img src="https://img.shields.io/badge/LeetCode-FFA116?style=for-the-badge&logo=leetcode&logoColor=black" alt="LeetCode"/></a>
  <a href="mailto:sharmaalok705@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
</p>

### 🚀 About Me

- 🔭 Forward Deployed Engineer at **Future Path**: I embed with customer teams, find where AI actually fits, and ship it with evals and guardrails
- 🌱 Contributing to open-source **LLM routing and inference infrastructure**: [semantic-router](https://github.com/vllm-project/semantic-router), [AIBrix](https://github.com/vllm-project/aibrix), [llm-d](https://github.com/llm-d/llm-d), [llmgateway](https://github.com/theopenco/llmgateway), [agent-router](https://github.com/theagentrouter/agent-router), [LiteLLM](https://github.com/BerriAI/litellm), [caveman](https://github.com/JuliusBrussee/caveman)
- 💬 Ask me about **RAG, agents, LLM evaluation and guardrails, and LLM gateways**
- 👯 Happy to collaborate on open-source LLM infrastructure
- ⚡ Fun fact: I turn coffee and prompts into production code
- 📫 Reach me at **sharmaalok705@gmail.com**

### 🤝 Open source contributions

A selection of my merged pull requests in other projects (bug fixes with tests), including one I co-authored in LiteLLM. The caveman row is three fixes the maintainer adopted into a batch PR, with my authorship kept on each commit:

| Project | PR | What it fixed |
|---|---|---|
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | [#46617](https://github.com/BerriAI/litellm/pull/46617) (co-author) | Cache the public provider and agent field endpoints, so the bundled JSON is read and parsed once per process instead of on every request |
| [vllm-project/semantic-router](https://github.com/vllm-project/semantic-router) | [#5167](https://github.com/vllm-project/semantic-router/pull/5167) | Reject a zero or negative `max_tokens_limit` or `max_n` in the request params config, so a bad limit no longer rewrites every client's `max_tokens` or `n` to zero and gets each request rejected upstream |
| [vllm-project/semantic-router](https://github.com/vllm-project/semantic-router) | [#5152](https://github.com/vllm-project/semantic-router/pull/5152) | Reject a Set answer that omits a declared label's probability, so a missing label is no longer read as zero routing evidence |
| [vllm-project/semantic-router](https://github.com/vllm-project/semantic-router) | [#4858](https://github.com/vllm-project/semantic-router/pull/4858) | Stop mirroring a request the router rejected (for example on an unresolved credential) to the shadow model |
| [vllm-project/semantic-router](https://github.com/vllm-project/semantic-router) | [#4712](https://github.com/vllm-project/semantic-router/pull/4712) | Stop tool-observability debug headers from replacing a dispatch failure with a request continue, which let a rejected request go upstream |
| [vllm-project/aibrix](https://github.com/vllm-project/aibrix) | [#3116](https://github.com/vllm-project/aibrix/pull/3116) | Count a panicking `SlowStartBatch` callback as a failure, so RoleSet pod create and delete batches stop hiding panics as successes |
| [vllm-project/aibrix](https://github.com/vllm-project/aibrix) | [#2975](https://github.com/vllm-project/aibrix/pull/2975) | Report a missing latency in the pending-load estimate, so routers stop treating a pod with an incomplete profile as free |
| [vllm-project/aibrix](https://github.com/vllm-project/aibrix) | [#2846](https://github.com/vllm-project/aibrix/pull/2846) | Enforce the prefix-hash table's `maxContexts` cap and evict expired pods ([write-up: what the review taught me about activating dead code](writeups/aibrix-prefix-cache-eviction.md)) |
| [llm-d/llm-d](https://github.com/llm-d/llm-d) | [#2410](https://github.com/llm-d/llm-d/pull/2410) | Align the modelexpress-p2p guide's `PROVIDER_NAME` default with optimized-baseline, so a default install no longer applies GKE-only router resources on a non-GKE cluster |
| [theopenco/llmgateway](https://github.com/theopenco/llmgateway) | [#4672](https://github.com/theopenco/llmgateway/pull/4672) | Keep Anthropic `output_config.effort` when a `json_schema` response_format is used, so the effort setting is no longer dropped from the request body |
| [theopenco/llmgateway](https://github.com/theopenco/llmgateway) | [#3960](https://github.com/theopenco/llmgateway/pull/3960) | Clamp auto reasoning effort in the gateway |
| [theagentrouter/agent-router](https://github.com/theagentrouter/agent-router) | [#2749](https://github.com/theagentrouter/agent-router/pull/2749) | Accept `reasoning_effort: high` for Gemini 3 Pro models, and map `medium` to the right thinking level per model |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | [`e186906`](https://github.com/JuliusBrussee/caveman/commit/e186906a0c41d03a638fa4cb11b105359d4d8ed9), [`37f4b6d`](https://github.com/JuliusBrussee/caveman/commit/37f4b6d723d1d951fde472887a9b04ca84789e83), [`4f7e811`](https://github.com/JuliusBrussee/caveman/commit/4f7e8117332b557eb28c6808387dcb0432c51b7a) (adopted in [#1315](https://github.com/JuliusBrussee/caveman/pull/1315)) | Stop `uninstall` deleting a `settings.json.bak` it did not create, read the schema of Anthropic `input_schema` tools in `shrink`, and keep integers above 2^53 off the numeric range track so elision markers stay correct |

**Deeper dive:** [Fixing code that was never called: wiring up eviction in AIBrix's prefix-cache index](writeups/aibrix-prefix-cache-eviction.md)

[See all merged pull requests →](https://github.com/pulls?q=is%3Apr+is%3Amerged+author%3AAlSh007+-user%3AAlSh007)

### 🛠️ Tech Stack

**Languages**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=postgresql&logoColor=white)

**AI / LLMs**

![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)

**Backend & Web**

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)

**Data & Infrastructure**

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![Kafka](https://img.shields.io/badge/Kafka-231F20?style=flat-square&logo=apachekafka&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)

### 📊 GitHub Stats

<p align="center">
  <img height="170" src="https://github-readme-stats.vercel.app/api?username=alsh007&show_icons=true&locale=en&theme=tokyonight&hide_border=true" alt="Alok's GitHub stats" />
  <img height="170" src="https://github-readme-stats.vercel.app/api/top-langs?username=alsh007&show_icons=true&locale=en&layout=compact&theme=tokyonight&hide_border=true" alt="Top Languages" />
</p>

<p align="center">
  <img src="https://streak-stats.demolab.com/?user=alsh007&theme=tokyonight&hide_border=true" alt="GitHub Streak" />
</p>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=alsh007&label=Profile%20views&color=0e75b6&style=flat" alt="Profile views" />
</p>
