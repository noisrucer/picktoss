import requests


class EmailManager:
    def __init__(self, mailgun_api_key: str, mailgun_domain: str):
        self.mailgun_api_key = mailgun_api_key
        self.mailgun_domain = mailgun_domain

    def send_email(self, recipient: str, subject: str, content: str) -> None:

        requests.post(
            url=self.mailgun_domain,
            auth=("api", self.mailgun_api_key),
            data={"from": "reminder <admin@girok.org>", "to": [recipient], "subject": subject, "html": content},
        )

    def read_and_format_html(
        self,
        replacements: dict[str, str],
        html_path: str = "reminder/core/email/verification_template.html",
    ) -> str:
        f = open(html_path, "rt", encoding="UTF8")
        content = f.read()
        for target, val in replacements.items():
            content = content.replace(target, val)
        f.close()
        return content
