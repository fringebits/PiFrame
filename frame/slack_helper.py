import logging
logger = logging.getLogger()

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class Slack:
    def __init__(self, config):
        self.config = config

    def send(self, message, upload=None, channel=None):
        slack_token = self.config.slack_token
        slack_channel = self.config.slack_channel
        client = WebClient(token=slack_token)

        if channel is None:
            channel = slack_channel

        try:
            if upload is not None:
                response = client.files_upload(
                    channels=channel,
                    file=upload,
                    title=message)
            else:
                response = client.chat_postMessage(
                    channel=channel,
                    text=message
                )

        except SlackApiError as e:
            assert e.response["error"]