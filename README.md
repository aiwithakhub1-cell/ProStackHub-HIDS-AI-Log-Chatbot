# ProStackHub HIDS AI Log Chatbot

A Host-Based Intrusion Detection System (HIDS) that monitors security logs in real time, detects suspicious activities using rule-based detection, stores alerts in SQLite, and provides an AI-powered security analysis chatbot.

## Features

* Real-time log monitoring using Watchdog
* Failed login detection
* Brute-force detection
* Privilege escalation detection
* Port-scan detection
* Regex-based security rules
* SQLite alert storage
* Flask security dashboard
* Alert history
* AI-powered log analysis with Groq
* Natural-language security questions
* Nmap validation

## Architecture

```text
Security Log
     ↓
Watchdog
     ↓
Detection Rules
     ↓
Suspicious Event
     ↓
SQLite Database
     ↓
Flask Dashboard
     ↓
Groq AI Analysis
```

## Technologies

* Python
* Flask
* Watchdog
* SQLite
* Groq API
* Nmap
* HTML
* CSS
* Git & GitHub

## Project Structure

```text
ProStackHub-HIDS-AI-Log-Chatbot/
│
├── app.py
├── database.py
├── detector.py
├── rules.py
├── log_watcher.py
├── ai_chatbot.py
├── nmap_validation.py
├── requirements.txt
├── .gitignore
│
├── logs/
│   └── security.log
│
├── templates/
│   └── dashboard.html
│
└── results/
    └── hids.db
```

## Installation

Create and activate a Python virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

Never commit `.env` or API keys to GitHub.

## Running the Project

Start the HIDS dashboard:

```powershell
.\.venv\Scripts\python.exe app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Security Testing

Use only systems and networks that you own or are explicitly authorized to test.

## Project Status

Core HIDS functionality includes real-time monitoring, rule-based detection, SQLite alert storage, Flask visualization, and AI-assisted security analysis.
## Project Demonstration

A demonstration video of the HIDS and AI Log Chatbot is included in this repository.

[Watch HIDS Demonstration Video](hids.mp4)