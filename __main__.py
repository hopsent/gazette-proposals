import logging
from logging.handlers import RotatingFileHandler
from os import getenv
import json

from dotenv import load_dotenv
from slack_bolt import App
#from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web.client import WebClient

from core.slacker import Slacker
from core.data import StatusData as ST


load_dotenv()


handler = RotatingFileHandler(
    'logs/' + __name__ + '.log',
    maxBytes=52428800,
)
logger_main = logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(process)d, %(message)s, %(name)s',
    handlers=[handler, ],
)
logger = logging.getLogger(__name__)

token = getenv('BOT_TOKEN', '000000')
signing_secret = getenv('SIGNING_SECRET')
app = App(token=token, signing_secret=signing_secret)
app_token = getenv('APP_TOKEN', '000000')
channel_id = getenv('CHANNEL_ID', '000000')
port = int(getenv('SLACK_PORT', '0000'))


@app.event('app_mention')
def start_polling(event, client: WebClient):
    logger.info(json.dumps(event, indent=4))
    if event['channel'] == channel_id:
        slacker = Slacker(
            action=ST.NO_ACTION,
            client=client,
            user=event['user'],
            channel=event['channel'],
            msg=event['ts']
            )
        text = event['text'].lower()
        if ST.READ_REQUEST in text:
            slacker.action = ST.READ_DATA
            if ST.READ_EXACT_DATA in text:
                slacker.action = ST.READ_EXACT_DATA
                index = int(text.index(ST.READ_EXACT_DATA)) + 1
                gazette_num_raw = text[index:]
                g_num = gazette_num_raw.replace(' ', '').replace('.', '')
                slacker.exact_gazette = g_num
        if ST.WRITE_REQUEST in text:
            slacker.action = ST.WRITE_LETTERS
        slacker.human_interaction(
            event=event,
            token=token
        )


def main():
    # SocketModeHandler(app, app_token).start()
    app.start(port=port)


if __name__ == '__main__':
    main()
