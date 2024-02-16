from enum import Enum
from datetime import datetime
import requests
from requests import HTTPError
import pytz
from reminder.config import load_config

cfg = load_config()


class LLMErrorType(Enum):
    INVALID_JSON_FORMAT = "INVALID_LLM_JSON_RESPONSE_FORMAT"
    GENERAL = "GENERAL"


class DiscordClient:
    def __init__(
        self,
        channel_id: str,
        bot_token: str,
        base_url: str = "https://discord.com/api/v10",
    ):
        self.base_url = base_url
        self.url = base_url + f"/channels/{channel_id}/messages"
        self.headers = {"Authorization": f"Bot {bot_token}"}

    def report_llm_error(
        self,
        task: str,
        error_type: LLMErrorType,
        document_content: str,
        error_message: str,
        info: str = "",
        llm_response: str = "",
    ):
        """Report LLM Error

        Args:
            error_type (str): LLM task type
            document_content (str): Input document content
            llm_response (str): LLM Response string
            error_message (str): OpenAI Error message
            info (str, optional): Extra optional information. Defaults to "".
        """
        korea_tz = pytz.timezone("Asia/Seoul")
        korea_now = datetime.now(korea_tz).strftime("%Y/%m/%d, %H:%M:%S")
        utc_now = datetime.utcnow().strftime("%Y/%m/%d, %H:%M:%S")

        content = f"# Task: {task}\n## Error Type: {error_type.value}\n* KST: `{korea_now}`\n* UTC: `{utc_now}`\n{info}"
        embeds = [
            {"title": "Document Content", "description": document_content},
            {"title": "Error Message", "description": error_message},
        ]

        if error_type == LLMErrorType.INVALID_JSON_FORMAT:
            embeds.insert(
                1,
                {"title": "LLM Response", "description": llm_response},
            )

        body = {"content": content, "tts": False, "embeds": embeds}

        response = requests.post(url=self.url, json=body, headers=self.headers)

        try:
            response.raise_for_status()
        except HTTPError as e:
            pass


discord_client = DiscordClient(
    channel_id=cfg.discord.channel_id,
    bot_token=cfg.discord.bot_token,
)
