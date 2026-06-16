# CodeSentinel AI
## Autonomous Market Intelligence & Content Strategy Pipeline

> **Course**: Agent Orchestration | **Assignment**: 05
> **Instructor**: Dr. Yoram Segel | **Group Code**: `biu-he01` | **Date**: 2026-06-16

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Agents](#agents)
4. [Task Pipeline](#task-pipeline)
5. [Prerequisites](#prerequisites)
6. [Installation](#installation)
7. [Configuration](#configuration)
8. [Running](#running)
9. [Expected Output](#expected-output)
10. [File Structure](#file-structure)
11. [Screenshots](#screenshots)
12. [Troubleshooting](#troubleshooting)

---

## Project Overview

A CrewAI system implementing an **autonomous pipeline** of 4 AI agents operating sequentially (Sequential Process).

**The problem this system solves:**
An AI startup in the Go-To-Market phase needs market research, customer profiles, content strategy, and content assets - tasks that normally take weeks. This system produces a complete strategic package in a single run.

**The startup:** `CodeSentinel AI` - an AI-powered automated code review platform.

**System outputs:**
- Comprehensive Market Intelligence Report (TAM/SAM/SOM, competitors, trends, opportunities)
- 3 detailed ICP Profiles with psychological analysis
- 90-Day Content Strategy Blueprint with cost-benefit analysis
- 3 Content Asset Packages (Blog, LinkedIn, Email sequence)

---

## System Architecture

```
Agent 1          Agent 2            Agent 3              Agent 4
Dr. Maya Chen -> Prof. Alex Rivera -> Marcus Thompson -> Sophia Laurent
(Market Intel)   (ICP Profiles)      (Strategy)          (Content Assets)
     |                |                   |                    |
  Task 1 --------> Task 2 ----------> Task 3 -----------> Task 4
                  [ctx: T1]         [ctx: T1+T2]         [ctx: T3]
```

**Context Chain principle:**
Each Task receives outputs from prior Tasks as context, creating **knowledge flow** between agents:
- Task 2 "knows" the market analysis findings
- Task 3 "knows" both the market and customer profiles
- Task 4 "knows" the strategy and uses it for content

---

## Agents

### Agent 1 - Dr. Maya Chen
**Role**: Senior AI Market Intelligence Analyst
**Expertise**: Blue Ocean Detection Methodology, McKinsey-style market analysis
**Personality**: Analytical, precise, data-driven
**Output**: Market Intelligence Report (~1000 words, 7 sections)

### Agent 2 - Prof. Alex Rivera
**Role**: Chief Customer Psychology Expert & ICP Architect
**Expertise**: Pain Hierarchy Framework (Functional/Emotional/Social), behavioral economics
**Personality**: Code-switching academic, obsessive about precision
**Output**: 3 ICP Profiles (~1200 words)
**Context**: Receives Agent 1 output

### Agent 3 - Marcus Thompson
**Role**: Chief Content Strategy Architect & Thought Leadership Director
**Expertise**: Content-Led Growth methodology (Stanford curriculum), Stripe/HubSpot alumni
**Personality**: ROI-obsessed, data-driven, anti-vanity-metrics
**Output**: 90-Day Strategy Blueprint (~1200 words)
**Context**: Receives Agents 1 and 2 outputs

### Agent 4 - Sophia Laurent
**Role**: Senior Creative Content Director & Conversion Copywriter
**Expertise**: Conversion copywriting, developer audience, Hacker News virality
**Personality**: "Would I stop scrolling for this?" - every sentence must earn its place
**Output**: 3 Content Asset Packages (~2200 words)
**Context**: Receives Agent 3 output

---

## Task Pipeline

| # | Task | Agent | Context | Output |
|---|------|-------|---------|--------|
| 1 | Market Intelligence Analysis | Dr. Maya Chen | - | Market Report |
| 2 | ICP Development | Prof. Alex Rivera | Task 1 | 3 ICP Profiles |
| 3 | Content Strategy Blueprint | Marcus Thompson | Tasks 1 + 2 | 90-Day Strategy |
| 4 | Content Asset Production | Sophia Laurent | Task 3 | Content Assets |

---

## Prerequisites

- Python **3.10 - 3.13**
- Groq API key (free at console.groq.com)
- Internet connection
- Minimum 4GB RAM

---

## Installation

```bash
# 1. Navigate to project directory
cd "C:\Users\USER\hadar-biu\5 עבודה"

# 2. Install dependencies
pip install -r requirements.txt
```

---

## Configuration

```bash
# 1. Copy the template file
copy .env.example .env

# 2. Open .env and add your API key:
#    GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx
```

**.env file after editing:**
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx
GROQ_MODEL=groq/llama-3.3-70b-versatile
```

---

## Running

```bash
python main.py
# or on Windows with Python 3.12:
py -3.12 main.py
```

**What happens during the run:**
1. Validates `GROQ_API_KEY`
2. Initializes 4 agents and tasks
3. Executes `crew.kickoff()` - verbose output shows reasoning steps
4. Prints final output to console
5. Saves output to `output/final_report_{timestamp}.md`

**Estimated run time**: 5-15 minutes

---

## Expected Output

### Console - Start of run
```
Starting CodeSentinel AI - Multi-Agent Pipeline...
Working Agent: Dr. Maya Chen
Starting Task: Market Intelligence Analysis...
```

### Console - End of run
```
Working Agent: Sophia Laurent
Task completed: Content Asset Production
Output saved to: output/final_report_20260616_151412.md
Pipeline complete!
```

---

## File Structure

```
עבודה 5/
├── main.py              # Main pipeline - all agents, tasks, crew
├── requirements.txt     # Python dependencies
├── .env.example         # API key template (safe to commit)
├── .env                 # Your API keys (NOT committed)
├── .gitignore           # Excludes .env from git
├── PRD.md               # Product Requirements Document
├── PLAN.md              # Architecture Plan
├── TODO.md              # Development Checklist
├── README.md            # This file
├── output/              # Generated reports (auto-created)
│   └── final_report_*.md
└── screenshots/         # Run screenshots
    └── screenshot_*.png
```

---

## Screenshots

### Screenshot 3 - Agent Pipeline Running
![Agent Pipeline](screenshots/screenshot_3_agent1.png)

### Screenshot 4 - Agent 4 Content Output
![Content Output](screenshots/screenshot_4_agent4.png)

### Screenshot 5 - Pipeline Complete
![Pipeline Complete](screenshots/screenshot_5_complete.png)

---

## Troubleshooting

### Error: `GROQ_API_KEY not found`
**Solution**: Make sure you created a `.env` file (not just `.env.example`) with your key:
```bash
copy .env.example .env
# Open .env and update: GROQ_API_KEY=gsk_...
```

### Error: `ModuleNotFoundError: No module named crewai`
**Solution**: Install dependencies in the correct Python version:
```bash
py -3.12 -m pip install -r requirements.txt
```

### Error: `RateLimitError` from Groq
**Solution**: Wait a few minutes and try again. Groq free tier has a 12,000 TPM limit.

### Run takes too long (over 30 minutes)
**Check**: The `verbose=True` setting shows activity. If terminal is frozen - check internet connection.

---

*Generated as part of Assignment 05 - Agent Orchestration Course | biu-he01*