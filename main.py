from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import(
    InvalidSignatureError
)

from linebot.models import(
    ImageMessage, MessageEvent, TextMessage, TextSendMessage,
)

import os
import requests
import json
import io
from io import BytesIO
from PIL import Image

import settings
from vision import get_text_by_ms, detect_who

import numpy as np
import cv2
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from keras.models import load_model

app = Flask(__name__)

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

@handler.add(MessageEvent, message=TextMessage)
def handler_message(event):
     line_bot_api.reply_message(
         event.reply_token,
         TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    print("handle_image:", event)

    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)

    image = BytesIO(message_content.content)

    try:
        image_text = get_text_by_ms(image=image)
        ###
        model = load_model('./shiogao_model2.h5')
        image = cv2.imread(image_url)
        if image is None:
            print("Not open")
        b,g,r = cv2.split(image)
        image = cv2.merge([r,g,b])
        img = cv2.resize(image,(64,64))
        img=np.expand_dims(img,axis=0)
        face = detect_who(img=img)
        print(face)
        ###

        messages = [
            TextSendMessage(text=face),
        ]

        reply_message(event, messages)

    except Exception as e:
        reply_message(event, TextSendMessage(text='エラーが発生しました'))

def reply_message(event, messages):
    line_bot_api.reply_message(
        event.reply_token,
        messages=messages,
    )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
