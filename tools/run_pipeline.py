"""
run_pipeline.py — WANDAR LinkedIn Pipeline Orchestrator

Runs automatically via GitHub Actions every Sunday at 08:00 EDT.
Can also be triggered manually: python tools/run_pipeline.py

Agent chain:
  1. KB Agent    — assembles knowledge-bank context
  2. Scanner     — searches for trending signals (Tavily)
  3. Strategist  — decides what posts to write this week
  4. Writer      — writes the posts (N posts, per Strategist decision)
  5. Chief Editor— reviews and finalises every post before publish

Outputs:
  outputs/research/YYYY-MM-DD-research.md  + .xlsx
  outputs/strategy/YYYY-MM-DD-strategy.md  + .xlsx
  outputs/drafts/YYYY-MM-DD-week-1.md      + .docx
  outputs/final/YYYY-MM-DD-week-1-final.md + .docx
  Google Drive: pipeline outputs folder (draft files)
  Google Drive: Ready to Post folder (final.docx)
  Slack: success notification with Drive links

Required environment variables:
  ANTHROPIC_API_KEY
  TAVILY_API_KEY
  SLACK_WEBHOOK_URL
  GDRIVE_TOKEN_JSON        (contents of tools/.gdrive-token.json)
  GDRIVE_CREDENTIALS_JSON  (contents of tools/credentials.json)
  GDRIVE_FINAL_FOLDER_ID   (Google Drive folder ID for ready-to-post content)
"""

import os
import sys
import json
import subprocess
import requests
from pathlib import Path
from datetime import date

try:
    import anthropic
except ImportError:
    print("Error: anthropic not installed. Run: pip install anthropic")
    sys.exit(1)

ROOT = Path(__file__).parent.parent
TOOLS = ROOT / "tools"
AGENTS_DIR = ROOT / "agents"
CHIEF_EDITOR_DIR = ROOT / "chief-editor"
KB_DIR = ROOT / "knowledge-bank"
TMP_DIR = ROOT / "tmp"
OUTPUTS = ROOT / "outputs"

TODAY = date.today().isoformat()
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 8192


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_text(path):
    p = Path(path)
    if p.exists():
        return p.read_text(encoding="utf-8")
    return ""


def write_text(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"  Wrote: {p}")


def load_config():
    cfg_path = TOOLS / "config.json"
    if cfg_path.exists():
        return json.loads(cfg_path.read_text(encoding="utf-8"))
    return {}


def call_claude(system_prompt, user_message, label=""):
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    print(f"\n[{label}] Calling Claude ({MODEL})...")
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    text = response.content[0].text
    print(f"[{label}] Done ({len(text)} chars)")
    return text


def tavily_search(query, max_results=5):
    api_key = os.environ.get("TAVILY_API_KEY", "")
    if not api_key:
        print(f"  [search] TAVILY_API_KEY not set — skipping: {query}")
        return []
    try:
        resp = requests.post(
            "https://api.tavily.com/search",
            json={"api_key": api_key, "query": query, "max_results": max_results, "search_depth": "advanced"},
            timeout=20,
        )
        resp.raise_for_status()
        return resp.json().get("results", [])
    except Exception as e:
        print(f"  [search] Error for '{query}': {e}")
        return []


def run_script(script_name, *args):
    cmd = [sys.executable, str(TOOLS / script_name)] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.returncode != 0 and result.stderr:
        print(f"  Warning from {script_name}: {result.stderr.strip()}")


def slack_notify(message):
    webhook = os.environ.get("SLACK_WEBHOOK_URL") or load_config().get("slack_webhook_url", "")
    if not webhook or "YOUR_WEBHOOK" in webhook:
        print("  Slack webhook not configured — skipping notification")
        return
    try:
        requests.post(webhook, json={"text": message}, timeout=10)
    except Exception as e:
        print(f"  Slack notification failed: {e}")


def upload_to_drive(file_path, folder_id=None):
    if not file_path.exists():
        print(f"  Drive upload skipped (file not found): {file_path}")
        return None

    cmd = [sys.executable, str(TOOLS / "upload_gdrive.py"), str(file_path)]
    if folder_id:
        cmd += ["--folder-id", folder_id]

    env = os.environ.copy()
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    output = result.stdout.strip()
    if output:
        print(output)

    # Extract URL from output
    for line in output.splitlines():
        if "drive.google.com" in line:
            return line.strip()
    return None


# ---------------------------------------------------------------------------
# Step 1: KB Agent — assemble knowledge-bank context
# ---------------------------------------------------------------------------

