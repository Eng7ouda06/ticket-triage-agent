# 🎫 AI Ticket Triage Agent

An AI-powered automation agent that reads incoming support tickets, classifies them by urgency and category using an LLM, and automatically routes them — escalating urgent issues to Slack in real time. Includes a live Streamlit dashboard for monitoring.

## Features

- 📥 **Automated ingestion** — reads new tickets from a Google Sheet (easily swappable for a real inbox)
- 🤖 **LLM classification** — urgency (low/medium/high), category, and a one-line summary via Groq
- 🔀 **Smart routing** — high-urgency tickets trigger instant Slack alerts; others get tagged for review or auto-handled
- 💾 **Persistent logging** — every processed ticket is stored in SQLite
- 📊 **Live dashboard** — Streamlit UI showing metrics and ticket details in real time

## Tech Stack

Python · Groq API (LLM) · Google Sheets API · Slack Webhooks · SQLite · Streamlit

## How it works

```
Google Sheet (tickets) → LLM Classifier → Router → Slack Alert (if urgent)
                                              ↓
                                         SQLite Log → Streamlit Dashboard
```

## Setup

1. Clone the repo and create a virtual environment:
   ```
   git clone https://github.com/Eng7ouda06/ticket-triage-agent.git
   cd ticket-triage-agent
   python -m venv venv
   venv\Scripts\activate  # or source venv/bin/activate on Mac/Linux
   pip install -r requirements.txt
   ```

2. Create a `.env` file with:
   ```
   GROQ_API_KEY=your_groq_key
   SHEET_ID=your_google_sheet_id
   SLACK_WEBHOOK_URL=your_slack_webhook_url
   ```

3. Add a Google service account `credentials.json` to the project root (see [Google Sheets API docs](https://docs.gspread.org/en/latest/oauth2.html)), and share your sheet with the service account's email.

4. Run the pipeline once via CLI:
   ```
   python -m main
   ```

5. Or launch the dashboard:
   ```
   streamlit run app.py
   ```

## Project Structure

```
src/
├── sheets.py       # reads tickets from Google Sheets
├── classifier.py   # LLM-based classification
├── router.py       # routing/decision logic
├── actions.py      # Slack alerts
└── db.py           # SQLite logging
app.py              # Streamlit dashboard
main.py             # CLI pipeline runner
```

## Roadmap

- [ ] Human-in-the-loop approval before auto-actions
- [ ] Auto-reply drafting for low-urgency tickets
- [ ] Swap Google Sheet for a real email inbox (Gmail API)

---

Built by [Mahmoud](https://github.com/Eng7ouda06) as part of an AI automation portfolio project.









