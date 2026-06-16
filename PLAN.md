# תוכנית ארכיטקטונית (PLAN)
## CodeSentinel AI — CrewAI Multi-Agent System

| שדה | ערך |
|-----|-----|
| **קוד קבוצה** | biu-he01 |
| **מטלה** | 05 |
| **תאריך** | 16 ביוני 2026 |

---

## 1. סקירה ארכיטקטונית

### 1.1 פרדיגמת האורקסטרציה

המערכת מיישמת את דפוס **Sequential Multi-Agent Pipeline** של CrewAI:

```
┌─────────────────────────────────────────────────────────────────┐
│                     CREW: CodeSentinel AI                       │
│                  process = Process.sequential                    │
│                       verbose = True                            │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────┐    ┌──────────────────────────────────────┐
│   AGENT 1        │    │  Task 1: Market Intelligence Report  │
│  Dr. Maya Chen   │───▶│  context: None (first in chain)      │
│  Market Analyst  │    │  output : Market Intelligence Report │
└──────────────────┘    └──────────────────────────────────────┘
         │                              │
         │                              │ context ↓
         ▼                              ▼
┌──────────────────┐    ┌──────────────────────────────────────┐
│   AGENT 2        │    │  Task 2: ICP Development             │
│  Prof. A. Rivera │───▶│  context: [Task 1 output]            │
│  Persona Expert  │    │  output : 3 ICP Profiles             │
└──────────────────┘    └──────────────────────────────────────┘
         │                    │              │
         │              context ↓            │ context ↓
         ▼                    ▼              ▼
┌──────────────────┐    ┌──────────────────────────────────────┐
│   AGENT 3        │    │  Task 3: Content Strategy Blueprint  │
│  Marcus Thompson │───▶│  context: [Task 1 + Task 2 outputs]  │
│  Strategy Arch.  │    │  output : 90-Day Strategy Blueprint  │
└──────────────────┘    └──────────────────────────────────────┘
         │                              │
         │                              │ context ↓
         ▼                              ▼
┌──────────────────┐    ┌──────────────────────────────────────┐
│   AGENT 4        │    │  Task 4: Content Asset Production    │
│  Sophia Laurent  │───▶│  context: [Task 3 output]            │
│  Content Director│    │  output : 3 Content Asset Packages   │
└──────────────────┘    └──────────────────────────────────────┘
                                        │
                                        ▼
                           ┌────────────────────────┐
                           │  output/final_report_  │
                           │  {timestamp}.md        │
                           └────────────────────────┘
```

### 1.2 מנגנון זרימת המידע

**מנגנון ה-Context** של CrewAI הוא הלב של האורקסטרציה:
- כל `Task` שמקבל `context=[task_object]` מקבל את פלט ה-Task הזה כחלק מה-prompt שלו
- זה מאפשר לסוכנים "לדבר" אחד עם השני מבלי לשלוח הודעות ישירות
- בתהליך Sequential, CrewAI מנהל את שרשרת הביצוע ומזרים את הפלטים אוטומטית

---

## 2. פירוט הסוכנים

### Agent 1 — Dr. Maya Chen
```
role      : "Senior AI Market Intelligence Analyst"
focus     : Market sizing, competitive analysis, trend identification
expertise : Blue Ocean methodology, GTM strategy, market segmentation
output    : Structured Market Intelligence Report (markdown, ~1000 words)
```

**עקרון עיצוב ה-Backstory:**
הבאקסטורי מתפקד כ-System Prompt. הוא מגדיר:
- **אישיות**: אנליטית, דקדקנית, מבוססת עובדות
- **מתודולוגיה**: "Blue Ocean Detection Methodology"
- **הגבלות**: "אלרגי לנחות ללא ראיות"
- **ציפיות לפלט**: "דוח שהוא גם המקיף ביותר וגם הניתן לפעולה ביותר"

