import json
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a support ticket classifier. Given a ticket's subject and message,
respond with ONLY a JSON object, no other text, in this exact format:

{
  "urgency": "low" | "medium" | "high",
  "category": "billing" | "technical" | "general",
  "summary": "one short sentence summarizing the issue"
}

Rules:
- "high" urgency = account access, payment failures, security issues, angry/urgent tone
- "medium" urgency = broken features, refund requests
- "low" urgency = questions, feature requests, general feedback
"""

def classify_ticket(subject: str, message: str) -> dict:
    user_prompt = f"Subject: {subject}\nMessage: {message}"

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    return json.loads(raw)


if __name__ == "__main__":
    # quick manual test
    result = classify_ticket(
        subject="Can't log in",
        message="I keep getting an error when I try to log into my account"
    )
    print(result)