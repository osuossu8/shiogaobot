# -*- coding: utf-8 -*-

import requests
import settings
import os
import numpy as np
import cv2
from keras.models import load_model

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

#LINEBotのキーを設定
LINE_API_ENDPOINT = "https://api.line.me/v2/bot/message/reply"

def get_text_by_ms(image_url=None, image=None):
    if image_url is None and image is None:
        return '必要な情報が足りません'

    if image_url:
        headers = {
    "Content-Type": "application/json",
    }
        data = {'url': image_url}
        response = requests.post(
            LINE_API_ENDPOINT,
            headers=headers,
            json=data
        )

    elif image is not None:
        headers = {
    "Content-Type": "application/json",
    }
        response = requests.post(
            LINE_API_ENDPOINT,
            headers=headers,
            data=image,
        )

    status = response.status_code
    data = response.json()

    #####
    print("** 1 **")
    print("** 2 **")
    image = cv2.imread(image_url)
    if image is None:
        print("Not open")
    print("** 3 **")
    b,g,r = cv2.split(image)
    image = cv2.merge([r,g,b])
    img = cv2.resize(image,(64,64))
    img=np.expand_dims(img,axis=0)
    print("** 4 **")
    face = detect_who(img=img)
    print("** 9 **")
    print(face)
    #####

    text = face

    if len(text) == 0:
        text += '文字が検出できませんでした'

    print('text:', text)
    return text

#####
def detect_who(img):
    #予測
    #print(img)
    face=""
    global model
    model = load_model('./shiogao_model2.h5')
    print("** 5 **")
    print(model.summary())
    print("** 6 **")
    predict = model.predict(img)
    print("** 7 **")
    print(predict)
    print("** 8 **")
    faceNumLabel=np.argmax(predict)
    if faceNumLabel == 0:
        face = "オリーブオイル顔"
    elif faceNumLabel == 1:
        face = "塩顔"
    elif faceNumLabel == 2:
        face = "しょうゆ顔"
    elif faceNumLabel == 3:
        face = "ソース顔"
    return face
#####

if __name__ == "__main__":
    get_text_by_ms(image_url)
