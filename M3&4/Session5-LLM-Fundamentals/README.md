# Session 5 — LLM Fundamentals for Builders
## LangChain · Google Gemini (free tier) · from-scratch ReAct

This is the session where you stop *using* AI and start *building* with it.
By the end you'll understand what an LLM really is (a very confident
autocomplete), how to get reliable output from it, how it fails, what it costs,
and how to wrap it in a **thinking loop** — the seed of every agent you'll build
in Sessions 6-14.

**Work through the files in order.** Each one teaches a single idea, runs on its
own, and ends with a short **"Your Challenge"** — do it before moving on. This is
designed to be followed solo, at your own pace.

---

## Learning goals

- **The mental model** — an LLM predicts the next token; it does not "reason" or "look things up".
- **Prompts & messages** — system instructions, chat history, and the context window.
- **Structured output** — get reliable JSON back with a schema (the glue between agents).
- **Tool calling** — let the LLM request Python functions it can't do itself.
- **Hallucinations** — why they happen and three ways to defend against them.
- **Temperature & top-p** — the randomness dials, and why production loves determinism.
- **Token costs** — estimate before you send, read actual usage, build cheap habits.
- **ReAct** — build a transparent Thought → Action → Observation loop by hand.

---

## Prerequisites

- Project virtual environment active (from repo root):
  ```bash
  source .venv/bin/activate            # Windows: .venv\Scripts\activate
  pip install -r requirements.txt      # installs langchain + langchain-google-genai + python-dotenv
  ```
  > Versions are pinned in the root `requirements.txt`. If a pin ever fails to
  > install, drop the `==version` to grab the latest compatible release.
- A **free Google Gemini API key** (next section).

---

## Get your FREE Gemini API key (about 1 minute)

We use **Google Gemini** because it has the most generous *no-credit-card* free
tier — perfect for learning. See the comparison table below for why.

1. Go to **https://aistudio.google.com/apikey** and sign in with a Google account.
2. Click **Create API key** → copy the key.
3. In this folder, copy the template and paste your key in:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and replace `paste-your-key-here` with your key. Save.
4. Verify everything works:
   ```bash
   python 00_setup_check.py
   ```
   If it prints a greeting from Gemini, you're ready.

> Your `.env` is git-ignored — the key never gets committed. **Never share it or
> paste it into a script.**

---

## Which LLM should you use? (free options, June 2026)

You can build this entire session for **$0**. Here's the current landscape of
free API tiers. Numbers change often — always confirm at each provider's site.

| Provider | Best free model | Free limits (approx) | Credit card? | Notes |
|----------|-----------------|----------------------|--------------|-------|
| **Google Gemini** ⭐ | Gemini 2.5 Flash / Flash-Lite | ~10-15 RPM, 250-1,000 req/day, 250K tokens/min | **No** | Most accessible free baseline, huge context window. **What we use.** |
| **Groq** | Llama 4 / Qwen3-32B | ~30 RPM, ~1,000 req/day, 500K tokens/day | **No** | *Fastest* inference (hundreds of tokens/sec). Great free alternative. |
| **Mistral** | open-mixtral-8x7b | ~60 RPM, very high monthly tokens | No | Generous, but prompts may be used for training — privacy tradeoff. |
| **OpenAI** | GPT-3.5 (free tier) | 3 RPM, GPT-5.x **not** on free tier | **Yes** (for real use) | Industry standard but effectively needs a ~$5 deposit. Session 6 uses it. |
| **Anthropic Claude** | — | No permanent free tier (~$5 trial, expires) | **Yes** | Best-in-class reasoning, but not free. |

> **Sources:** klymentiev.com/blog/free-llm-api, apiscout.dev, stochasticsandbox.com
> (all June 2026). Free tiers change frequently — verify current limits at
> `ai.google.dev` / `console.groq.com` before relying on them.

**Want to swap providers later?** Because we use LangChain, the code barely
changes — e.g. `pip install langchain-groq`, then use `ChatGroq(...)` instead of
`ChatGoogleGenerativeAI(...)` in `llm_utils.py`. Same interface, different engine.

---

## How to run

Every file is a plain script. Run them one at a time, in order:

```bash
python 00_setup_check.py
python 01_what_llm_does.py
# ...and so on through 08
```

Read the comments at the top of each file first — they explain the concept
before any code runs.

---

## The walkthrough — one idea per file

| File | The question it answers | New concepts |
|------|-------------------------|--------------|
| `00_setup_check.py` | Is my setup working? | `.env`, first `model.invoke()` |
| `01_what_llm_does.py` | What *is* an LLM, really? | next-token prediction, non-determinism |
| `02_prompts_and_messages.py` | How do I hold a conversation? | System/Human/AI messages, history, context window |
| `03_structured_output.py` | How do I get reliable JSON? | `with_structured_output`, Pydantic schema |
| `04_tool_calling.py` | How does the LLM use functions? | `@tool`, `bind_tools`, tool call → execute → answer |
| `05_hallucinations.py` | Why does it confidently lie? | grounding, "I don't know" escape hatch, verification |
| `06_temperature_topp.py` | How do I control randomness? | temperature, top-p, determinism |
| `07_token_costs.py` | What does this cost? | input/output tokens, usage metadata, cost math |
| `08_react_from_scratch.py` | How does an agent *think*? | ReAct loop, context engineering |

Shared setup lives in **`llm_utils.py`** (the model connection + token helpers),
so each script stays short. Sanity-check it any time with `python llm_utils.py`.

---

## Homework options (pick one)

1. **Batch tester** — write a script that asks the LLM **10 manufacturing
   questions** and parses each into structured JSON (reuse `03`). Log every case
   where parsing or the answer breaks. Total the tokens/cost.
2. **Note extractor** — prompt-engineer the model to pull **structured defect
   records** from messy operator notes. Evaluate accuracy by hand on 10 notes.
3. **Hallucination hunt** — find **3 manufacturing questions** where the model is
   confidently wrong, and document exactly how you'd *catch* each one in
   production.

---

## Folder structure

```
Session5-LLM-Fundamentals/
├── .env.example                 ← copy to .env and add your free Gemini key
├── llm_utils.py                 ← shared: model setup + token/cost helpers
├── 00_setup_check.py            ← start here: verify your setup
├── 01_what_llm_does.py
├── 02_prompts_and_messages.py
├── 03_structured_output.py
├── 04_tool_calling.py
├── 05_hallucinations.py
├── 06_temperature_topp.py
├── 07_token_costs.py
├── 08_react_from_scratch.py     ← build a thinking loop by hand
└── README.md
```

---

## Troubleshooting

- **`No Gemini API key found`** — copy `.env.example` to `.env` and paste your key (see above).
- **`ModuleNotFoundError: langchain_google_genai`** — activate the `.venv`, then `pip install -r requirements.txt`.
- **`429 / ResourceExhausted`** — you hit the free rate limit. Wait a minute, or switch to `gemini-2.5-flash-lite` (higher daily cap) in `llm_utils.py`.
- **Model name error** — Google renames models over time. Check current names at `ai.google.dev` and update `DEFAULT_MODEL` in `llm_utils.py`.
- **Empty/blocked reply** — a safety filter may have triggered; rephrase the prompt.
