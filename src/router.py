from src.actions import send_slack_alert

def route_ticket(ticket: dict, classification: dict):
    """
    Decide what to do with a classified ticket.
    Returns a status string to write back to the sheet.
    """
    urgency = classification["urgency"]

    if urgency == "high":
        send_slack_alert(ticket, classification)
        return "escalated"

    elif urgency == "medium":
        # for now, just log it as needing review
        return "needs_review"

    else:  # low
        return "auto_handled"