### Agent 2 — Prof. Alex Rivera
```
role      : "Chief Customer Psychology Expert & ICP Architect"
focus     : Behavioral economics, customer psychology, ICP development
expertise : Pain Hierarchy Framework, buyer journey mapping
output    : 3 richly detailed ICP profiles (~1200 words)
dependency: Receives Task 1 output as context
```

**עקרון עיצוב ה-Backstory:**
- מייצב אמונה פילוסופית מנוגדת לשוק ("most companies build for the customer they imagine")
- מגדיר מסגרת ייחודית (Pain Hierarchy: Functional / Emotional / Social)
- מציב מדד ברור לאיכות: "does the persona make the PM uncomfortable?"

### Agent 3 — Marcus Thompson
```
role      : "Chief Content Strategy Architect & Thought Leadership Director"
focus     : Channel strategy, editorial planning, content ROI
expertise : Content-Led Growth methodology, developer content, pipeline metrics
output    : 90-Day Content Strategy Blueprint (~1200 words)
dependency: Receives Tasks 1 + 2 outputs as context
```

**עקרון עיצוב ה-Backstory:**
- קרדיטים קונקרטיים ומדידים (Stripe: 3M readers; HubSpot: $240M pipeline)
- זהות סטנצה ברורה: "fierce opponent of content for content's sake"
- ציפיות מובנות: "refuses to write strategy that cannot be measured"

### Agent 4 — Sophia Laurent
```
role      : "Senior Creative Content Director & Conversion Copywriter"
focus     : Blog posts, LinkedIn content, email sequences
expertise : Conversion copywriting, developer audience, Hacker News virality
output    : 3 content asset packages (~2200 words)
dependency: Receives Task 3 output as context
```

**עקרון עיצוב ה-Backstory:**
- מגדיר ה-"Voice" האוטנטי: "brilliant friend, not a marketing team"
- מציב מחסום איכות: "Would I stop scrolling for this?"
- מכמת הצלחות: "9 Hacker News front page hits", "3.4x email open rate"

---

## 3. פירוט המשימות

### Task 1 — Market Intelligence Analysis

| פרמטר | ערך |
|-------|-----|
| `agent` | `market_analyst` |
| `context` | `[]` (ריק — ראשון בשרשרת) |
| `max_iter` | 3 |
| **מבנה description** | 6 סקציות ממוספרות, כל אחת עם הנחיות ספציפיות |
| **מבנה expected_output** | 7 כותרות markdown מפורטות עם הנחיות תוכן |

**סיבת עיצוב**: description מפורט מאוד עם 6 סקציות מובנות מונע "hallucination drift" — הסוכן לא יכול "להחליט" לדלג על סקציה.

### Task 2 — ICP Development

| פרמטר | ערך |
|-------|-----|
| `agent` | `persona_expert` |
| `context` | `[market_research_task]` |
| **קשר לקודם** | משתמש במידע על Segments ו-Blue Ocean מ-Task 1 |

**סיבת עיצוב**: ה-context מבטיח שה-ICPs לא נבנים בחלל ריק — הם מעוגנים בממצאי השוק.

### Task 3 — Content Strategy Blueprint

| פרמטר | ערך |
|-------|-----|
| `agent` | `strategy_architect` |
| `context` | `[market_research_task, persona_development_task]` |
| **קשר לקודם** | כל עמוד תוכן חייב למפות לכאב ICP ספציפי |

**סיבת עיצוב**: הסוכן מקבל שני מקורות מידע — שוק ולקוחות — ועליו לסנתז שניהם לאסטרטגיה.

### Task 4 — Content Asset Production

| פרמטר | ערך |
|-------|-----|
| `agent` | `content_director` |
| `context` | `[strategy_planning_task]` |
| **קשר לקודם** | נכסי התוכן חייבים לממש את ה-Quick Wins ו-Week 1 מ-Task 3 |

**סיבת עיצוב**: הסוכן מקבל רק את האסטרטגיה (לא את ניתוח השוק הגולמי) — זה מייצר תוכן ממוקד ולא "שופך" מידע מחקר לתוך הכתיבה.

---

## 4. הרציונל הארכיטקטוני

