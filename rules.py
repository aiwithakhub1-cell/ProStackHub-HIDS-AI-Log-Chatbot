import re


DETECTION_RULES = [
    {
        "name": "Failed Login",
        "pattern": re.compile(
            r"failed login|authentication failure|login failed|invalid password",
            re.IGNORECASE
        ),
        "severity": "MEDIUM"
    },

    {
        "name": "Brute Force Attack",
        "pattern": re.compile(
            r"brute force|multiple failed login|too many authentication failures",
            re.IGNORECASE
        ),
        "severity": "HIGH"
    },

    {
        "name": "Privilege Escalation",
        "pattern": re.compile(
            r"privilege escalation|root access|administrator privilege|sudo",
            re.IGNORECASE
        ),
        "severity": "HIGH"
    },

    {
        "name": "Port Scanning",
        "pattern": re.compile(
            r"port scan|nmap scan|scanning ports|multiple ports",
            re.IGNORECASE
        ),
        "severity": "MEDIUM"
    }
]


def match_rules(log_line):
    detected = []

    for rule in DETECTION_RULES:
        if rule["pattern"].search(log_line):
            detected.append(rule)

    return detected