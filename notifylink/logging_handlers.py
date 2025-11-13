import json
import logging
from datetime import datetime

import requests


class GoogleChatHandler(logging.Handler):

    def __init__(self, webhook_url):
        super().__init__()
        self.webhook_url = webhook_url

    def emit(self, record):
        try:
            log_message = self.format(record)

            message = {
                "text": f"*NotifyLink Debug Log*\n"
                        f"**Level:** {record.levelname}\n"
                        f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                        f"**Module:** {record.module}\n"
                        f"**Message:**\n```\n{log_message}\n```"
            }

            requests.post(
                self.webhook_url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(message),
                timeout=5
            )
        except Exception:
            pass