### מדוע Sequential (ולא Hierarchical)?

| קריטריון | Sequential | Hierarchical |
|----------|-----------|-------------|
| **תלויות ברורות** | ✅ כל שלב תלוי בקודמו | ❌ Manager יכול לחלק בכל סדר |
| **שליטה על הזרימה** | ✅ גבוהה — ניתן לעקוב בדיוק | ❌ לפעמים Manager מחליט אחרת |
| **הוכחת קשרים** | ✅ context chains גלויים בקוד | ❌ המנגנון אוטומטי ופחות גלוי |
| **מתאים לפרויקט** | ✅ כל שלב *חייב* את כל קודמיו | ❌ הייררכי מתאים כשניתן לפרלל |

### מדוע `allow_delegation=False`?
בתהליך Sequential, האורקסטרציה מנוהלת ע"י Crew ולא ע"י הסוכנים עצמם. delegation מיותר וגורם לתוצאות בלתי-צפויות.

### מדוע `max_iter=3`?
בלי הגבלה, סוכנים יכולים להיכנס ללולאות "חשיבה" ארוכות. `max_iter=3` מגביל לשלושה מחזורי reasoning, מספיק לתוצאה איכותית מבלי לבזבז tokens.

---

## 5. מבנה הקבצים

```
עבודה 5/
├── main.py            ← ← ← נקודת כניסה ראשית (ALL logic here)
│                             Agents → Tasks → Crew → kickoff()
├── requirements.txt   ← תלויות Python
├── .env.example       ← תבנית משתני סביבה
├── .env               ← (נוצר ע"י המשתמש, לא בגיט)
├── output/            ← (נוצר אוטומטית בריצה)
│   └── final_report_{timestamp}.md
├── PRD.md             ← מסמך דרישות מוצר
├── PLAN.md            ← קובץ זה
├── TODO.md            ← רשימת משימות
└── README.md          ← תיעוד מלא עם הנחיות הרצה
```

**עיצוב של קובץ יחיד (`main.py`):**
הבחירה לאחד הכל לקובץ אחד היא מכוונת — עבור מטלת קורס, ריכוז הלוגיקה ב-`main.py` מאפשר קריאה ליניארית מלמעלה למטה שמשקפת ישירות את מושגי הקורס (agents → tasks → crew).

---

## 6. תרשים זרימת הנתונים

```
INPUT
  └── OPENAI_API_KEY (env)
  └── STARTUP_CONTEXT (hardcoded string in main.py)
        │
        ▼
AGENT 1 receives: STARTUP_CONTEXT
AGENT 1 produces: Market Report (TAM/SAM/SOM, competition, trends, segments, blue ocean, GTM)
        │
        ▼
AGENT 2 receives: Market Report [via context]
AGENT 2 produces: 3 ICP Profiles (demographics, pain hierarchy, triggers, blockers)
        │
        ▼
AGENT 3 receives: Market Report + ICP Profiles [via context]
AGENT 3 produces: 90-Day Strategy Blueprint (pillars, channels, calendar, KPIs)
        │
        ▼
AGENT 4 receives: Strategy Blueprint [via context]
AGENT 4 produces: Content Asset Packages (blog post, LinkedIn posts, email sequence)
        │
        ▼
OUTPUT
  └── Printed to console
  └── Saved to output/final_report_{timestamp}.md
```

---

## 7. הנחיות פיתוח עתידי

| שיפור | תיאור | מורכבות |
|-------|-------|---------|
| Add Tools | הוספת `SerperDevTool` לסוכן 1 לחיפוש מחקר אמיתי | בינונית |
| Human-in-loop | הוספת `human_input=True` בין Tasks לאישור ביניים | נמוכה |
| Output Parsing | שימוש ב-`output_pydantic` לניתוח פלט מובנה | גבוהה |
| Parallel Sub-tasks | פיצול Task 2 ל-3 sub-agents מקבילים (אחד לכל ICP) | גבוהה |
| Memory | הפעלת `memory=True` ב-Crew לזיכרון בין ריצות | נמוכה |
