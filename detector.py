import re
from collections import defaultdict, deque
from datetime import datetime, timedelta

from rules import match_rules
from database import save_alert


FAILED_LOGIN_WINDOW = 60
FAILED_LOGIN_THRESHOLD = 5

failed_attempts = defaultdict(deque)


def extract_ip(log_line):
    match = re.search(
        r"(?:ip=|src=|source=)(\d{1,3}(?:\.\d{1,3}){3})",
        log_line,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return "Unknown"


def detect_log_event(log_line):

    current_time = datetime.now()

    source_ip = extract_ip(log_line)

    detected_rules = match_rules(log_line)

    alerts = []

    for rule in detected_rules:

        alert = {
            "event_type": rule["name"],
            "severity": rule["severity"],
            "source_ip": source_ip,
            "log_message": log_line
        }

        alerts.append(alert)

    # Track failed login attempts for brute-force detection
    if re.search(
        r"failed login|authentication failure|login failed|invalid password",
        log_line,
        re.IGNORECASE
    ):

        attempts = failed_attempts[source_ip]

        attempts.append(current_time)

        while attempts:
            age = current_time - attempts[0]

            if age > timedelta(seconds=FAILED_LOGIN_WINDOW):
                attempts.popleft()
            else:
                break

        if len(attempts) >= FAILED_LOGIN_THRESHOLD:

            already_detected = any(
                alert["event_type"] == "Brute Force Attack"
                for alert in alerts
            )

            if not already_detected:

                alerts.append({
                    "event_type": "Brute Force Attack",
                    "severity": "HIGH",
                    "source_ip": source_ip,
                    "log_message": log_line
                })

    for alert in alerts:
        save_alert(
            alert["event_type"],
            alert["severity"],
            alert["source_ip"],
            alert["log_message"]
        )

    return alerts