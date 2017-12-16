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

line_bot_api = LineBotApi('uvlk18Xh8Mb6XkyAiP3FKr820XKQRcv8BPFy1JZ01nu05+2l4iyfLihVMtPu+j9JDmw0DO+1d8NlhKUqdekRNEP9YzAOyN4zSvNZWnl8jQEhGKdtMuuTaSVzzvUuMSiB1Z+J8Qt7GJ12uiT2kQtCMwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('82c0056ca4312d125939533fb29e149f')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    content = "{}: {}".format(event.source.user_id, event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
