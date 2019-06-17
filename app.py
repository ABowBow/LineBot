from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('8lkhlrRmimnctTvBpNbpuGfMm2VWkoJKfIubH6zEA8Or3Kq5WgCEE49RM2hoWcMQawyWak7rknJGxgwMKY9LCK+Sv475YQ/J1o4y2DyyPdeiiQl4PvqeNrMwpRo3GH4GtmAJAcgyBAOPgPWViczisQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9b9928d58bdc8eb6fb55d5f79d2b56f5')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()