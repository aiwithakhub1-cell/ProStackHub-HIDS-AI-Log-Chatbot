import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from detector import detect_log_event


LOG_FILE = os.path.abspath("logs/security.log")


class SecurityLogHandler(FileSystemEventHandler):

    def __init__(self):
        super().__init__()
        self.position = 0

        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

        if os.path.exists(LOG_FILE):
            self.position = os.path.getsize(LOG_FILE)

    def process_new_lines(self):

        if not os.path.exists(LOG_FILE):
            return

        with open(
            LOG_FILE,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            file.seek(self.position)

            new_content = file.read()

            self.position = file.tell()

        if not new_content:
            return

        for line in new_content.splitlines():

            line = line.strip()

            if not line:
                continue

            alerts = detect_log_event(line)

            for alert in alerts:
                print("\n🚨 SECURITY ALERT")
                print(f"Event: {alert['event_type']}")
                print(f"Severity: {alert['severity']}")
                print(f"Source IP: {alert['source_ip']}")
                print(f"Log: {alert['log_message']}")

    def on_modified(self, event):

        if os.path.abspath(event.src_path) == LOG_FILE:
            self.process_new_lines()


def start_log_watcher():

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "a", encoding="utf-8").close()

    event_handler = SecurityLogHandler()

    observer = Observer()

    observer.schedule(
        event_handler,
        os.path.dirname(LOG_FILE),
        recursive=False
    )

    observer.start()

    print(f"Monitoring log file: {LOG_FILE}")

    return observer