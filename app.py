import streamlit as st
from src.db import init_db, get_all_logged_tickets
from src.sheets import get_new_tickets, mark_processed
from src.classifier import classify_ticket
from src.router import route_ticket
from src.db import log_ticket

st.set_page_config(page_title="Ticket Triage Agent", layout="wide")

init_db()

st.title("🎫 AI Ticket Triage Agent")
st.caption("Automatically classifies and routes incoming support tickets.")

# --- Run pipeline button ---
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🔄 Check for new tickets"):
        with st.spinner("Fetching and classifying new tickets..."):
            tickets = get_new_tickets()
            for ticket in tickets:
                classification = classify_ticket(ticket["subject"], ticket["message"])
                status = route_ticket(ticket, classification)
                mark_processed(ticket["_row_number"], status)
                log_ticket(ticket, classification, status)
        st.success(f"Processed {len(tickets)} new ticket(s).")

st.divider()

# --- Metrics ---
all_tickets = get_all_logged_tickets()
total = len(all_tickets)
escalated = sum(1 for t in all_tickets if t["status"] == "escalated")
auto_handled = sum(1 for t in all_tickets if t["status"] == "auto_handled")
needs_review = sum(1 for t in all_tickets if t["status"] == "needs_review")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Processed", total)
m2.metric("🚨 Escalated", escalated)
m3.metric("👀 Needs Review", needs_review)
m4.metric("✅ Auto-Handled", auto_handled)

st.divider()

# --- Ticket table ---
st.subheader("Processed Tickets")

if not all_tickets:
    st.info("No tickets processed yet. Click 'Check for new tickets' above.")
else:
    for t in all_tickets:
        urgency_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(t["urgency"], "⚪")
        with st.expander(f"{urgency_color} {t['subject'] or '(no subject)'} — {t['sender']}"):
            st.write(f"**Category:** {t['category']}")
            st.write(f"**Urgency:** {t['urgency']}")
            st.write(f"**Status:** {t['status']}")
            st.write(f"**Summary:** {t['summary']}")
            st.write(f"**Message:** {t['message']}")
            st.caption(f"Processed at {t['processed_at']}")