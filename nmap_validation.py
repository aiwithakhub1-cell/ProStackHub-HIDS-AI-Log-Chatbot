import subprocess
from datetime import datetime
import os


LOG_FILE = "logs/security.log"


def run_nmap_validation():
    target = "127.0.0.1"

    print(f"Running Nmap validation against {target}...\n")

    try:
        result = subprocess.run(
            [
                r"C:\Program Files (x86)\Nmap\nmap.exe",
                "-sT",
                "-p",
                "1-1000",
                target
            ],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            print("Nmap returned an error:")
            print(result.stderr)
            return

        print("Nmap scan completed.\n")
        print(result.stdout)

        os.makedirs("logs", exist_ok=True)

        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(
                f"{datetime.now().isoformat()} "
                f"Nmap scan detected source={target} "
                f"multiple ports\n"
            )

        print("\nNmap validation event written to security.log.")

    except FileNotFoundError:
        print(
            "Nmap was not found. Make sure Nmap is installed "
            "and available in PATH."
        )

    except subprocess.TimeoutExpired:
        print("Nmap scan timed out.")

    except Exception as error:
        print(f"Validation error: {error}")


if __name__ == "__main__":
    run_nmap_validation()