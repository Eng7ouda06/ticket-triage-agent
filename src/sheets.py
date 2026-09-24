import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
import json

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def get_credentials():
    # Running on Streamlit Cloud: credentials come from st.secrets
    try:
        import streamlit as st
        if "gcp_service_account" in st.secrets:
            creds_dict = dict(st.secrets["gcp_service_account"])
            return Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    except Exception:
        pass
    # Running locally: read the actual file
    return Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

def get_sheet():
    creds = get_credentials()
    client = gspread.authorize(creds)
    sheet_id = os.getenv("SHEET_ID") or __import__("streamlit").secrets.get("SHEET_ID")
    return client.open_by_key(sheet_id).sheet1
def get_new_tickets():
    """Return rows where status is empty AND the row actually has content."""
    sheet = get_sheet()
    records = sheet.get_all_records()
    new_tickets = []
    for i, row in enumerate(records, start=2):
        if not row.get("status") and (row.get("sender") or row.get("subject") or row.get("message")):
            row["_row_number"] = i
            new_tickets.append(row)
    return new_tickets

def mark_processed(row_number, status="processed"):
    sheet = get_sheet()
    status_col = sheet.find("status").col
    sheet.update_cell(row_number, status_col, status)