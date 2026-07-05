import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


REPORT_PATH = Path("reports/latest_report.txt")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def required_email_settings():
    return {
        "AEGIS_EMAIL_TO": os.getenv("AEGIS_EMAIL_TO"),
        "AEGIS_EMAIL_FROM": os.getenv("AEGIS_EMAIL_FROM"),
        "AEGIS_EMAIL_APP_PASSWORD": os.getenv("AEGIS_EMAIL_APP_PASSWORD"),
    }


def missing_settings(settings):
    return [name for name, value in settings.items() if not value]


def build_message(sender, recipient, report_text):
    message = EmailMessage()
    message["Subject"] = "AEGIS Paper-Trading Report"
    message["From"] = sender
    message["To"] = recipient
    message.set_content(report_text)
    return message


def send_latest_report():
    settings = required_email_settings()
    missing = missing_settings(settings)

    if missing:
        print("AEGIS email not sent. Missing required environment variables:")
        for name in missing:
            print(f"- {name}")
        return False

    if not REPORT_PATH.exists():
        print(f"AEGIS email not sent. Report not found: {REPORT_PATH}")
        print("Run: python3 -m aegis.reports")
        return False

    report_text = REPORT_PATH.read_text()
    message = build_message(
        settings["AEGIS_EMAIL_FROM"],
        settings["AEGIS_EMAIL_TO"],
        report_text,
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(
            settings["AEGIS_EMAIL_FROM"],
            settings["AEGIS_EMAIL_APP_PASSWORD"],
        )
        smtp.send_message(message)

    print(f"AEGIS report emailed to {settings['AEGIS_EMAIL_TO']}")
    return True


def main():
    send_latest_report()


if __name__ == "__main__":
    main()
