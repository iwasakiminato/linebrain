#-*- coding: utf-8 -*-
# インポートするライブラリ
from flask import Flask, request, abort, render_template, jsonify

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage,
    ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction,
    MessageTemplateAction, URITemplateAction, VideoMessage, AudioMessage, StickerMessage,
    URIAction, RichMenu, DatetimePickerTemplateAction, PostbackEvent
)
import os
import json
import datetime

# 軽量なウェブアプリケーションフレームワーク:Flask
# flaskの定義をする
app = Flask(_name_)

#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


# "/"にGETリクエストを送ると、index.htmlを返す  (ルートのアドレスに以下のものを配置することを明言)
@app.route('/', methods=['GET'])
def index():
    return 'ise'


# 送られてきたメッセージがくる場所　処理する場所？
@app.route("/callback", methods=['POST'])
def callback():
     # get X-Line-Signature header value
    # LINE側が送ってきたメッセージが正しいか検証する  (リクエストヘッダーに含まれる署名を検証して、リクエストがLINEプラットフォームから送信されたことを確認)
    signature = request.headers['X-Line-Signature']

    # ログ表示
    # get request body as text
    body = request.get_data(as_text=True)
    # プログラムの通常の操作中に発生したイベントの報告
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        # 署名を検証し、問題なければhandleに定義されている関数を呼び出す
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 署名検証で失敗したときは例外をあげる
        abort(400)

    #return 'OK'
    return jsonify({"state": 200})

# MessageEvent　テキストメッセージ受け取った時
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if 'こんにちは' in text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Hello World')
         )
    else:
    	line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='「' + text + '」って何？')
         )

if _name_ == "_main_":
    port = int(os.getenv("PORT",8080))
    app.run(host="0.0.0.0", port=port)