def run_kb_agent():
    print("\n=== Step 1: KB Agent ===")

    kb_files = {
        "INDEX": load_text(KB_DIR / "INDEX.md"),
        "hooks": "\n\n".join(load_text(f) for f in sorted((KB_DIR / "hooks").glob("*.md")) if f.exists()) if (KB_DIR / "hooks").exists() else "",
        "voice_patterns": load_text(KB_DIR / "voice-patterns" / "examples.md"),
        "engagement": load_text(KB_DIR / "engagement" / "patterns.md"),
        "traveler_intel": load_text(KB_DIR / "traveler-intel" / "behavior.md"),
        "operator_lang": load_text(KB_DIR / "operator-lang" / "language.md"),
        "narrative_frameworks": load_text(KB_DIR / "narrative-frameworks" / "frameworks.md"),
        "algorithm": load_text(KB_DIR / "algorithm-intel" / "linkedin-algorithm.md"),
        "brew360": load_text(KB_DIR / "algorithm-intel" / "brew360-latest.md"),
    }

    pillar_intel = ""
    pillar_dir = KB_DIR / "pillar-intel"
    if pillar_dir.exists():
        for f in sorted(pillar_dir.glob("*.md")):
            pillar_intel += f"\n\n### {f.stem}\n" + load_text(f)

    agent_prompt = load_text(AGENTS_DIR / "00-knowledge-bank.md")

    system = f"""{agent_prompt}

You are running at pipeline START. Assemble the KB context package for this week's pipeline run.
Today's date: {TODAY}

Here is the full Knowledge Bank content:

## INDEX
{kb_files['INDEX']}

## HOOKS
{kb_files['hooks']}

## VOICE PATTERNS
{kb_files['voice_patterns']}

## PILLAR INTEL
{pillar_intel}

## ENGAGEMENT PATTERNS
{kb_files['engagement']}

## TRAVELER INTEL
{kb_files['traveler_intel']}

## OPERATOR LANGUAGE
{kb_files['operator_lang']}

## NARRATIVE FRAMEWORKS
{kb_files['narrative_frameworks']}

## ALGORITHM INTEL — LinkedIn
{kb_files['algorithm']}

## ALGORITHM INTEL — Brew360
{kb_files['brew360']}
"""

    user_msg = f"""Assemble the KB context package for {TODAY}.

Follow the context package format defined in your role. Extract only the most relevant intelligence for this week's pipeline run. Write the complete context package as your output — this will be passed directly to the Scanner and Strategist agents."""

    context = call_claude(system, user_msg, "KB Agent")

    out_path = TMP_DIR / f"kb-context-{TODAY}.md"
    write_text(out_path, f"# KB Context Package — {TODAY}\n\n{context}")
    return context


# ---------------------------------------------------------------------------
# Step 2: Scanner — external signals via Tavily
# ---------------------------------------------------------------------------

def run_scanner(kb_context):
    print("\n=== Step 2: Scanner ===")

    search_queries = [
        "safari operator marketing 2026",
        "luxury safari travel news 2026",
        "East Africa safari travel trends 2026",
        "safari booking behavior 2026",
        "social listening travel industry 2026",
        "reddit safari planning 2026",
        "Maasai Mara OR Serengeti travel 2026",
        "safari operator technology 2026",
        "luxury travel industry news 2026",
        "African safari demand 2026",
    ]

    print("  Running web searches via Tavily...")
    search_results = []
    for query in search_queries:
        results = tavily_search(query, max_results=3)
        for r in results:
            search_results.append({
                "query": query,
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", "")[:500],
            })

    search_summary = "\n\n".join(
        f"Query: {r['query']}\nTitle: {r['title']}\nURL: {r['url']}\nSnippet: {r['content']}"
        for r in search_results
    )

    agent_prompt = load_text(AGENTS_DIR / "01-scanner.md")

    system = f"""{agent_prompt}

Today's date: {TODAY}
You have already completed the web searches. Here are the raw results to analyse and score."""

    user_msg = f"""Here are the web search results from today's scan:

{search_summary}

---

Analyse all results. Apply the pillar filter, scoring rubric, and virality tagging from your role instructions.

Output the full scanner report in the exact format specified in your role. Include:
- Summary
- Qualified signals table (with pillar, score, virality type, recommended angle)
- Hot take alerts (score 8+ on relevance)
- Discarded signals

Write the report now. Today is {TODAY}."""

    scanner_out = call_claude(system, user_msg, "Scanner")

    research_md = OUTPUTS / "research" / f"{TODAY}-research.md"
    write_text(research_md, f"# Scanner Report — {TODAY}\n\n{scanner_out}")
    return scanner_out, research_md


