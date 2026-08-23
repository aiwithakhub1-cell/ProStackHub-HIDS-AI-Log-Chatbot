import os

from dotenv import load_dotenv
from groq import Groq

from database import get_alerts


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")


def ask_ai(question):
    # Load the project's .env every time
    load_dotenv(ENV_FILE, override=True)

    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-120b"
    )

    if not api_key:
        return (
            "AI configuration error: "
            "GROQ_API_KEY is missing from the project .env file."
        )

    alerts = get_alerts(50)

    if alerts:
        alert_text = "\n".join(
            (
                f"Time: {alert['timestamp']} | "
                f"Event: {alert['event_type']} | "
                f"Severity: {alert['severity']} | "
                f"Source IP: {alert['source_ip']} | "
                f"Log: {alert['log_message']}"
            )
            for alert in alerts
        )
    else:
        alert_text = "No security alerts have been detected yet."

    prompt = f"""
You are a defensive cybersecurity assistant.

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
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model=model,
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
            max_tokens=1000,
            include_reasoning=False
        )

        return response.choices[0].message.content

    except Exception as error:
        print(f"AI analysis error: {error}")
        return f"AI analysis error: {error}"