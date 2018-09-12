from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import(
    InvalidSignatureError
)

from linebot.models import(
    MessageEvent, TextMessage, TextSendMessage,
)

import os
import requests
import json
import io
from PIL import Image

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#####
@app.route("/hello")
def hello_world():
    return "hello world!"

#####
header = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + YOUR_CHANNEL_ACCESS_TOKEN
}

@app.route("/", methods=['POST'])
def root_post():

    for event in request.json['events']:
        if event['type'] == 'message':
            if event['message']['type'] == 'image':
                msg = getImageLine(event['message']['id'])
                lineReply(event, msg)

    return '', 200, {}

#指定されたメッセージで返送する
def lineReply(event, message):

    payload = {
        'replyToken': event['replyToken'],
        'messages': [{
            "type": "text",
            "text": message
        }]
    }

    #LineBotのエンドポイントに送信
    response = requests.post(
        LINE_API_ENDPOINT, headers=header, data=json.dumps(payload))

#LINEから画像データを取得
def getImageLine(id):

    line_url = 'https://api.line.me/v2/bot/message/' + id + '/content/'

    # 画像の取得
    result = requests.get(line_url, headers=header)

    # 画像の保存
    i = Image.open(io.StringIO(result.content))
    filename = '/tmp/' + id + '.jpg'
    i.save(filename)

    return handler_message(filename)

#####

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
        abort(400)

    return 'OK'

#@handler.add(MessageEvent, message=TextMessage)
#def handler_message(event):
def handler_message(string):
     line_bot_api.reply_message(
         event.reply_token,
         TextSendMessage(text=string))

"""
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))
"""
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
