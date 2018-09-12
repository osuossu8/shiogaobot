import requests
import settings

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
    "Authorization": "Bearer " + LINE_ACCESSTOKEN
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
    "Authorization": "Bearer " + LINE_ACCESSTOKEN
    }
        response = requests.post(
            LINE_API_ENDPOINT,
            headers=headers,
            data=image,
        )

    status = response.status_code
    data = response.json()

    if status != 200:

        if data['code'] == 'InvalidImageSize':
            text = '画像のサイズが大きすぎます'

        elif data['code'] == 'InvalidImageUrl':
            text = 'この画像URLからは取得できません'

        elif data['code'] == 'InvalidImageFormat':
            text = '対応していない画像形式です'

        else:
            text = 'エラーが発生しました'

        print(status, data)
        return text

    text = ''

    if len(text) == 0:
        text += '文字が検出できませんでした'

    print('text:', text)
    return text

if __name__ == "__main__":
    get_text_by_ms(image_url)
