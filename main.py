"""
════════════════════════════════════════════════════════════════════════════════
  CodeSentinel AI
  Autonomous Market Intelligence & Content Strategy Pipeline

  Course  : Agent Orchestration (אורקסטרציה של סוכנים)
  Assignment : 05
  Instructor : Dr. Yoram Segel
  Group Code : biu-he01
  Date       : 2026-06-16
════════════════════════════════════════════════════════════════════════════════

SYSTEM OVERVIEW
───────────────
This CrewAI pipeline simulates an autonomous strategic consulting team that
produces a complete Go-To-Market content package for an AI startup — with zero
human input between steps. Four specialist agents collaborate via a sequential
process, each building directly on the verified output of the previous agent.

PIPELINE ARCHITECTURE
─────────────────────
  [Agent 1] Dr. Maya Chen — Market Intelligence Analyst
      ↓ Market Intelligence Report
  [Agent 2] Prof. Alex Rivera — Customer Psychology Expert
      ↓ ICP Profiles (informed by market report)
  [Agent 3] Marcus Thompson — Content Strategy Architect
      ↓ 90-Day Strategy Blueprint (informed by market report + ICPs)
  [Agent 4] Sophia Laurent — Creative Content Director
      ↓ Production-Ready Content Assets (informed by strategy)

PROCESS : Sequential (Process.sequential)
VERBOSE  : True  (enables step-by-step agent reasoning visibility)
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# ── Load .env before anything else ───────────────────────────────────────────
load_dotenv()

# ── Fix Unicode output on Windows Hebrew terminals ───────────────────────────
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# ── CrewAI core imports ───────────────────────────────────────────────────────
from crewai import Agent, Task, Crew, Process, LLM
import litellm

def _patch_litellm_for_groq():
    """
    Two fixes for Groq compatibility with crewai 1.x:
    1. Strip cache_breakpoint — Groq rejects Anthropic-style cache markers.
    2. Auto-retry on rate limits — Groq free tier is 12,000 TPM; wait and retry.
    """
    import time
    import asyncio
    from litellm.exceptions import RateLimitError

    _orig_completion  = litellm.completion
    _orig_acompletion = litellm.acompletion
    MAX_RETRIES = 6

    def _strip(kwargs):
        for msg in kwargs.get("messages", []):
            if isinstance(msg, dict):
                msg.pop("cache_breakpoint", None)

    def patched_completion(*a, **kw):
        _strip(kw)
        for attempt in range(MAX_RETRIES):
            try:
                return _orig_completion(*a, **kw)
            except RateLimitError:
                if attempt < MAX_RETRIES - 1:
                    wait = 30 + attempt * 15
                    print(f"\n  [Rate limit] Waiting {wait}s (retry {attempt+1}/{MAX_RETRIES-1})...")
                    time.sleep(wait)
                else:
                    raise

    async def patched_acompletion(*a, **kw):
        _strip(kw)
        for attempt in range(MAX_RETRIES):
            try:
                return await _orig_acompletion(*a, **kw)
            except RateLimitError:
                if attempt < MAX_RETRIES - 1:
                    wait = 30 + attempt * 15
                    print(f"\n  [Rate limit] Waiting {wait}s (retry {attempt+1}/{MAX_RETRIES-1})...")
                    await asyncio.sleep(wait)
                else:
                    raise

    litellm.completion  = patched_completion
    litellm.acompletion = patched_acompletion

_patch_litellm_for_groq()


# ── LLM factory ──────────────────────────────────────────────────────────────
def get_llm() -> LLM:
    """Return a Groq-backed LLM via CrewAI's LiteLLM bridge."""
    return LLM(
        model=os.getenv("GROQ_MODEL", "groq/llama-3.3-70b-versatile"),
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7,
    )


# ════════════════════════════════════════════════════════════════════════════════
#  GLOBAL STARTUP CONTEXT
#  Injected into Task #1 so all downstream agents receive the same
#  product framing through the context-chain mechanism.
# ════════════════════════════════════════════════════════════════════════════════

