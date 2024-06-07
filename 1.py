from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('GpsIpFwvg0COEKfSidtPrJZe1t7ELxxxcgTO9yq1XThlJNCr9d3C3x5pK8gvvb20M00Dcp8hQXB+P5982qe1bw5igyooBUVTknHJr6ymZxlITCp77TFlfqfsM//5GtQKVdT8WhAlrk2Fu/37g5rI1gdB04t89/1O/w1cDnyilFU='))
handler = WebhookHandler(os.getenv('e0e81d04355f41b5ed8a9bb2f0d045d4'))

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 输出群组 ID
    if event.source.type == 'group':
        group_id = event.source.group_id
        user_id = event.source.user_id
        app.logger.info(f"Group ID: {group_id}, User ID: {user_id}")
        # 回复群组 ID 给用户
        line_bot_api.reply_message(event.reply_token, TextMessage(text=f"Group ID: {group_id}"))

if __name__ == "__main__":
    app.run(port=8000)