# ---------------------------------------------------------------------------
# Step 3: Strategist — decide this week's posts
# ---------------------------------------------------------------------------

def run_strategist(kb_context, scanner_out):
    print("\n=== Step 3: Strategist ===")

    post_history = load_text(ROOT / "posted" / "posted-history.md")
    agent_prompt = load_text(AGENTS_DIR / "02-content-strategist.md")

    system = f"""{agent_prompt}

Today's date: {TODAY}
You have the KB context and Scanner report. Decide this week's content plan."""

    user_msg = f"""## KB Context Package

{kb_context}

---

## Scanner Report

{scanner_out}

---

## Post History

{post_history if post_history else "No post history yet."}

---

Decide this week's content plan. Apply pillar rotation rules and bucket ratio checks.

For each post brief, determine: bucket, pillar, virality strategy, hook direction, narrative arc, posting day, distribution notes, and target metric.

The number of posts this week is your decision based on the signals available — write as many briefs as the signals justify. If there are 3 strong signals, write 3 posts. If there are 5, write 5.

Output the complete strategy document in the format specified in your role. Today is {TODAY}."""

    strategy_out = call_claude(system, user_msg, "Strategist")

    strategy_md = OUTPUTS / "strategy" / f"{TODAY}-strategy.md"
    write_text(strategy_md, f"# Content Strategy — Week of {TODAY}\n\n{strategy_out}")
    return strategy_out, strategy_md


# ---------------------------------------------------------------------------
# Step 4: Writer — write the posts
# ---------------------------------------------------------------------------

def run_writer(kb_context, strategy_out):
    print("\n=== Step 4: Writer ===")

    agent_prompt = load_text(AGENTS_DIR / "03-writer.md")

    system = f"""{agent_prompt}

Today's date: {TODAY}
You have the Strategist's complete brief and the KB context (voice patterns, hooks, traveler language)."""

    user_msg = f"""## Strategist Brief

{strategy_out}

---

## KB Context (voice patterns, hooks, traveler language)

{kb_context}

---

Write every post briefed by the Strategist. Do not skip any.

Apply all hard content rules: no em dashes, no generic phrasing, Unicode Bold Sans-Serif on hook lines only, short sentences, safari-specific voice.

Pass every post through all 5 quality tests before finalising.

Output every post in the exact format specified in your role (PILLAR / BUCKET / FORMAT / VIRALITY STRATEGY / BEST DAY / POSTING WINDOW / full post copy / WHY THIS WORKS / IMAGE DIRECTION).

All posts go in a single output. Today is {TODAY}."""

    writer_out = call_claude(system, user_msg, "Writer")

    draft_md = OUTPUTS / "drafts" / f"{TODAY}-week-1.md"
    write_text(draft_md, writer_out)
    return writer_out, draft_md


# ---------------------------------------------------------------------------
# Step 5: Chief Content Editor — review and finalise
# ---------------------------------------------------------------------------

def load_editor_knowledge():
    parts = [load_text(CHIEF_EDITOR_DIR / "CLAUDE.md")]
    knowledge_dir = CHIEF_EDITOR_DIR / "knowledge"
    if knowledge_dir.exists():
        for f in sorted(knowledge_dir.glob("*.md")):
            if f.name != "index.md":
                parts.append(f"\n\n---\n\n# Knowledge: {f.stem}\n\n" + load_text(f))
    key_workflows = ["03_diagnose.md", "04_rewrite.md", "05_distribution_upgrade.md", "06_output.md"]
    workflows_dir = CHIEF_EDITOR_DIR / "workflows"
    if workflows_dir.exists():
        for wf in key_workflows:
            wf_path = workflows_dir / wf
            if wf_path.exists():
                parts.append(f"\n\n---\n\n# Workflow: {wf}\n\n" + load_text(wf_path))
    return "\n".join(parts)


