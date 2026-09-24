from src.sheets import get_new_tickets, mark_processed
from src.classifier import classify_ticket
from src.router import route_ticket
from src.db import init_db, log_ticket

def run_pipeline():
    init_db()  # creates the table if it doesn't exist yet
    tickets = get_new_tickets()
    print(f"Found {len(tickets)} new ticket(s).")

    for ticket in tickets:
        classification = classify_ticket(ticket["subject"], ticket["message"])
        status = route_ticket(ticket, classification)
        mark_processed(ticket["_row_number"], status)
        log_ticket(ticket, classification, status)
        print(f"Processed: {ticket['subject']} -> {status} ({classification})")

if __name__ == "__main__":
    run_pipeline()