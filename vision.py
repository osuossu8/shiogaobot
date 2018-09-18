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

print("** a **")
model = None
print(model)
print("** b **")

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
    image = cv2.imread(image_url)
    if image is None:
        print("Not open")
    b,g,r = cv2.split(image)
    image = cv2.merge([r,g,b])
    img = cv2.resize(image,(64,64))
    img=np.expand_dims(img,axis=0)
    print("** 1 **")
    face = detect_who(img=img)
    print("** 7**")
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
    counter = 0
    face=""
    print("** 2 **")
    global model
    print("** 3 **")
    print(model)
    if model is None:
        model = load_model('./shiogao_model2.h5')
        print(model)
    #print(model.summary())
    print("** 4 **")
    predict = model.predict(img)
    print("** 5 **")
    #print(predict)
    print("** 6 **")
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