def run_editor(writer_out):
    print("\n=== Step 5: Chief Content Editor ===")

    editor_knowledge = load_editor_knowledge()

    system = f"""{editor_knowledge}

Today's date: {TODAY}
Channel: LinkedIn
Audience: Luxury safari operators and DMC principals

You are reviewing LinkedIn posts written by the Writer agent. Apply your full editorial workflow to every post:
- Step 3 (Diagnose): flag every issue
- Step 4 (Rewrite): apply the correct intervention level
- Step 5 (Distribution Upgrade): pass all 5 distribution checks
- Step 6 (Output): final QC — only pass if all 9 criteria are met

Do not ask clarifying questions. The channel is LinkedIn, the audience is operators, and the brief context is embedded in each post's metadata. Proceed directly to diagnosis and editing."""

    user_msg = f"""Here are the LinkedIn posts written by the Writer agent this week. Review and finalise every post.

{writer_out}

---

For each post:
1. Diagnose: identify any issues (generic phrasing, AI style, em dashes, weak hook, distribution problems)
2. Rewrite: apply light edit, medium rewrite, heavy rewrite, or full reconstruction — whatever is needed
3. Distribution upgrade: confirm opening lines, problem clarity, specificity, shareability, AEO phrasing
4. Final QC: only output if all 9 pass criteria are met

Output the final, publication-ready version of every post in the same format as the Writer's output (PILLAR / BUCKET / FORMAT / VIRALITY STRATEGY / BEST DAY / POSTING WINDOW / post copy / WHY THIS WORKS / IMAGE DIRECTION).

Do not include editorial commentary in the final output — clean Markdown posts only."""

    editor_out = call_claude(system, user_msg, "Chief Editor")

    final_md = OUTPUTS / "final" / f"{TODAY}-week-1-final.md"
    write_text(final_md, editor_out)
    return editor_out, final_md


# ---------------------------------------------------------------------------
# Step 6 & 7: Generate Excel and Word files
# ---------------------------------------------------------------------------

def generate_outputs(research_md, strategy_md, draft_md, final_md):
    print("\n=== Step 6-7: Generate Excel + Word ===")
    run_script("generate_excel.py", str(research_md))
    run_script("generate_excel.py", str(strategy_md))
    run_script("generate_word.py", str(draft_md))
    run_script("generate_word.py", str(final_md))


# ---------------------------------------------------------------------------
# Steps 8 & 9: Upload to Google Drive
# ---------------------------------------------------------------------------

def upload_outputs(research_md, strategy_md, draft_md, final_md):
    print("\n=== Step 8-9: Upload to Google Drive ===")

    config = load_config()
    pipeline_folder = config.get("google_drive_folder_id", "")
    final_folder = os.environ.get("GDRIVE_FINAL_FOLDER_ID") or config.get("gdrive_final_folder_id", "")

    drive_links = []

    # Pipeline outputs folder — research, strategy, draft
    print("\nPipeline Outputs folder:")
    for f in [research_md.with_suffix(".xlsx"), strategy_md, draft_md.with_suffix(".docx")]:
        url = upload_to_drive(f, pipeline_folder if pipeline_folder not in ("", "YOUR_FOLDER_ID_HERE") else None)
        if url:
            drive_links.append(url)

    # Ready to Post folder — final only
    if final_folder and final_folder not in ("YOUR_READY_TO_POST_FOLDER_ID_HERE", ""):
        print("\nReady to Post folder:")
        final_docx = final_md.with_suffix(".docx")
        url = upload_to_drive(final_docx, final_folder)
        if url:
            drive_links.append(url)
    else:
        print("  Ready to Post folder not configured — skipping final upload")

    return drive_links


# ---------------------------------------------------------------------------
# Step 10: Slack success notification
# ---------------------------------------------------------------------------

def notify_success(drive_links):
    print("\n=== Step 10: Slack Notification ===")
    link_list = "\n".join(f"• {u}" for u in drive_links) if drive_links else "• Drive upload not configured"
    message = (
        f"✅ *Wandar LinkedIn pipeline complete* — {TODAY}\n\n"
        f"Posts written, edited by Chief Content Editor, and uploaded to Google Drive.\n\n"
        f"*Files ready:*\n{link_list}"
    )
    slack_notify(message)
    print("  Slack notification sent.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"\n{'='*60}")
    print(f"WANDAR LinkedIn Pipeline — {TODAY}")
    print(f"{'='*60}")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)

    TMP_DIR.mkdir(parents=True, exist_ok=True)

    # Run all 5 agents
    kb_context = run_kb_agent()
    scanner_out, research_md = run_scanner(kb_context)
    strategy_out, strategy_md = run_strategist(kb_context, scanner_out)
    writer_out, draft_md = run_writer(kb_context, strategy_out)
    editor_out, final_md = run_editor(writer_out)

    # Generate formatted files
    generate_outputs(research_md, strategy_md, draft_md, final_md)

    # Upload to Drive
    drive_links = upload_outputs(research_md, strategy_md, draft_md, final_md)

    # Notify success
    notify_success(drive_links)

    print(f"\n{'='*60}")
    print(f"Pipeline complete. {TODAY}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
