import os
import openai
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.rtm_v2 import RTMClient

# Initialize OpenAI and Slack clients
openai.api_key = os.getenv("OPENAI_API_KEY")
slack_token = os.getenv("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

@RTMClient.run_on(event="message")
def handle_message(**payload):
    data = payload['data']
    web_client = payload['web_client']
    if 'text' in data and 'bot_id' not in data:
        user_query = data['text']
        channel_id = data['channel']

        # Get response from OpenAI
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_query,
            max_tokens=150
        )
        answer = response.choices[0].text.strip()

        # Send response back to Slack
        try:
            web_client.chat_postMessage(
                channel=channel_id,
                text=answer
            )
        except SlackApiError as e:
            print(f"Error posting message: {e.response['error']}")

if __name__ == "__main__":
    rtm_client = RTMClient(token=slack_token)
    rtm_client.start()
