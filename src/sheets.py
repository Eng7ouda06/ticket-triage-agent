import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def get_sheet():
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet_id = os.getenv("SHEET_ID")
    return client.open_by_key("1EgqOx4SejzssodUfom5wNxrz6dAVcxJRMm-jlfSF5Vk").sheet1

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