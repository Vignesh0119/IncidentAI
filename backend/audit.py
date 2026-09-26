# audit.py

import json
from datetime import datetime


AUDIT_FILE = "audit.log"


def write_audit(event_type, details):
    """
    Record an event in the audit log.
    """

    event = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "details": details
    }

    with open(AUDIT_FILE, "a", encoding="utf-8") as file:
        file.write(
            json.dumps(event) + "\n"
        )

    print(f"[AUDIT] {event_type}")


def get_audit_logs():
    """
    Read all audit events.
    """

    logs = []

    try:
        with open(AUDIT_FILE, "r", encoding="utf-8") as file:

            for line in file:
                if line.strip():
                    logs.append(
                        json.loads(line)
                    )

    except FileNotFoundError:
        return []

    return logs


def clear_audit_logs():
    """
    Clear the audit log for a fresh demo.
    """

    open(
        AUDIT_FILE,
        "w",
        encoding="utf-8"
    ).close()


if __name__ == "__main__":

    print("Current Audit Logs:")

    logs = get_audit_logs()

    if not logs:
        print("No audit events yet.")

    for log in logs:
        print(
            f"{log['timestamp']} | "
            f"{log['event']} | "
            f"{log['details']}"
        )