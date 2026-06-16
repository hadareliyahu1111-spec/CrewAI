# מסמך דרישות מוצר (PRD)
## מערכת CodeSentinel AI — אורקסטרציה רב-סוכנית אוטונומית

| שדה | ערך |
|-----|-----|
| **שם הפרויקט** | CodeSentinel AI — Autonomous Market Intelligence & Content Strategy Pipeline |
| **קוד קבוצה** | biu-he01 |
| **מטלה** | 05 — CrewAI Multi-Agent Orchestration |
| **קורס** | אורקסטרציה של סוכנים |
| **מרצה** | ד"ר יורם סגל |
| **תאריך** | 16 ביוני 2026 |
| **גרסה** | 1.0.0 |

---

## 1. חזון המוצר

### 1.1 תיאור כללי
המערכת מממשת **pipeline אוטונומי מלא** המבוסס על CrewAI, המורכב מארבעה סוכני AI מתמחים הפועלים בתהליך סדרתי (Sequential Process). כל סוכן מקבל את הפלט של קודמו כהקשר (context), ומייצר פלט עשיר שמשמש את הסוכן הבא. התוצאה הסופית היא **חבילת תוכן שיווקית מלאה** עבור סטארטאפ AI בשלב Go-To-Market.

### 1.2 הגדרת הבעיה
צוותי Marketing ו-Strategy בסטארטאפים בשלב Go-To-Market נדרשים לבצע ניתוחי שוק מורכבים, לפתח פרופילי לקוחות, לעצב אסטרטגיית תוכן, וליצור נכסי תוכן — תהליך שלוקח שבועות ועולה עשרות אלפי דולרים. המערכת מייצרת את כלל הפלטים הללו בריצה אוטונומית אחת.

### 1.3 מדדי הצלחה עסקיים
- **זמן ייצור**: מ-6 שבועות לפחות מ-30 דקות (בהתאם לעומס LLM)
- **עלות**: מ-$15,000-50,000 (יועצי אסטרטגיה) לעלות API בלבד
- **איכות**: פלטים מובנים, מפורטים, ומוכנים לשימוש עיסקי

---

## 2. דרישות פונקציונליות

### 2.1 רכיב 1 — ניהול סוכנים (Agent Management)

| מזהה | דרישה | עדיפות |
|------|-------|--------|
| FR-01 | המערכת תאכלס בדיוק ארבעה (4) סוכנים מוגדרים | חובה |
| FR-02 | כל סוכן יכיל role, goal, ו-backstory עשיר (לפחות 150 מילה) | חובה |
| FR-03 | כל backstory יתפקד כ-system prompt אורגאני המעצב את אופי הסוכן | חובה |
| FR-04 | כל סוכן יהיה בעל תפקיד ייחודי ומוגדר בבירור ללא חפיפה | חובה |
| FR-05 | הסוכנים יפעלו עם `allow_delegation=False` (אין העברת משימות בין סוכנים) | חובה |
| FR-06 | הסוכנים יפעלו עם `verbose=True` להצגת שלבי החשיבה | חובה |

**הסוכנים המוגדרים:**

| # | שם הסוכן | תפקיד (role) | מיקוד |
|---|----------|--------------|-------|
| 1 | Dr. Maya Chen | Senior AI Market Intelligence Analyst | ניתוח שוק ותחרות |
| 2 | Prof. Alex Rivera | Chief Customer Psychology Expert & ICP Architect | פרופילי לקוחות |
| 3 | Marcus Thompson | Chief Content Strategy Architect | אסטרטגיית תוכן |
| 4 | Sophia Laurent | Senior Creative Content Director & Conversion Copywriter | ייצור תוכן |

### 2.2 רכיב 2 — ניהול משימות (Task Management)

| מזהה | דרישה | עדיפות |
|------|-------|--------|
| FR-07 | כל סוכן ישויך למשימה (Task) ייעודית אחת לפחות | חובה |
| FR-08 | כל Task תכיל description מפורט (לפחות 200 מילה) | חובה |
| FR-09 | כל Task תגדיר expected_output מובנה ומדויק | חובה |
| FR-10 | Tasks 2, 3, 4 יכילו את פרמטר `context` עם הפניה למשימות קודמות | חובה |
| FR-11 | פרמטר `context` ב-Task 3 יפנה לשתי משימות קודמות (Tasks 1 ו-2) | חובה |

**שרשרת ה-Context:**
```
Task 1 (Market Research)    ──→  context of Task 2
Task 1 + Task 2 (Personas)  ──→  context of Task 3
Task 3 (Strategy)           ──→  context of Task 4
```

### 2.3 רכיב 3 — ניהול ה-Crew

| מזהה | דרישה | עדיפות |
|------|-------|--------|
| FR-12 | ה-Crew יופעל עם `process=Process.sequential` | חובה |
| FR-13 | ה-Crew יופעל עם `verbose=True` | חובה |
| FR-14 | הפעלת המערכת תתבצע דרך פונקציית `main()` | חובה |
| FR-15 | הפונקציה תפעיל `crew.kickoff()` | חובה |
| FR-16 | הפונקציה תדפיס את התוצאה הסופית | חובה |
| FR-17 | הפלט הסופי יישמר לקובץ `.md` בתיקיית `output/` | מומלץ |

