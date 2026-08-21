import os

from dotenv import load_dotenv
from groq import Groq

from database import get_alerts


load_dotenv()


API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)


def ask_ai(question):

    if not API_KEY:
        return (
            "Groq API key is not configured. "
            "Please add GROQ_API_KEY to your .env file."
        )

    alerts = get_alerts(50)

    if alerts:

        alert_text = "\n".join(
            [
                (
                    f"Time: {alert['timestamp']} | "
                    f"Event: {alert['event_type']} | "
                    f"Severity: {alert['severity']} | "
                    f"Source IP: {alert['source_ip']} | "
                    f"Log: {alert['log_message']}"
                )
                for alert in alerts
            ]
        )

    else:
        alert_text = "No security alerts have been detected yet."

    prompt = f"""
You are a cybersecurity assistant.

Analyze the following HIDS security events.

Security Events:
{alert_text}

User Question:
{question}

Provide:

1. What happened
2. Which security event is relevant
3. Severity and risk
4. Possible attack technique
5. Recommended remediation steps

Do not invent events that are not present in the supplied logs.
If the information is insufficient, clearly say so.
"""

    try:

        client = Groq(api_key=API_KEY)

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a defensive cybersecurity "
                        "log-analysis assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as error:

        return f"AI analysis error: {error}"