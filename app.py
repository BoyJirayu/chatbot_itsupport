from flask import Flask, jsonify, render_template, request
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageSendMessage,FlexSendMessage, StickerSendMessage, AudioSendMessage, QuickReply, QuickReplyButton, MessageAction
from linebot.models.template import *
from linebot import LineBotApi, WebhookHandler
from use_model import myPredict, comma
from firebase import firebase
from connect_firebase import *
from card_function import *
from compare_text import *

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

    # Add User Profile to DB
    post_user_profile(uid=userID,data=data,firebase_app=firebase,db_name=db_name)

    # Verify User Session
    user_session = get(uid=userID,firebase_app=firebase,db_name="User Session")
    # create session for new user
    if (user_session is None):
      post_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
      user_session = get(uid=userID,firebase_app=firebase,db_name="User Session")
    user_session = user_session["Session"]

    # Verify Message for reply back
    if msgType == "text":
      message = str(event["message"]["text"])

      if user_session == 0 :  
        if match_menu(def_msg="ขอแจ้งปัญหาการใช้งานด้าน IT ครับ",user_msg=message) :
          Reply_object = TextSendMessage(text='โปรดระบุประเภทปัญหาที่ท่านใช้งานครับ',quick_reply=QuickReply(items=[
              QuickReplyButton(action=MessageAction(label="VPN", text="ปัญหาการใช้งาน VPN")),
              QuickReplyButton(action=MessageAction(label="Share Drive", text="Share Drive")),
              QuickReplyButton(action=MessageAction(label="E-mail", text="E-mail")),
              QuickReplyButton(action=MessageAction(label="Internet", text="Internet")),
              QuickReplyButton(action=MessageAction(label="Printer & Scanner", text="Printer & Scanner")),
              QuickReplyButton(action=MessageAction(label="คอมพิวเตอร์", text="การใช้งานเครื่องคอมพิวเตอร์")),
            ]))
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 1},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ขอแจ้งปัญหาการใช้งานระบบ Back Office ครับ",user_msg=message) :
          Reply_object = TextSendMessage(text='โปรดระบุระบบ Back Office ที่ท่านใช้งานครับ',quick_reply=QuickReply(items=[
              QuickReplyButton(action=MessageAction(label="ระบบสารบรรณ", text="ระบบสารบรรณ")),
              QuickReplyButton(action=MessageAction(label="ระบบใบลา", text="ระบบใบลา")),
              QuickReplyButton(action=MessageAction(label="ระบบหนังสือเวียน", text="ระบบหนังสือเวียน")),
              QuickReplyButton(action=MessageAction(label="ระบบ S-curve", text="ระบบ S-curve")),
              QuickReplyButton(action=MessageAction(label="ระบบ DPIS", text="ระบบ DPIS")),
              QuickReplyButton(action=MessageAction(label="ระบบ ERP", text="ระบบ ERP")),
            ]))
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 2},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="รบกวนขอใช้งานระบบประชุมออนไลน์ (Zoom) ครับ",user_msg=message) :
          Reply_object = TextSendMessage(text="โปรดระบุชื่อการประชุมครับ")
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 3},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="กรุณาเรียกเจ้าหน้าที่ให้หน่อยครับ",user_msg=message) :
          line_notify(name=user_name)
          Reply_object = TextSendMessage(text="โปรดระบุปัญหาของท่านให้เจ้าหน้าที่ทราบ")
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 4},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ขอเบอร์หรือช่องทางการติดต่อ IT Support ครับ",user_msg=message) :
          flex = contact_card(name=user_name,pic=user_pic)
          flex = json.loads(flex)
          Reply_object = FlexSendMessage(alt_text='Flex Message',contents=flex)
          line_bot_api.reply_message(Reply_token, Reply_object)

      elif user_session == 1 :
        if match_menu(def_msg="ปัญหาการใช้งาน VPN",user_msg=message) :
          Reply_object = TextSendMessage(text='การใช้งาน VPN....')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ปัญหาการใช้งาน Share Drive",user_msg=message) :
          Reply_object = TextSendMessage(text='การใช้งาน Share Drive....')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ปัญหาการใช้งาน E-mail",user_msg=message) :
          Reply_object = TextSendMessage(text='การใช้งาน E-mail....')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ปัญหาการใช้งาน Internet",user_msg=message) :
          Reply_object = TextSendMessage(text='การใช้งาน Internet....')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ปัญหาการใช้งาน Printer & Scanner",user_msg=message) :
          Reply_object = TextSendMessage(text='การใช้งาน Printer & Scanner....')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ปัญหาการใช้งานเครื่องคอมพิวเตอร์ computer",user_msg=message) :
          Reply_object = TextSendMessage(text='การใช้งานคอมพิวเตอร์....')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        else :
          Reply_object = TextSendMessage(text='ฉันไม่เข้าใจ โปรดระบุประเภทปัญหาที่ท่านใช้งานอีกครั้งครับ',quick_reply=QuickReply(items=[
              QuickReplyButton(action=MessageAction(label="VPN", text="ปัญหาการใช้งาน VPN")),
              QuickReplyButton(action=MessageAction(label="Share Drive", text="Share Drive")),
              QuickReplyButton(action=MessageAction(label="E-mail", text="E-mail")),
              QuickReplyButton(action=MessageAction(label="Internet", text="Internet")),
              QuickReplyButton(action=MessageAction(label="Printer & Scanner", text="Printer & Scanner")),
              QuickReplyButton(action=MessageAction(label="คอมพิวเตอร์", text="การใช้งานเครื่องคอมพิวเตอร์")),
            ]))
          line_bot_api.reply_message(Reply_token, Reply_object)

      elif user_session == 2 :
        if match_menu(def_msg="ระบบสารบรรณ",user_msg=message) :
          Reply_object = TextSendMessage(text='การใช้งานระบบสารบรรณ....')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ระบบใบลา",user_msg=message) :
          Reply_object = TextSendMessage(text='การใช้งานระบบใบลา....')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ระบบหนังสือเวียน",user_msg=message) :
          Reply_object = TextSendMessage(text='การใช้งานระบบหนังสือเวียน....')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="S-curve",user_msg=message) :
          Reply_object = TextSendMessage(text='การใช้งานระบบ S-curve....')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="DPIS",user_msg=message) :
          Reply_object = TextSendMessage(text='การใช้งานระบบ DPIS....')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ERP",user_msg=message) :
          Reply_object = TextSendMessage(text='การใช้งานระบบ ERP....')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        else :
          Reply_object = TextSendMessage(text='ฉันไม่เข้าใจ โปรดระบุระบบสารสนเทศที่ท่านใช้งานอีกครั้งครับ',quick_reply=QuickReply(items=[
              QuickReplyButton(action=MessageAction(label="ระบบสารบรรณ", text="ระบบสารบรรณ")),
              QuickReplyButton(action=MessageAction(label="ระบบใบลา", text="ระบบใบลา")),
              QuickReplyButton(action=MessageAction(label="ระบบหนังสือเวียน", text="ระบบหนังสือเวียน")),
              QuickReplyButton(action=MessageAction(label="ระบบ S-curve", text="ระบบ S-curve")),
              QuickReplyButton(action=MessageAction(label="ระบบ DPIS", text="ระบบ DPIS")),
              QuickReplyButton(action=MessageAction(label="ระบบ ERP", text="ระบบ ERP")),
            ]))
          line_bot_api.reply_message(Reply_token, Reply_object)

      elif user_session == 3 :
        Reply_object = TextSendMessage(text='โปรดระบุวันที่ในการประชุมครับ (เช่น 15/01/2021)')
        line_bot_api.reply_message(Reply_token, Reply_object)
        put_user_session(uid=userID,data={"Session": 3.1},firebase_app=firebase,db_name="User Session")
      elif user_session == 3.1 :
        Reply_object = TextSendMessage(text='โปรดระบุเวลาการประชุม (เช่น 09:00-15:30)')
        line_bot_api.reply_message(Reply_token, Reply_object)
        put_user_session(uid=userID,data={"Session": 3.2},firebase_app=firebase,db_name="User Session")
      elif user_session == 3.2 :
        Reply_object = TextSendMessage(text='โปรดระบุสถานที่ประชุม (เช่น ห้องประชุมชั้น5 อาคารพระจอมเกล้า)')
        line_bot_api.reply_message(Reply_token, Reply_object)
        put_user_session(uid=userID,data={"Session": 3.3},firebase_app=firebase,db_name="User Session")
      elif user_session == 3.3 :
        Reply_object = TextSendMessage(text='โปรดระบุว่าต้องการใช้อุปกรณ์การประชุมหรือไม่ (ต้องการ หรือ ไม่ต้องการ)')
        line_bot_api.reply_message(Reply_token, Reply_object)
        put_user_session(uid=userID,data={"Session": 3.4},firebase_app=firebase,db_name="User Session")
      elif user_session == 3.4 :
        Reply_object = TextSendMessage(text='ผลลัพธ์จากการขอใช้ zoom')
        line_bot_api.reply_message(Reply_token, Reply_object)
        put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")

      elif user_session == 4 :
        Reply_object = TextSendMessage(text='ได้ดำเนินการเรียกเจ้าหน้าที่แล้ว กรุณารอสักครู่ครับ')
        line_bot_api.reply_message(Reply_token, Reply_object)
        put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")


      # elif message :
      #   Label_message = myPredict(message)
      #   if Label_message == "ทักทาย" :
      #     Reply_message = "สวัสดีครับ K'" + user_name +"\n" + " IT Support ยินดีให้บริการครับ"
      #     Reply_object = TextSendMessage(text=Reply_message)
      #     line_bot_api.reply_message(Reply_token, Reply_object)
      #   elif Label_message == "เสร็จสิ้นและขอบคุณ" :
      #     Reply_message = "IT Support ยินดีให้บริการครับ ขอบคุณครับ"
      #     Reply_object = TextSendMessage(text=Reply_message)
      #     line_bot_api.reply_message(Reply_token, Reply_object)
      #   elif Label_message == "Video Conference" :
      #     Reply_message = "ถ้าท่านต้องการใช้งานระบบ Video Conference"+"\n"+"โปรดแจ้งรายละเอียด ดังนี้"+"\n"+"ชื่อการประชุม วันที่ เวลา และต้องการอุปกรณ์สำหรับประชุม Video Conference หรือไม่"
      #     Reply_object = TextSendMessage(text=Reply_message)
      #     line_bot_api.reply_message(Reply_token, Reply_object)
      #   elif Label_message == "ระบบ E-Budget" :
      #     Reply_message = "http://budget.mhesi.go.th/"
      #     Reply_object = TextSendMessage(text=Reply_message)
      #     line_bot_api.reply_message(Reply_token, Reply_object)
      #   elif Label_message == "ระบบ VPN" :
      #     Reply_message = "ท่านสามารถใช้งานผ่าน Web Browser ได้ที่ลิงก์ https://vpn.mhesi.go.th/dana-na/auth/url_3/welcome.cgi"
      #     Reply_object = TextSendMessage(text=Reply_message)
      #     line_bot_api.reply_message(Reply_token, Reply_object)
      #   elif Label_message == "ระบบ ERP" :
      #     Reply_message = "สามารถใช้งานได้ผ่าน https://erp.mhesi.go.th/"
      #     Reply_object = TextSendMessage(text=Reply_message)
      #     line_bot_api.reply_message(Reply_token, Reply_object)
      #   elif Label_message == "Share Drive" :
      #     Reply_message = "รบกวนตรวจสอบอินเทอร์เน็ตและ Reboot Computer 1 ครั้งครับ"
      #     Reply_object = TextSendMessage(text=Reply_message)
      #     line_bot_api.reply_message(Reply_token, Reply_object)
      #   elif Label_message == "Back Office System" :
      #     Reply_object = TextSendMessage(text='โปรดระบุระบบ Back Office ที่ท่านใช้งานครับ',quick_reply=QuickReply(items=[
      #       QuickReplyButton(action=MessageAction(label="ระบบสารบรรณ", text="ระบบสารบรรณ")),
      #       QuickReplyButton(action=MessageAction(label="ระบบใบลา", text="ระบบใบลา")),
      #       QuickReplyButton(action=MessageAction(label="ระบบหนังสือเวียน", text="ระบบหนังสือเวียน")),
      #       QuickReplyButton(action=MessageAction(label="ระบบ S-curve", text="ระบบ S-curve")),
      #       QuickReplyButton(action=MessageAction(label="ระบบ DPIS", text="ระบบ DPIS")),
      #     ]))
      #     line_bot_api.reply_message(Reply_token, Reply_object)
      #   elif Label_message == "Email" :
      #     Reply_message = "สามารถใช้งานได้ที่ webmail.mhesi.go.th"
      #     Reply_object = TextSendMessage(text=Reply_message)
      #     line_bot_api.reply_message(Reply_token, Reply_object)
      #   elif Label_message == "Internet" :
      #     Reply_message = "เจ้าหน้าที่ขออนุญาตตรวจสอบสักครู่ครับ ขอบคุณครับ"
      #     Reply_object = TextSendMessage(text=Reply_message)
      #     line_bot_api.reply_message(Reply_token, Reply_object)
      #   elif Label_message == "Network Security" :
      #     Reply_message = "รับทราบครับ เดี๋ยวเจ้าหน้าที่ดำเนินการตรวจสอบให้ครับ"
      #     Reply_object = TextSendMessage(text=Reply_message)
      #     line_bot_api.reply_message(Reply_token, Reply_object)
      #   elif Label_message == "เครื่องแม่ข่าย VM & Server" :
      #     Reply_message = "รับทราบครับ เดี๋ยวเจ้าหน้าที่ดำเนินการตรวจสอบให้ครับ"
      #     Reply_object = TextSendMessage(text=Reply_message)
      #     line_bot_api.reply_message(Reply_token, Reply_object)
      #   elif Label_message == "Printer & Scanner" :
      #     Reply_message = "รับทราบครับ เดี๋ยวเจ้าหน้าที่จะดำเนินการติดตั้งหรือแก้ปัญหาเครื่อง Printer/Scanner ของท่านให้ครับ"
      #     Reply_object = TextSendMessage(text=Reply_message)
      #     line_bot_api.reply_message(Reply_token, Reply_object)
      #   elif Label_message == "ปัญหา Computer" :
      #     Reply_message = "รับทราบครับ เจ้าหน้าที่ขออนุญาตตรวจสอบสักครู่ครับ"
      #     Reply_object = TextSendMessage(text=Reply_message)
      #     line_bot_api.reply_message(Reply_token, Reply_object)
      #   elif Label_message == "ยืมคืน Accessory" :
      #     Reply_message = "IT Support มีเครื่องคอมพิวเตอร์ Notebook สำหรับให้บริการชั่วคราวเพียงอย่างเดียวครับ"+"\n"+"สามารถแจ้งเราได้เลยครับ ว่าท่านต้องการกี่เครื่อง ใช้เพื่อวัตถุประสงค์อะไร ระยะเวลาในการยืม"
      #     Reply_object = TextSendMessage(text=Reply_message)
      #     line_bot_api.reply_message(Reply_token, Reply_object)
    else:
      Reply_object = StickerSendMessage(package_id=str(1),sticker_id=str(2))
      line_bot_api.reply_message(Reply_token, Reply_object)