---

## 3. דרישות תוכן

### 3.1 Task 1 — Market Intelligence Report
**מה הסוכן חייב לייצר:**
- Executive Summary (5 נקודות)
- ניתוח גודל שוק: TAM / SAM / SOM עם הנמקה
- טבלת תחרות: 8-10 מתחרים עם פרמטרים מרכזיים
- 5 מגמות מאקרו עם השלכות אסטרטגיות
- 3 קטגוריות לקוחות מדורגות עם ציוני אטרקטיביות
- 3 הזדמנויות Blue Ocean מפורטות
- 3 המלצות GTM מעוגנות בממצאים

### 3.2 Task 2 — ICP Profiles
**מה הסוכן חייב לייצר (לכל אחד מ-3 הפרופילים):**
- Snapshot דמוגרפי ופירמוגרפי
- נרטיב "יום בחיים" (150-200 מילה, נוכח)
- טבלת Pain Hierarchy (5 כאבים, מימד, עוצמה)
- 3 Buying Triggers ספציפיים
- 3 Buying Blockers ספציפיים
- העדפות תוכן
- "ציטוט זהב" — משפט אחד בקולם

### 3.3 Task 3 — Content Strategy Blueprint
**מה הסוכן חייב לייצר:**
- Content Mission Statement (≤25 מילה)
- 4 עמודי תוכן עם רציונל, פורמטים, ICP ו-KPI
- טבלת Channel Strategy Matrix (5 ערוצים)
- לוח עריכה חודש 1 (12 פריטים, 3 לשבוע)
- סקירת נושאים חודשים 2-3
- 5 KPIs עם יעדים ל-30/60/90 יום
- Content Differentiation Manifesto (3-5 נקודות)
- 3 Quick Win Content Assets

### 3.4 Task 4 — Content Asset Packages
**מה הסוכן חייב לייצר:**

**Package 1 — Flagship Blog Post:**
- 3 אפשרויות כותרת (זוויות שונות)
- פוסט בלוג מלא (600-800 מילה)
- Meta description (≤155 תווים)
- 3 כיתובים לרשתות חברתיות

**Package 2 — LinkedIn Series:**
- פוסט A: "The Counter-Intuitive Take" (150-250 מילה)
- פוסט B: "The Wisdom Post" (150-250 מילה)

**Package 3 — Email Nurture Sequence:**
- Email 1 (Day 0): Welcome
- Email 2 (Day 2): Education + Social Proof
- Email 3 (Day 5): Case Study + Upgrade Prompt

---

## 4. דרישות טכניות

| מזהה | דרישה | פירוט |
|------|-------|-------|
| TR-01 | שפת תכנות | Python 3.10 ומעלה |
| TR-02 | Framework | CrewAI ≥ 0.51.0 |
| TR-03 | LLM Backend | OpenAI API (GPT-4o-mini כברירת מחדל) |
| TR-04 | ניהול env | python-dotenv |
| TR-05 | הפעלה | `python main.py` מתיקיית הפרויקט |
| TR-06 | הגדרות | OPENAI_API_KEY ב-.env |
| TR-07 | קידוד קבצים | UTF-8 |
| TR-08 | שמירת פלט | output/final_report_{timestamp}.md |

---

## 5. דרישות לא-פונקציונליות

| קטגוריה | דרישה |
|---------|-------|
| **קריאות קוד** | כל פונקציה מתועדת עם docstring, שמות משתנים ברורים |
| **מבנה** | הפרדה ברורה לסקציות: Agents / Tasks / Crew / Main |
| **עמידות** | בדיקת קיום OPENAI_API_KEY בהפעלה, עם הודעת שגיאה ברורה |
| **ביצועים** | max_iter=3 לכל סוכן למניעת לולאות אינסופיות |
| **פלט** | כל ריצה שומרת קובץ ייחודי עם timestamp בתיקיית output/ |

---

## 6. קריטריוני קבלה (Acceptance Criteria)

- [ ] המערכת מכילה ≥4 סוכנים, כל אחד עם role/goal/backstory מלאים
- [ ] כל Task מכיל description עשיר, expected_output מפורט, ו-context מתאים
- [ ] ה-Crew רץ עם `Process.sequential` ו-`verbose=True`
- [ ] פונקציית `main()` מפעילה `kickoff()` ומדפיסה את הפלט
- [ ] הקוד רץ בהצלחה עם OPENAI_API_KEY תקין
- [ ] הפלט הסופי נשמר לקובץ
- [ ] כל קבצי ה-Markdown קיימים ומלאים
- [ ] ה-verbose output מציג את שלבי החשיבה של כל סוכן

---

## 7. הנחות ומגבלות

- המערכת מניחה זמינות OpenAI API עם מפתח תקין
- זמן ריצה משוער: 5-15 דקות (תלוי בעומס שרתי OpenAI)
- עלות ריצה משוערת: $0.10-$0.50 עם GPT-4o-mini
- המשימות לא כוללות כלים חיצוניים (web search, file reading) — הסוכנים מסתמכים על ידע הLLM
- הפלטים הם "fictional but plausible" — לא מבוססים על data אמיתי בזמן-אמת