STARTUP_CONTEXT = """
COMPANY: CodeSentinel AI
STAGE  : Series A — Post product-market-fit, preparing GTM expansion

PRODUCT:
  An AI-powered automated code review SaaS platform for software engineering
  teams. The platform combines large-language-model code understanding with
  deterministic static analysis to surface bugs, security vulnerabilities,
  and architectural anti-patterns inside pull requests — before they reach
  production. Integrates natively with GitHub, GitLab, and Bitbucket.

TARGET MARKET:
  Software development teams of 10–500 engineers at technology companies,
  ranging from hypergrowth Series A–C startups to mid-market enterprises.

KEY DIFFERENTIATOR:
  Unlike legacy static-analysis tools, CodeSentinel AI understands *intent*
  — it can detect when code is technically valid but logically wrong relative
  to the PR description. Unlike generic LLM coding assistants, it produces
  zero-hallucination, evidence-backed findings with file-line citations.
"""


# ════════════════════════════════════════════════════════════════════════════════
#  SECTION 1: AGENT DEFINITIONS
#  Each agent is given a rich, character-driven backstory that functions as
#  a detailed system prompt — shaping how the LLM reasons and responds.
# ════════════════════════════════════════════════════════════════════════════════

def build_agents(llm: LLM) -> list:
    """Instantiate all four specialist agents and return them as a list."""

    # ──────────────────────────────────────────────────────────────────────────
    #  AGENT 1: Market Intelligence Analyst
    # ──────────────────────────────────────────────────────────────────────────
    market_analyst = Agent(
        role="Senior AI Market Intelligence Analyst",
        goal=(
            "Conduct a rigorous, evidence-based market analysis of the AI-powered "
            "code review landscape. Size the opportunity, map the competition, surface "
            "five macro trends, rank the top three customer segments, and identify "
            "three defensible Blue Ocean gaps where CodeSentinel AI can establish "
            "an uncontested competitive moat."
        ),
        backstory=(
            "You are Dr. Maya Chen — Silicon Valley's most respected market intelligence "
            "oracle. You began your career building quantitative tech-sector models at "
            "Goldman Sachs before spending eight years at McKinsey's Technology Practice, "
            "where you led market-entry strategies for 60+ enterprise software companies "
            "— three of which went on to IPO.\n\n"
            "Your proprietary 'Blue Ocean Detection Methodology' was published in the "
            "Harvard Business Review and is now a standard framework at Y Combinator and "
            "a16z for pre-investment market validation. You have an almost supernatural "
            "ability to distinguish genuine market inflection points from hype cycles, "
            "and you are famous for delivering reports that are simultaneously the most "
            "thorough AND the most actionable in the room.\n\n"
            "You are constitutionally incapable of presenting hand-waving or unfounded "
            "claims. Every assertion in your reports is anchored to a specific data point, "
            "analyst citation, or logical first-principle. Your professional mantra:\n"
            "'The market doesn't lie — but only if you ask the right questions.'"
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        llm=llm,
    )

    # ──────────────────────────────────────────────────────────────────────────
    #  AGENT 2: Customer Psychology Expert
    # ──────────────────────────────────────────────────────────────────────────
    persona_expert = Agent(
        role="Chief Customer Psychology Expert & ICP Architect",
        goal=(
            "Transform the market intelligence findings into three richly detailed "
            "Ideal Customer Profiles (ICPs) — revealing not just WHO the buyer is, "
            "but WHY they buy, WHAT keeps them awake at 2 a.m., and EXACTLY what "
            "trigger will make them commit their budget to CodeSentinel AI today."
        ),
        backstory=(
            "You are Professor Alex Rivera — the behavioral economist who decoded "
            "why B2B buyers make the decisions they do, not the decisions they claim "
            "to make. Armed with a PhD in Behavioral Economics from MIT and an MBA "
            "from Wharton, you spent a decade at McKinsey's Behavioral Science Lab "
            "before becoming the go-to ICP architect for hypergrowth B2B SaaS companies.\n\n"
            "Your landmark 'Pain Hierarchy Framework' — mapping customer pain across "
            "functional (what doesn't work), emotional (how it makes them feel), and "
            "social (how it affects their standing) dimensions — has been adopted by "
            "over 400 startups and is core curriculum at Y Combinator. You have "
            "personally conducted more than 2,500 customer discovery interviews in the "
            "developer tools space.\n\n"
            "You hold a fierce contrarian belief that most companies build products for "
            "the customer they *imagine* exists, not the customer who actually exists. "
            "Your mission is to destroy comfortable fictions and replace them with "
            "radical, evidence-grounded clarity. You measure the quality of a persona "
            "by one test: does it make the product manager *uncomfortable* because it "
            "is uncomfortably specific?"
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        llm=llm,
    )

    # ──────────────────────────────────────────────────────────────────────────
    #  AGENT 3: Content Strategy Architect
    # ──────────────────────────────────────────────────────────────────────────
    strategy_architect = Agent(
        role="Chief Content Strategy Architect & Thought Leadership Director",
        goal=(
            "Design a comprehensive, ROI-obsessed 90-Day Content Strategy Blueprint "
            "that positions CodeSentinel AI as the category-defining thought leader in "
            "AI code review — with a clear content mission, four audience-mapped content "
            "pillars, an optimized channel mix, a detailed Month 1 editorial calendar, "
            "and a measurement framework tied directly to pipeline creation."
        ),
        backstory=(
            "You are Marcus Thompson — the most battle-tested content strategist in "
            "the developer tools ecosystem. You served as Head of Content at Stripe, "
            "where you built their developer content engine from zero to 3 million "
            "monthly readers in 24 months. You then joined HubSpot as VP of Content, "
            "where your content-led growth strategy generated $240 million in attributed "
            "pipeline in 18 months — a result that earned you a front-page feature "
            "in TechCrunch.\n\n"
            "You pioneered the 'Content-Led Growth' methodology, now taught in "
            "Stanford's Product Management curriculum, which treats content as a "
            "compounding business asset rather than a discretionary cost center. "
            "You are a legendary opponent of 'content for content's sake' and have "
            "personally killed $4M+ worth of content programs that had no path to "
            "revenue.\n\n"
            "You believe that in the AI era, companies that own the *narrative* own "
            "the *market*. Your strategies always account for algorithmic distribution "
            "compounding, the asymmetric returns of category-defining thought leadership, "
            "and the precise interplay of top-of-funnel trust and bottom-of-funnel "
            "conversion. You refuse to write strategy that cannot be measured."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        llm=llm,
    )

    # ──────────────────────────────────────────────────────────────────────────
    #  AGENT 4: Creative Content Director
    # ──────────────────────────────────────────────────────────────────────────
    content_director = Agent(
        role="Senior Creative Content Director & Conversion Copywriter",
        goal=(
            "Execute the approved content strategy by producing three categories of "
            "production-ready content assets: a long-form flagship blog post with "
            "three headline variants, two high-engagement LinkedIn thought leadership "
            "posts, and a three-email welcome nurture sequence — all calibrated to the "
            "specific ICP pain points and designed to drive measurable engagement "
            "and pipeline."
        ),
        backstory=(
            "You are Sophia Laurent — the rare copywriter who can make a senior "
            "engineer stop scrolling mid-thumb-swipe. You trained under direct disciples "
            "of David Ogilvy at Wieden+Kennedy before pivoting to B2B SaaS content and "
            "discovering your true calling: making complex technical products feel "
            "viscerally exciting to the people who need them most.\n\n"
            "You learned to code specifically so you could write more authentically for "
            "technical audiences — a decision that transformed your career. Your blog "
            "posts have reached the front page of Hacker News nine times. Your email "
            "sequences achieve open rates 3.4x the industry benchmark. You once wrote "
            "a LinkedIn post for a developer tools company that generated 847 qualified "
            "demo requests in 72 hours.\n\n"
            "You operate by one professional religion: the reader's time is sacred. "
            "Every sentence must earn its right to exist. You despise jargon-stuffed, "
            "corporate-speak content with a passion that borders on theatrical, and "
            "you measure every word against a single ruthless question:\n"
            "'Would I stop scrolling for this?'\n\n"
            "You believe the best B2B writing sounds like it was written by a brilliant "
            "friend who happens to be an expert — not by a marketing team hitting a "
            "content calendar deadline."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        llm=llm,
    )

    return [market_analyst, persona_expert, strategy_architect, content_director]


# ════════════════════════════════════════════════════════════════════════════════
#  SECTION 2: TASK DEFINITIONS
#  Tasks are defined with detailed descriptions and explicit expected_output
#  specifications. The 'context' parameter creates the information flow chain:
#    Task 2 receives output of Task 1 as context.
#    Task 3 receives outputs of Tasks 1 and 2 as context.
#    Task 4 receives output of Task 3 as context.
# ════════════════════════════════════════════════════════════════════════════════

def build_tasks(agents: list) -> list:
    """Define all tasks with context chains and return them in execution order."""

    market_analyst, persona_expert, strategy_architect, content_director = agents

    # ──────────────────────────────────────────────────────────────────────────
    #  TASK 1: Market Intelligence Analysis
    #  Agent    : market_analyst
    #  Context  : None (first in chain)
    #  Output   : Passes to Tasks 2 and 3
    # ──────────────────────────────────────────────────────────────────────────
    market_research_task = Task(
        description=(
            f"You are conducting market analysis for the following startup:\n\n"
            f"{STARTUP_CONTEXT}\n\n"
            "Produce a comprehensive Market Intelligence Report covering ALL six "
            "sections below. Be analytical, specific, and evidence-informed.\n\n"

            "**SECTION 1 — Market Sizing**\n"
            "Estimate the Total Addressable Market (TAM), Serviceable Addressable "
            "Market (SAM), and Serviceable Obtainable Market (SOM) for AI-powered "
            "code review tools in 2024–2026. Include CAGR projection and the key "
            "structural drivers of market growth (e.g., rise of DevSecOps, AI "
            "developer tooling wave, shift-left testing mandates).\n\n"

            "**SECTION 2 — Competitive Landscape**\n"
            "Analyze 8–10 direct and indirect competitors. Include: GitHub Copilot "
            "PR Review, Snyk DeepCode, SonarQube, CodeClimate, Codacy, Amazon "
            "CodeGuru, Qodo (formerly CodiumAI), and at least one emerging AI-native "
            "entrant. For each: positioning statement, pricing tier, primary "
            "differentiator, and most critical competitive weakness.\n\n"

            "**SECTION 3 — Macro Trends**\n"
            "Identify and analyze 5 macro trends reshaping the AI code review market. "
            "For each trend: name, 2-3 sentence description, and the specific "
            "strategic implication for CodeSentinel AI (opportunity or threat).\n\n"

            "**SECTION 4 — Customer Segments**\n"
            "Identify and rank the top 3 customer segments by a composite score of: "
            "(a) market size, (b) willingness to pay, (c) competitive accessibility. "
            "Include firmographic characteristics and a segment attractiveness score "
            "(1–10) with explicit rationale for each.\n\n"

            "**SECTION 5 — Blue Ocean Opportunities**\n"
            "Identify 3 specific, defensible market gaps where CodeSentinel AI can "
            "establish uncontested positioning. For each: describe the gap precisely, "
            "explain why it is currently underserved by existing competitors, and "
            "articulate CodeSentinel AI's unique advantage in filling it.\n\n"

            "**SECTION 6 — GTM Strategic Recommendations**\n"
            "Provide 3 actionable go-to-market recommendations informed by the above "
            "analysis. Include: recommended initial vertical or beachhead, preferred "
            "distribution channel(s), and one high-leverage partnership or ecosystem "
            "play. Each recommendation must be tied to a specific market finding."
        ),
        expected_output=(
            "A structured Market Intelligence Report in clean markdown with these exact sections:\n\n"
            "## Executive Summary\n"
            "  Five bullet points capturing the most critical, decision-relevant findings.\n\n"
            "## Market Size Analysis\n"
            "  TAM / SAM / SOM estimates with reasoning, CAGR, and growth drivers.\n\n"
            "## Competitive Landscape\n"
            "  Markdown table: Competitor | Positioning | Price Tier | Key Strength | "
            "Critical Weakness | Threat Level (H/M/L)\n\n"
            "## Top 5 Macro Trends\n"
            "  For each: Trend Name | Description | Strategic Implication for CodeSentinel AI\n\n"
            "## Top 3 Target Segments\n"
            "  For each: Segment Name | Firmographics | Attractiveness Score (1–10) | Rationale\n\n"
            "## 3 Blue Ocean Opportunities\n"
            "  For each: Gap Description | Why Underserved | CodeSentinel AI's Unique Advantage\n\n"
            "## 3 GTM Strategic Recommendations\n"
            "  Specific, actionable, each tied to a finding above.\n\n"
            "Total length: 900–1200 words of substantive, evidence-based analysis."
        ),
        agent=market_analyst,
    )

    # ──────────────────────────────────────────────────────────────────────────
    #  TASK 2: ICP Development
    #  Agent    : persona_expert
    #  Context  : market_research_task (receives market report as input)
    #  Output   : Passes to Task 3
    # ──────────────────────────────────────────────────────────────────────────
    persona_development_task = Task(
        description=(
            "You have been handed a Market Intelligence Report (see context). "
            "Using those findings — especially the target segments, competitive "
            "landscape, and Blue Ocean opportunities — develop 3 detailed Ideal "
            "Customer Profiles (ICPs) for CodeSentinel AI.\n\n"

            "Apply the Pain Hierarchy Framework to each ICP, mapping their pain "
            "across three dimensions:\n"
            "  • Functional: What concrete workflows or outcomes are broken?\n"
            "  • Emotional : How does the problem make them *feel*?\n"
            "  • Social    : How does it affect their standing with peers / leadership?\n\n"

            "──────────────────────────────────────────────────────────\n"
            "ICP #1: The Enterprise Engineering Director\n"
            "──────────────────────────────────────────────────────────\n"
            "• Director of Engineering or VP Engineering at a company with 150–600 developers\n"
            "• Responsible for engineering quality, sprint velocity, security posture, "
            "and compliance (SOC 2, ISO 27001)\n"
            "• Part of a buying committee — not the sole decision-maker\n"
            "• Focus: What code-quality failures make them look incompetent to their CTO?\n\n"

            "──────────────────────────────────────────────────────────\n"
            "ICP #2: The Hypergrowth Startup CTO\n"
            "──────────────────────────────────────────────────────────\n"
            "• Technical co-founder or first CTO at a Series A/B startup (15–80 engineers)\n"
            "• Owns both technical vision AND team health — constantly managing "
            "the velocity-vs-quality trade-off under investor pressure\n"
            "• Often the sole decision-maker for tools under $2k/month\n"
            "• Focus: The existential technical-debt anxiety that keeps them awake\n\n"

            "──────────────────────────────────────────────────────────\n"
            "ICP #3: The Senior / Staff Software Engineer\n"
            "──────────────────────────────────────────────────────────\n"
            "• End-user AND internal champion who can accelerate or permanently block adoption\n"
            "• Deep, opinionated standards about tool quality; instinctively skeptical of "
            "AI 'magic' that can't explain itself\n"
            "• Influences procurement through bottom-up advocacy or quiet sabotage\n"
            "• Focus: What daily code-review friction do they desperately want eliminated?\n\n"

            "FOR EACH ICP, PROVIDE ALL OF THE FOLLOWING:\n"
            "1. Demographic & Firmographic Snapshot (age range, experience, company type)\n"
            "2. Day-in-the-Life Narrative (150–200 words, present tense, immersive)\n"
            "3. Pain Hierarchy Table (5 pains, each tagged functional/emotional/social, "
            "   with an intensity score 1–10)\n"
            "4. Top 3 Buying Triggers (specific events that create urgency to buy *now*)\n"
            "5. Top 3 Buying Blockers (objections that stall or kill the deal)\n"
            "6. Content Preferences (channels, formats, trusted sources)\n"
            "7. Golden Quote (one sentence in their exact voice capturing their core pain)"
        ),
        expected_output=(
            "Three richly detailed ICP profiles in markdown format.\n\n"
            "Required structure for each ICP:\n\n"
            "### ICP #[N]: [Persona Name & Title]\n\n"
            "**Demographic Snapshot**\n"
            "[Age range, years of experience, company type & size, location profile]\n\n"
            "**Day in the Life**\n"
            "[150–200 word immersive narrative in present tense]\n\n"
            "**Pain Hierarchy Analysis**\n"
            "| # | Pain Point | Dimension | Intensity (1–10) |\n"
            "|---|-----------|-----------|------------------|\n"
            "[5 rows]\n\n"
            "**Buying Triggers** (3 specific events)\n\n"
            "**Buying Blockers** (3 specific objections)\n\n"
            "**Content Preferences**\n"
            "[Channels, formats, and topics they actively trust]\n\n"
            "**Golden Quote**\n"
            "> \"[Their core pain in their own authentic voice]\"\n\n"
            "Total: 1,000–1,500 words across all three profiles."
        ),
        agent=persona_expert,
        context=[market_research_task],
    )

    # ──────────────────────────────────────────────────────────────────────────
    #  TASK 3: Content Strategy Blueprint
    #  Agent    : strategy_architect
    #  Context  : market_research_task + persona_development_task
    #  Output   : Passes to Task 4
    # ──────────────────────────────────────────────────────────────────────────
    strategy_planning_task = Task(
        description=(
            "You have been handed a Market Intelligence Report AND three ICP profiles "
            "(see context). Using both documents — grounding every decision in specific "
            "findings, not generic best practices — design CodeSentinel AI's "
            "90-Day Content Strategy Blueprint.\n\n"

            "The strategy must answer: what do we publish, for whom, where, "
            "how often, and how do we know if it's working?\n\n"

            "──────────────────────────────────────────────────────────\n"
            "REQUIRED STRATEGY COMPONENTS\n"
            "──────────────────────────────────────────────────────────\n\n"

            "**1. Content Mission Statement**\n"
            "A single, memorable sentence (≤25 words) that defines what CodeSentinel "
            "AI's content stands for, who it serves, and what it commits to deliver.\n\n"

            "**2. Four Content Pillars**\n"
            "Each pillar must map to a specific ICP pain or market gap identified above.\n"
            "For each: Pillar Name | Strategic Rationale | Example Content Formats | "
            "Target ICP | Primary KPI.\n\n"

            "**3. Channel Strategy Matrix**\n"
            "Channels to address: Technical Blog/SEO, LinkedIn, Hacker News / Dev.to, "
            "Email Nurture, GitHub Community / Developer Forums.\n"
            "For each channel: Budget Allocation % | Target ICP | Content Type | "
            "Posting Frequency | Primary KPI.\n\n"

            "**4. Month 1 Editorial Calendar (Weeks 1–4)**\n"
            "Month 1 theme: 'Establishing Credibility and Demonstrating Expertise'\n"
            "Provide 3 specific content pieces per week (12 total).\n"
            "For each piece: Content Title / Angle | Format | Target ICP | "
            "Content Pillar | Distribution Channel.\n\n"

            "**5. Months 2–3 Theme Overview**\n"
            "High-level themes only: Month 2 (Engagement & Community) and "
            "Month 3 (Conversion & Pipeline).\n\n"

            "**6. Measurement Framework**\n"
            "5 KPIs with 30-day / 60-day / 90-day targets and the tool/method "
            "for measuring each.\n\n"

            "**7. Content Differentiation Manifesto**\n"
            "3–5 specific ways CodeSentinel AI's content voice, format, and topics "
            "will be *distinctly different* from competitors such as Snyk and SonarQube.\n\n"

            "**8. Three Quick Win Content Assets**\n"
            "Content pieces creatable within 2 weeks that are likely to generate "
            "immediate traction. For each: Asset Description | Why It Will Generate "
            "Traction | Estimated Production Time."
        ),
        expected_output=(
            "A 90-Day Content Strategy Blueprint in clean markdown format:\n\n"
            "### Content Mission Statement\n"
            "[Single memorable sentence ≤25 words]\n\n"
            "### Content Pillars (4)\n"
            "| Pillar | Rationale | Formats | Target ICP | KPI |\n"
            "|--------|-----------|---------|------------|-----|\n\n"
            "### Channel Strategy Matrix\n"
            "| Channel | Allocation % | Target ICP | Content Type | Frequency | KPI |\n"
            "|---------|-------------|------------|-------------|-----------|-----|\n\n"
            "### Month 1 Editorial Calendar\n"
            "| Week | Content Title / Angle | Format | ICP | Pillar | Channel |\n"
            "|------|----------------------|--------|-----|--------|--------|\n"
            "[12 rows, 3 per week]\n\n"
            "### Months 2–3 Theme Overview\n"
            "[Brief thematic overview for each month]\n\n"
            "### Measurement Framework\n"
            "| KPI | Measurement Tool | 30-Day Target | 60-Day Target | 90-Day Target |\n"
            "|-----|-----------------|--------------|--------------|---------------|\n\n"
            "### Content Differentiation Manifesto\n"
            "[3–5 numbered points of specific differentiation]\n\n"
            "### Three Quick Win Content Assets\n"
            "[Each: Asset | Why It Works | Est. Time]\n\n"
            "Total: 1,000–1,500 words of specific, actionable strategy."
        ),
        agent=strategy_architect,
        context=[market_research_task, persona_development_task],
    )

    # ──────────────────────────────────────────────────────────────────────────
    #  TASK 4: Content Asset Production
    #  Agent    : content_director
    #  Context  : strategy_planning_task (receives the full strategy blueprint)
    #  Output   : Final deliverable — production-ready content assets
    # ──────────────────────────────────────────────────────────────────────────
    content_creation_task = Task(
        description=(
            "You have been handed the 90-Day Content Strategy Blueprint (see context). "
            "Your job is to *execute* — not to plan. Produce the following three asset "
            "packages, drawing directly on the ICP pain points, content pillars, and "
            "Quick Win opportunities specified in the strategy. Every word must serve "
            "the strategy. Zero generic filler.\n\n"

            "════════════════════════════════════════\n"
            "ASSET PACKAGE 1: Flagship Blog Post\n"
            "════════════════════════════════════════\n"
            "Choose the highest-impact topic from the Quick Win list or Week 1 calendar.\n\n"
            "Deliverables:\n"
            "• Three headline options (different emotional angles: curiosity / benefit / "
            "  controversy). Label them Option A, B, C.\n"
            "• Complete blog post: 600–800 words\n"
            "  - Hook: addresses a specific ICP pain in the first 40 words\n"
            "  - Structure: 4–5 sections with punchy, descriptive subheadings\n"
            "  - Data: 2–3 specific statistics or credible data points woven naturally\n"
            "  - Voice: 'brilliant friend' — authoritative but conversational, never corporate\n"
            "  - CTA: natural, non-aggressive, leads logically to CodeSentinel AI\n"
            "• Meta description (≤155 characters)\n"
            "• Three social sharing captions (one each for LinkedIn, Twitter/X, "
            "  Hacker News show post)\n\n"

            "════════════════════════════════════════\n"
            "ASSET PACKAGE 2: LinkedIn Thought Leadership Series\n"
            "════════════════════════════════════════\n"
            "Write two distinct, publication-ready LinkedIn posts:\n\n"
            "Post A — 'The Counter-Intuitive Take' (150–250 words)\n"
            "A genuinely provocative perspective on AI code review that challenges "
            "conventional wisdom. Must spark respectful debate. End with a specific "
            "engagement question that invites comments from the target ICP.\n\n"
            "Post B — 'The Wisdom Post' (150–250 words)\n"
            "A 'What nobody tells you about...' or 'After [N] code reviews, here's "
            "what I learned...' format aimed at Engineering Directors and CTOs. "
            "Authoritative, personal-feeling, with a genuine insight they haven't "
            "heard before. End with a question that invites others to share their experience.\n\n"

            "════════════════════════════════════════\n"
            "ASSET PACKAGE 3: Welcome Email Nurture Sequence (3 emails)\n"
            "════════════════════════════════════════\n"
            "A three-email sequence for new CodeSentinel AI trial users.\n\n"
            "Email 1 — Sent immediately at signup (Day 0)\n"
            "Purpose: Welcome, set clear expectations, celebrate their decision, "
            "guide them to their first meaningful win inside the product.\n"
            "Length: 150–200 words. Warm, human, energizing.\n\n"
            "Email 2 — Sent 48 hours after signup (Day 2)\n"
            "Purpose: Deliver a specific, surprising insight about how top engineering "
            "teams use the tool differently. Include one fictional-but-plausible "
            "customer example (use a generic 'a fintech team we work with...' framing). "
            "Highlight the one feature most trial users overlook.\n"
            "Length: 150–200 words.\n\n"
            "Email 3 — Sent 5 days after signup (Day 5)\n"
            "Purpose: Mini case study teaser (fictional), soft upgrade prompt "
            "(benefit-led, never pushy), and a genuine offer of human support.\n"
            "Length: 150–200 words.\n\n"
            "For ALL three emails provide:\n"
            "  Subject line | Preview text | Body | CTA button text"
        ),
        expected_output=(
            "Three complete, production-ready content asset packages in clean markdown.\n\n"
            "═══════════════════════════════════\n"
            "## PACKAGE 1: Flagship Blog Post\n"
            "═══════════════════════════════════\n\n"
            "**Headline Options**\n"
            "- Option A (Curiosity): ...\n"
            "- Option B (Benefit): ...\n"
            "- Option C (Controversy): ...\n\n"
            "**Full Blog Post** (~700 words)\n"
            "[Complete post with hook, 4–5 sections, subheadings, data, and CTA]\n\n"
            "**Meta Description** (≤155 chars)\n"
            "[...]\n\n"
            "**Social Sharing Captions**\n"
            "- LinkedIn: [...]\n"
            "- Twitter/X: [...]\n"
            "- Hacker News Show HN: [...]\n\n"
            "═══════════════════════════════════\n"
            "## PACKAGE 2: LinkedIn Series\n"
            "═══════════════════════════════════\n\n"
            "**Post A — Counter-Intuitive Take** (150–250 words)\n"
            "[Full post text]\n\n"
            "**Post B — Wisdom Post** (150–250 words)\n"
            "[Full post text]\n\n"
            "═══════════════════════════════════\n"
            "## PACKAGE 3: Welcome Email Sequence\n"
            "═══════════════════════════════════\n\n"
            "**Email 1 — Day 0 (Immediate)**\n"
            "Subject: [...] | Preview: [...]\n"
            "Body: [...]\n"
            "CTA: [...]\n\n"
            "**Email 2 — Day 2**\n"
            "Subject: [...] | Preview: [...]\n"
            "Body: [...]\n"
            "CTA: [...]\n\n"
            "**Email 3 — Day 5**\n"
            "Subject: [...] | Preview: [...]\n"
            "Body: [...]\n"
            "CTA: [...]\n\n"
            "All content formatted in clean markdown. Total: 2,000–2,500 words."
        ),
        agent=content_director,
        context=[strategy_planning_task],
    )

    return [
        market_research_task,
        persona_development_task,
        strategy_planning_task,
        content_creation_task,
    ]


# ════════════════════════════════════════════════════════════════════════════════
#  SECTION 3: CREW ASSEMBLY
# ════════════════════════════════════════════════════════════════════════════════

def assemble_crew(agents: list, tasks: list) -> Crew:
    """Assemble the sequential CrewAI pipeline."""
    return Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,   # Each task runs in order; outputs chain as context
        verbose=True,                 # Prints each agent's reasoning steps to console
    )


# ════════════════════════════════════════════════════════════════════════════════
#  SECTION 4: MAIN ENTRY POINT
# ════════════════════════════════════════════════════════════════════════════════

def main():
    """Run the full multi-agent pipeline and persist output to disk."""

    print("═" * 78)
    print("  CodeSentinel AI — Autonomous Market Intelligence & Content Strategy")
    print("  Course: Agent Orchestration | Assignment 05 | Dr. Yoram Segel")
    print("  Group Code: biu-he01 | Date: 2026-06-16")
    print("═" * 78)
    print()

    # ── Validate environment ──────────────────────────────────────────────────
    if not os.getenv("GROQ_API_KEY"):
        print("  ERROR: GROQ_API_KEY is not set.")
        print("  → Open .env and add:  GROQ_API_KEY=gsk_...")
        print("  → Get a key at: https://console.groq.com/keys")
        print("  → Then re-run: python main.py")
        sys.exit(1)

    print("  Environment: OK")
    print(f"  Model: {os.getenv('GROQ_MODEL', 'groq/llama-3.3-70b-versatile')}")
    print("  Initializing agents and task pipeline...")
    print()

    # ── Build and assemble ────────────────────────────────────────────────────
    llm    = get_llm()
    agents = build_agents(llm)
    tasks  = build_tasks(agents)
    crew   = assemble_crew(agents, tasks)

    agent_names = [a.role.split(" — ")[-1] if " — " in a.role else a.role for a in agents]
    print(f"  Pipeline: {len(agents)} agents | {len(tasks)} tasks | Sequential process")
    print(f"  Agents  : {' → '.join(['Agent '+str(i+1) for i in range(len(agents))])}")
    print()
    print("═" * 78)
    print("  STARTING PIPELINE EXECUTION")
    print("═" * 78)
    print()

    # ── Execute ───────────────────────────────────────────────────────────────
    start_time = datetime.now()
    result = crew.kickoff()
    elapsed = datetime.now() - start_time

    # ── Print final result ────────────────────────────────────────────────────
    print()
    print("═" * 78)
    print(f"  PIPELINE COMPLETE — Elapsed: {elapsed}")
    print("═" * 78)
    print()
    print("FINAL OUTPUT (Task 4 — Content Asset Packages):")
    print("─" * 78)
    print(result)
    print("─" * 78)

    # ── Persist output to file ────────────────────────────────────────────────
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"final_report_{timestamp}.md")

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write("# CodeSentinel AI — Full Pipeline Output\n\n")
        fh.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
        fh.write("**Group:** biu-he01 | **Assignment:** 05  \n\n")
        fh.write("---\n\n")
        fh.write(str(result))

    print()
    print(f"  Full output saved → {output_path}")
    print("═" * 78)

    return result


if __name__ == "__main__":
    main()
