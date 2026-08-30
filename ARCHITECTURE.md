# Architecture — HIDS + AI Log Chatbot

## 1. System Overview

This project is a Host-Based Intrusion Detection System (HIDS) that monitors security logs in real time, detects suspicious activities using rule-based detection, stores alerts in SQLite, and provides AI-assisted security analysis through a Flask dashboard.

## 2. Architecture

```text
Security Log
     |
     v
Watchdog File Monitoring
     |
     v
Detection Engine
     |
     +----------------------+
     |                      |
     v                      v
Detection Rules       Brute-Force Analysis
     |                      |
     +----------+-----------+
                |
                v
          Security Alert
                |
                v
          SQLite Database
                |
        +-------+--------+
        |                |
        v                v
Flask Dashboard       Groq AI
        |                |
        +-------+--------+
                |
                v
       Security Analysis
       + Remediation