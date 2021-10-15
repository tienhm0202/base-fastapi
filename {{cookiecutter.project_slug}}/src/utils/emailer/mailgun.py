import requests

from src.config import email_settings
from src.utils import get_logger


logger = get_logger(__name__)


class MailGun:
    def send(self, to_mail, content, subject):
        from_mail = f"{email_settings.EMAILER_FROM_NAME} "\
            f"<{email_settings.EMAILER_FROM_EMAIL}>"
        baseurl = "https://api.mailgun.net/v3"
        return requests.post(
            f"{baseurl}/{email_settings.EMAILER_MAILGUN_DOMAIN}/messages",
            auth=("api", email_settings.EMAILER_MAILGUN_KEY),
            data={
                "from": from_mail,
                "to": [to_mail],
                "subject": subject,
                "html": content
            })
