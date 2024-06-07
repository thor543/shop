from flask import Flask, request, abort
from linebot.v3.messaging import MessagingApi
from linebot.v3.webhook import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.v3.messaging.models import TextMessage
import os

app = Flask(__name__)

# 从环境变量中获取 Line Bot API 和 Webhook Handler 的凭证
channel_access_token = os.getenv('GpsIpFwvg0COEKfSidtPrJZe1t7ELxxxcgTO9yq1XThlJNCr9d3C3x5pK8gvvb20M00Dcp8hQXB+P5982qe1bw5igyooBUVTknHJr6ymZxlITCp77TFlfqfsM//5GtQKVdT8WhAlrk2Fu/37g5rI1gdB04t89/1O/w1cDnyilFU=')
channel_secret = os.getenv('e0e81d04355f41b5ed8a9bb2f0d045d4')

# 检查是否获取到了环境变量

# 创建 MessagingApi 实例时，传递一个配置对象作为参数
config = {
    "channel_access_token": channel_access_token,
    "channel_secret": channel_secret
}

line_bot_api = MessagingApi(config)
handler = WebhookHandler(channel_secret=channel_secret)

@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(TextMessage)
def handle_message(event):
    if event.source.type == 'group':
        group_id = event.source.group_id
        app.logger.info(f"Group ID: {group_id}")
        line_bot_api.reply_message(event.reply_token, TextMessage(text=f"Group ID: {group_id}"))

if __name__ == "__main__":
    app.run(port=8000)
