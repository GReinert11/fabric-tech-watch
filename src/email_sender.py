import os
from pathlib import Path

import resend
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

resend.api_key = os.environ["RESEND_API_KEY"]


def send_newsletter():

    html_path = BASE_DIR / "reports" / "newsletter.html"

    if not html_path.exists():
        raise FileNotFoundError("Newsletter HTML introuvable")

    html_content = html_path.read_text(encoding="utf-8")

    response = resend.Emails.send({
        "from": os.environ["EMAIL_FROM"],
        "to": [os.environ["EMAIL_TO"]],
        "subject": "Fabric Tech Watch — Veille hebdomadaire",
        "html": html_content
    })

    print("Email accepté par Resend :", response["id"])


if __name__ == "__main__":
    send_newsletter()