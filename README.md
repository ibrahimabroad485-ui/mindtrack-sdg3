<div align="center">

# 🧠 MindTrack

https://github.com/user-attachments/assets/436241b1-aba6-4341-9ff0-28288536519b

### A daily mood, sleep & exercise tracker that turns raw logs into real insight

![Python](https://img.shields.io/badge/PYTHON-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/FLASK-3.0-black?style=for-the-badge&logo=flask&logoColor=white)
![Pandas](https://img.shields.io/badge/PANDAS-DATA%20ANALYSIS-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/MATPLOTLIB-CHARTS-11557C?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLITE-DATABASE-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Gunicorn](https://img.shields.io/badge/GUNICORN-WSGI%20SERVER-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
![Render](https://img.shields.io/badge/DEPLOYED%20ON-RENDER-46E3B7?style=for-the-badge&logo=render&logoColor=white)

![Status](https://img.shields.io/badge/Status-Live%20Demo-brightgreen?style=flat-square)
![SDG](https://img.shields.io/badge/UN%20SDG-3%20Good%20Health%20%26%20Well--being-orange?style=flat-square)
![Hackathon](https://img.shields.io/badge/Built%20for-README%20Generation%20Hackathon-purple?style=flat-square)

### 🔗 [**Try the live demo →**](https://mindtrack-842d.onrender.com)

*Hosted on Render's free tier — first load after inactivity may take ~30 seconds to wake up. This is a public demo, not a personal wellness log — please don't enter real personal data.*

</div>

---

## ❓ The Problem

> "People have a *sense* that sleep and exercise affect their mood, but no easy way to actually see it."

Most mood-tracking apps either demand a wearable or bury you in features you'll abandon by day three. MindTrack strips it down to what actually matters: **a 60-second daily check-in**, and a dashboard that answers the one question people actually want answered — *what's affecting my mood?*

Built around **UN Sustainable Development Goal 3 (Good Health & Well-being)**, MindTrack takes raw daily entries and turns them into rolling trends, a logging streak, and a plain-language insight generated from your own data.

## 🎯 What is "SDG 3," and why is it in the repo name?

The UN's **Sustainable Development Goals** are 17 global targets, and **SDG 3 is "Good Health and Well-being."** This project was built for a hackathon themed specifically around that goal — the repo is named `mindtrack-sdg3` to tag which goal it addresses, a naming convention carried over from the hackathon's submission requirements.

## 🧪 About this project

This was built during a hackathon under real time constraints. It's a **working demo**, not a production wellness app — there's no user authentication yet, data is shared/public on the live demo, and the emphasis was on shipping a clean, functional data pipeline end-to-end rather than a fully-featured product. See the Roadmap section below for what a production version would need.


---

## 📊 Dashboard Preview

<div align="center">
<img width="1789" height="1001" alt="Image" src="https://github.com/user-attachments/assets/abcbc535-d0ba-49e6-b943-be67c5752b12" />

**Your Wellness Dashboard**

| Avg Mood | Avg Sleep | Exercise Rate |
|:---:|:---:|:---:|
| **~6.45** | **~6.94 hrs** | **~63.6%** |

*"Your mood tends to be higher on days you exercise."* — generated insight

</div>

The dashboard plots daily mood against a 7-day rolling average, and lists recent entries below the chart. Numbers above are representative of the seeded demo data — see the [live demo](https://mindtrack-842d.onrender.com/dashboard) for the current state.

---

## ⚙️ How It Works

```
Log Entry (form) → SQLite (upsert by date) → Pandas (rolling avgs, streak, insight rules) → Matplotlib chart → Dashboard
```

Each entry is a row: date, mood (1–10), sleep hours, exercised (bool), notes. On every dashboard load, all entries load into a Pandas DataFrame, get sorted by date, and are enriched with 7-day rolling averages for mood and sleep. A small rule-based function compares mood on exercise days vs. rest days, checks average sleep against a threshold, and returns whichever observation is most relevant — no black box, no ML model, just readable logic over your own numbers.

---

## 🚀 From Localhost to Live: How This Got Deployed

Documenting this because the deployment process taught me more than the original build did. A few real problems came up, in order:

**1. Factory pattern vs. WSGI servers**
The app uses Flask's *application factory pattern* (`create_app()` in `app/__init__.py`) rather than a bare module-level `app` variable. That's a clean pattern for local dev (`run.py` calls `create_app()` directly), but production WSGI servers like Gunicorn expect to *import* a plain `app` object — they can't call a factory function themselves. Fix: added a small `wsgi.py` at the project root:

```python
from app import create_app
app = create_app()
```

Start command on Render: `gunicorn wsgi:app` (not `gunicorn app:app`, which was the platform's incorrect autofill guess).

**2. Keeping the database out of version control**
`mindtrack.db` is a local SQLite file — not something that belongs in a public GitHub repo, since it would expose real logged data and generate noisy binary diffs on every commit. It's gitignored, and instead:

```
Build Command: pip install -r requirements.txt && python data/seed.py
```

This regenerates fresh demo data on every deploy, so the live app always opens to a populated dashboard instead of a blank one — without any personal data ever touching GitHub.

**3. Render's free-tier cold starts**
Free web services on Render spin down after ~15 minutes of no traffic. The next visitor triggers a "cold start" — the container has to boot back up, which can take 30–60 seconds and occasionally shows a 404 on the very first request before the app finishes starting. Rather than pay for an always-on instance for a demo project, I set up a free [UptimeRobot](https://uptimerobot.com) monitor that pings the live URL every 5 minutes, which keeps Render's traffic threshold from ever going idle long enough to sleep.

---

## 🛠️ What I Actually Built

| Area | What I Did |
|---|---|
| **Backend** | Built the app in Flask — handled the form submission and page rendering |
| **Database** | Used SQLite to store entries, with rules so bad data can't be saved (e.g. mood must be 1–10) |
| **Data Analysis** | Used Pandas to calculate rolling averages and detect logging streaks from raw entries |
| **Charts** | Generated the mood trend chart with Matplotlib and embedded it directly in the page |
| **Deployment** | Deployed the live app on Render, using Gunicorn to serve it in production |
| **Reliability** | Set up automatic uptime monitoring so the live demo doesn't fall asleep between visits |

---

## 📦 Project Structure

```
mindtrack-sdg3/
├── assets/
│   ├── vid.mov
│   ├── image-1.png
│   └── image-2.png
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── db.py
│   ├── analytics.py
│   ├── charts.py
│   ├── static/css/
│   │   └── style.css
│   └── templates/
│       ├── base.html
│       ├── index.html
│       └── dashboard.html
├── data/
│   ├── mindtrack.db
│   └── seed.py
├── wsgi.py
├── run.py
├── requirements.txt
└── .gitignore
```

---

## 🚀 Getting Started Locally

**Requirements:** Python 3.10+

```bash
git clone https://github.com/ibrahimabroad485-ui/mindtrack-sdg3.git
cd mindtrack-sdg3

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt

python data/seed.py           # optional — populates a demo-ready dashboard

python run.py
```

Then open **http://127.0.0.1:5000**

- `/` — log today's entry
- `/dashboard` — view trends, stats, and insights

---

## 🗄️ Database Schema

```sql
CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_date TEXT NOT NULL UNIQUE,
    mood INTEGER NOT NULL CHECK (mood BETWEEN 1 AND 10),
    sleep_hours REAL NOT NULL,
    exercised INTEGER NOT NULL CHECK (exercised IN (0, 1)),
    notes TEXT
);
```

`entry_date` is unique — logging again on the same day updates that entry instead of duplicating it.

---

## 📋 Project Deliverables

| Deliverable | Description | Link |
|---|---|---|
| 🌐 Live Demo | Deployed Flask app on Render | [mindtrack-842d.onrender.com](https://mindtrack-842d.onrender.com) |
| 🖥️ Flask App | Full log-entry + dashboard application | `app/` |
| 🗄️ SQLite Schema | Constrained schema with upsert logic | `app/db.py` |
| 📈 Analytics Layer | Rolling averages, streaks, rule-based insights | `app/analytics.py` |
| 📊 Chart Rendering | Server-side Matplotlib, base64-embedded | `app/charts.py` |
| 🌱 Seed Script | Generates demo data on every deploy | `data/seed.py` |
| ⚙️ WSGI Entry Point | Production server configuration | `wsgi.py` |

---

## 🔭 Roadmap

What a production version of this would need:

- User authentication and per-user data isolation
- Export entries to CSV
- Weekly digest / email summary
- Weekday vs. weekend pattern insights
- Persistent (non-ephemeral) storage on the hosting side

---

## ⚠️ Disclaimer

MindTrack is a self-reflection and habit-tracking tool. Its insights are simple rule-based observations over your own logged data — **not medical or psychological advice, and not a diagnostic tool.** If you're struggling with your mental health, please reach out to a qualified professional or a crisis line in your area.

---

<div align="center">

**Ibrahim Jamil**

Data Science & Computer Science · Luther College · Class of 2029

[LinkedIn]([https://linkedin.com/in/<your-linkedin>)](https://www.linkedin.com/in/ibrahim-jamil-ds/) · [GitHub](https://github.com/ibrahimabroad485-ui)

*Sophomore targeting a Data Analytics Internship — Summer 2027*

---

Built for the **README Generation Hackathon** — themed around UN SDG 3 (Good Health & Well-being).
This documentation covers the build, the deployment process, and the live demo.

</div>