if __name__ == '__main__':
    app.run(debug=True)

    # if message == "รบกวนขอใช้งานระบบประชุมออนไลน์ (Zoom) ครับ/ค่ะ" :
      #   Reply_object = TextSendMessage(text='โปรดระบุชื่อการประชุมครับ')
      #   line_bot_api.reply_message(Reply_token, Reply_object)
      # else :
      #   Reply_object = TextSendMessage(text='โปรดระบุวันที่ในการประชุมครับ')
      #   line_bot_api.reply_message(Reply_token, Reply_object)
      #โปรดระบุชื่อการประชุมครับ โปรดระบุวันที่ในการประชุมครับ (เช่น 15/01/2021) โปรดระบุเวลาการประชุม (เช่น 09:00-15:30) โปรดระบุสถานที่ประชุม (เช่น ห้องประชุมชั้น5 อาคารพระจอมเกล้า) โปรดระบุว่าต้องการใช้อุปกรณ์การประชุมหรือไม่
      #'รับทราบครับ เดี๋ยวเจ้าหน้าที่จะดำเนินการส่ง Link ห้องประชุมให้ครับ'+'\n\n' +'โดยมีรายละเอียดการประชุม ดังนี้'+'\n' +'Topic: การประชุมคณะกรรมการตรวจสอบ ครั้งที่1-1/2564'+'\n' +'วันที่: 21/02/2021 เวลา 08:30-17:00 น.'+'\n' +'สถานที่: ห้องประชุมชั้น3 อาคาระพระจอมเกล้า'+'\n' +'อุปกรณ์: ต้องการ'