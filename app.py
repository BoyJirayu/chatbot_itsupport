from flask import Flask, jsonify, render_template, request
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageSendMessage, StickerSendMessage, AudioSendMessage
from linebot.models.template import *
from linebot import LineBotApi, WebhookHandler
from use_model import myPredict, lamda_l
from firebase import firebase
from connect_firebase import *

import json
import numpy as np

firebase = firebase.FirebaseApplication('https://line-itsupport-firebase-default-rtdb.firebaseio.com/', None)

app = Flask(__name__)

lineaccesstoken = 'CxoEeTecHEIzApUgMPohAgQALqbSi/i0xq0Qx16YGDjwyqSXUXbtbul7oA8t1EiF6Ti+ylCs3JRmMLhBAyWP3l8r8KoCrPymAt4F+6j0AqO5Dg7ArwsY0YRgN+trYbjUyvbPqywXerDtCBGIbOAd/AdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(lineaccesstoken)

####################### new ########################
@app.route('/')
def index():
    return "Hello World!"


@app.route('/webhook', methods=['POST'])
def callback():
    json_line = request.get_json(force=False,cache=False)
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    no_event = len(decoded['events'])
    for i in range(no_event):
        event = decoded['events'][i]
        event_handle(event)
    return '',200


def event_handle(event):
    print(event)

    userID = event['source']['userId']
    Reply_token = event['replyToken']
    msgType = event["message"]["type"]

    # User Profile
    profile = line_bot_api.get_profile(userID)
    user_name = profile.display_name
    user_pic = profile.picture_url
    db_name = "User Profile"
    data = {"Display_Name": user_name, "Profile_Pic": user_pic}

    post_user_pofile(uid=userID,data=data,firebase_app=firebase,db_name=db_name)

    if msgType == "text":
      message = str(event["message"]["text"])

      if message :
        Label_message = myPredict(message)
        if Label_message == "ทักทาย" :
          Reply_message = "สวัสดีครับ K'" + user_name +"\n" + " IT Support ยินดีให้บริการครับ"
        elif Label_message == "เสร็จสิ้นและขอบคุณ" :
          Reply_message = "IT Support ยินดีให้บริการครับ ขอบคุณครับ"
        elif Label_message == "Video Conference" :
          Reply_message = "ถ้าท่านต้องการใช้งานระบบ Video Conference"+"\n"+"โปรดแจ้งรายละเอียด ดังนี้"+"\n"+"ชื่อการประชุม วันที่ เวลา และต้องการอุปกรณ์สำหรับประชุม Video Conference หรือไม่"
        elif Label_message == "ระบบ E-Budget" :
          Reply_message = "Test"
        elif Label_message == "ระบบ VPN" :
          Reply_message = "ท่านสามารถใช้งานผ่าน Web Browser ได้ที่ลิงก์ https://vpn.mhesi.go.th/dana-na/auth/url_3/welcome.cgi"
        elif Label_message == "ระบบ ERP" :
          Reply_message = "สามารถใช้ฃานได้ผ่าน https://erp.mhesi.go.th/"
        elif Label_message == "Share Drive" :
          Reply_message = "Test"
        elif Label_message == "Back Office System" :
          Reply_message = "Test"
        elif Label_message == "Email" :
          Reply_message = "สามารถใช้งานได้ที่ webmail.mhesi.go.th"
        elif Label_message == "Internet" :
          Reply_message = "Test"
        elif Label_message == "Network Security" :
          Reply_message = "Test"
        elif Label_message == "เครื่องแม่ข่าย VM & Server" :
          Reply_message = "Test"
        elif Label_message == "Printer & Scanner" :
          Reply_message = "รับทราบครับ เดี๋ยวเจ้าหน้าที่จะดำเนินการติดตั้งหรือแก้ปัญหาเครื่อง Printer/Scanner ของท่านให้ครับ"
        elif Label_message == "ปัญหา Computer" :
          Reply_message = "Test"
        elif Label_message == "ยืมคืน Accessory" :
          Reply_message = "Test"

        TextMessage = TextSendMessage(text=Reply_message)
        Reply_object = TextMessage
        line_bot_api.reply_message(Reply_token, Reply_object)

    else:
        Reply_object = StickerSendMessage(package_id=str(1),sticker_id=str(2))
        line_bot_api.reply_message(Reply_token, Reply_object)

if __name__ == '__main__':
    app.run(debug=True)