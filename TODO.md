# רשימת משימות (TODO)
## CodeSentinel AI — מטלה 05

| שדה | ערך |
|-----|-----|
| **קוד קבוצה** | biu-he01 |
| **מטלה** | 05 — CrewAI Multi-Agent Orchestration |
| **עדכון אחרון** | 16 ביוני 2026 |

---

## שלב 1: הקמת הסביבה

- [x] **ENV-01** — יצירת תיקיית הפרויקט: `C:\Users\USER\hadar-biu\עבודה 5\`
- [x] **ENV-02** — יצירת תיקיית output: `output/`
- [x] **ENV-03** — יצירת קובץ `requirements.txt` עם כל התלויות
- [x] **ENV-04** — יצירת קובץ `.env.example` עם הנחיות הגדרה
- [ ] **ENV-05** — **(המשתמש)** יצירת קובץ `.env` מתוך `.env.example`
- [ ] **ENV-06** — **(המשתמש)** הזנת `OPENAI_API_KEY` חוקי בקובץ `.env`
- [ ] **ENV-07** — **(המשתמש)** התקנת תלויות: `pip install -r requirements.txt`

---

## שלב 2: פיתוח הקוד

### 2.1 הגדרת סוכנים
- [x] **AGT-01** — הגדרת Agent 1: Dr. Maya Chen (Market Intelligence Analyst)
  - [x] `role` מוגדר: "Senior AI Market Intelligence Analyst"
  - [x] `goal` מוגדר: ניתוח שוק ממוקד עם 6 יעדים ברורים
  - [x] `backstory` עשיר (200+ מילה): אישיות, מתודולוגיה, ציפיות
  - [x] `verbose=True`, `allow_delegation=False`, `max_iter=3`

- [x] **AGT-02** — הגדרת Agent 2: Prof. Alex Rivera (Customer Psychology Expert)
  - [x] `role` מוגדר: "Chief Customer Psychology Expert & ICP Architect"
  - [x] `goal` מוגדר: פיתוח 3 ICPs מבוססי Pain Hierarchy
  - [x] `backstory` עשיר (200+ מילה): Pain Hierarchy Framework, 2500 ראיונות
  - [x] `verbose=True`, `allow_delegation=False`, `max_iter=3`

- [x] **AGT-03** — הגדרת Agent 3: Marcus Thompson (Content Strategy Architect)
  - [x] `role` מוגדר: "Chief Content Strategy Architect & Thought Leadership Director"
  - [x] `goal` מוגדר: Blueprint ל-90 יום עם KPIs מדידים
  - [x] `backstory` עשיר (200+ מילה): Stripe, HubSpot, Content-Led Growth
  - [x] `verbose=True`, `allow_delegation=False`, `max_iter=3`

- [x] **AGT-04** — הגדרת Agent 4: Sophia Laurent (Creative Content Director)
  - [x] `role` מוגדר: "Senior Creative Content Director & Conversion Copywriter"
  - [x] `goal` מוגדר: 3 חבילות נכסי תוכן מוכנות לפרסום
  - [x] `backstory` עשיר (200+ מילה): Ogilvy, Hacker News, email benchmark
  - [x] `verbose=True`, `allow_delegation=False`, `max_iter=3`

### 2.2 הגדרת משימות
- [x] **TSK-01** — הגדרת Task 1: Market Intelligence
  - [x] `description` מפורט (300+ מילה, 6 סקציות)
  - [x] `expected_output` מובנה עם 7 כותרות Markdown
  - [x] `agent = market_analyst`
  - [x] `context = []` (ללא הקשר — ראשון בשרשרת)

- [x] **TSK-02** — הגדרת Task 2: ICP Development
  - [x] `description` מפורט (200+ מילה, 3 ICP profiles מוגדרים)
  - [x] `expected_output` עם מבנה טבלאי מדויק לכל פרופיל
  - [x] `agent = persona_expert`
  - [x] `context = [market_research_task]` ← תלות ב-Task 1

- [x] **TSK-03** — הגדרת Task 3: Content Strategy Blueprint
  - [x] `description` מפורט (250+ מילה, 8 רכיבים נדרשים)
  - [x] `expected_output` עם 8 סקציות Markdown מובנות
  - [x] `agent = strategy_architect`
  - [x] `context = [market_research_task, persona_development_task]` ← תלות ב-Tasks 1+2

- [x] **TSK-04** — הגדרת Task 4: Content Asset Production
  - [x] `description` מפורט (300+ מילה, 3 asset packages)
  - [x] `expected_output` עם 3 חבילות מובנות (Blog + LinkedIn + Email)
  - [x] `agent = content_director`
  - [x] `context = [strategy_planning_task]` ← תלות ב-Task 3

### 2.3 הרכבת ה-Crew
- [x] **CRW-01** — הגדרת `Crew` עם `process=Process.sequential`
- [x] **CRW-02** — הפעלת `verbose=True` על ה-Crew
- [x] **CRW-03** — רשימת `agents` נכונה (4 סוכנים בסדר נכון)
- [x] **CRW-04** — רשימת `tasks` נכונה (4 משימות בסדר ביצוע)

### 2.4 פונקציית Main
- [x] **MAN-01** — פונקציית `main()` מוגדרת
- [x] **MAN-02** — בדיקת `OPENAI_API_KEY` לפני ביצוע
- [x] **MAN-03** — קריאה ל-`crew.kickoff()`
- [x] **MAN-04** — הדפסת התוצאה הסופית לקונסול
- [x] **MAN-05** — שמירת פלט לקובץ `output/final_report_{timestamp}.md`
- [x] **MAN-06** — הודעות status ברורות לאורך הריצה
- [x] **MAN-07** — Guard `if __name__ == "__main__": main()`

---

## שלב 3: תיעוד

- [x] **DOC-01** — יצירת `PRD.md`: מסמך דרישות מוצר מלא
- [x] **DOC-02** — יצירת `PLAN.md`: תוכנית ארכיטקטונית עם diagrams
- [x] **DOC-03** — יצירת `TODO.md`: קובץ זה
- [x] **DOC-04** — יצירת `README.md`: תיעוד מלא עם הנחיות הרצה

---

## שלב 4: בדיקות ואימות

- [ ] **TST-01** — **(המשתמש)** הרצת `python main.py` לראשונה
- [ ] **TST-02** — **(המשתמש)** אימות שה-verbose output מציג שלבי חשיבה של כל סוכן
- [ ] **TST-03** — **(המשתמש)** אימות שנוצר קובץ בתיקיית `output/`
- [ ] **TST-04** — **(המשתמש)** בדיקת איכות הפלט לכל Task
- [ ] **TST-05** — **(המשתמש)** צילום מסך של לוג ה-verbose לצורך הגשה

---

## שלב 5: הגשה

- [ ] **SUB-01** — **(המשתמש)** הוספת צילומי מסך לסקציה המיועדת ב-`README.md`
- [ ] **SUB-02** — **(המשתמש)** בדיקה סופית של כל קבצי ה-Markdown
- [ ] **SUB-03** — **(המשתמש)** הגשת הפרויקט בהתאם להנחיות המרצה
- [ ] **SUB-04** — **(המשתמש)** שמירת קובץ הפלט הסופי מהריצה המוצלחת

---

## סיכום התקדמות

| שלב | סטטוס | הערות |
|-----|-------|-------|
| שלב 1: הסביבה | ✅ הושלם (חלקית) | ENV-05 עד ENV-07 בידי המשתמש |
| שלב 2: הקוד | ✅ הושלם | כל הסוכנים, משימות, Crew, ו-main() |
| שלב 3: תיעוד | ✅ הושלם | כל קבצי ה-MD נוצרו |
| שלב 4: בדיקות | ⏳ ממתין | נדרשת הרצה בפועל ע"י המשתמש |
| שלב 5: הגשה | ⏳ ממתין | לאחר השלמת בדיקות |
