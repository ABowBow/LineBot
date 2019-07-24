from flask import Flask, request, abort
from bs4 import BeautifulSoup
import simplejson as json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('8lkhlrRmimnctTvBpNbpuGfMm2VWkoJKfIubH6zEA8Or3Kq5WgCEE49RM2hoWcMQawyWak7rknJGxgwMKY9LCK+Sv475YQ/J1o4y2DyyPdeiiQl4PvqeNrMwpRo3GH4GtmAJAcgyBAOPgPWViczisQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('9b9928d58bdc8eb6fb55d5f79d2b56f5')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='ABC'))

def getPhoto():
    insta_url = 'https://www.instagram.com/explore/tags/realyami/'
    res = requests.get(insta_url)
    if res.status_code == requests.codes.ok:
        soup = BeautifulSoup(res.text, "lxml")
        json_part = soup.find_all("script", type="text/javascript")[3].string
        json_part = json_part[json_part.find('=')+2:-1]
        data = json.loads(json_part)
        image_Ary = data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']
        image_Ary_len = len(image_Ary)
        indexNum = random.randint(0,image_Ary_len)
        return image_Ary[indexNum]['node']['display_url']

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8899))
    app.run(host='0.0.0.0', port=port)