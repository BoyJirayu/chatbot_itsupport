from flask import Flask, jsonify, render_template, request
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageSendMessage,FlexSendMessage, StickerSendMessage, AudioSendMessage, QuickReply, QuickReplyButton, MessageAction
from linebot.models.template import *
from linebot import LineBotApi, WebhookHandler
from use_model import myPredict, lamda_l
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
              QuickReplyButton(action=MessageAction(label="Email", text="Email")),
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
              QuickReplyButton(action=MessageAction(label="ระบบ Scurve", text="ระบบ Scurve")),
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
          Reply_object = TextSendMessage(text="โปรดระบุปัญหาของท่านให้เจ้าหน้าที่ทราบ")
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 4},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ขอเบอร์หรือช่องทางการติดต่อ IT Support ครับ",user_msg=message) :
          flex = contact_card(name=user_name,pic=user_pic)
          flex = json.loads(flex)
          Reply_object = FlexSendMessage(alt_text='Flex Message',contents=flex)
          line_bot_api.reply_message(Reply_token, Reply_object)
        elif match_menu90(def_msg="ระบบ",user_msg=message) :
          Reply_object = TextSendMessage(text='ฉันไม่เข้าใจ โปรดให้รายละเอียดกับเราอีกครั้งครับ')
          line_bot_api.reply_message(Reply_token, Reply_object)
        
        elif message :
          Label_message = myPredict(message)
          if Label_message == "ทักทาย" :
            Reply_message = "สวัสดีครับ K'" + user_name +"\n" + " IT Support ยินดีให้บริการครับ"
            Reply_object = TextSendMessage(text=Reply_message)
            line_bot_api.reply_message(Reply_token, Reply_object)
          elif Label_message == "เสร็จสิ้นและขอบคุณ" :
            Reply_message = "IT Support ยินดีให้บริการครับ"
            Reply_object = TextSendMessage(text=Reply_message)
            line_bot_api.reply_message(Reply_token, Reply_object)
          elif Label_message == "Video Conference" :
            Reply_object = TextSendMessage(text="โปรดระบุชื่อการประชุมครับ")
            line_bot_api.reply_message(Reply_token, Reply_object)
            put_user_session(uid=userID,data={"Session": 3},firebase_app=firebase,db_name="User Session")
          elif Label_message == "ระบบ E-Budget" :
            Reply_message = "ท่านสามารถเข้าใช้งานได้ที่ http://budget.mhesi.go.th/ \nแต่หากท่านยังคงมีปัญหา โปรดกดเมนูเรียกเจ้าหน้าที่ครับ"
            Reply_object = TextSendMessage(text=Reply_message)
            line_bot_api.reply_message(Reply_token, Reply_object)
          elif Label_message == "ระบบ VPN" :
            Reply_object = TextSendMessage(text='วิดีโอการใช้งานระบบ VPN ตามลิงก์ด้านล่างครับ\nhttps://iptv.mhesi.go.th/website/video/detail/1076 \n\nวิดีโอการติดตั้งโปรแกรม Pulse Secure เพื่อใช้งาน VPN ตามลิงก์ด้านล่างครับ\nhttps://iptv.mhesi.go.th/website/video/detail/1074')
            line_bot_api.reply_message(Reply_token, Reply_object)
          elif Label_message == "ระบบ ERP" :
            Reply_object = TextSendMessage(text='วิดีโอการใช้งานระบบ ERP ตามลิงก์ด้านล่างครับ\nhttps://iptv.mhesi.go.th/website/video/detail/1075 \n\nหากท่านยังคงมีปัญหา โปรดกดเมนูเรียกเจ้าหน้าที่ครับ')
            line_bot_api.reply_message(Reply_token, Reply_object)
          elif Label_message == "Share Drive" :
            Reply_message = "วิดีโอการใช้งาน Share Drive ตามลิงก์ด้านล่างครับ\nhttps://iptv.mhesi.go.th/website/video/detail/1078 \n\nหากท่านกำลังใช้ระบบเครือข่ายของ สป.อว.\nโปรดรีสตาร์ทคอมพิวเตอร์ 1 ครั้งครับ"
            Reply_object = TextSendMessage(text=Reply_message)
            line_bot_api.reply_message(Reply_token, Reply_object)
          elif Label_message == "Back Office System" :
            Reply_object = TextSendMessage(text='โปรดระบุระบบ Back Office ที่ท่านใช้งานครับ',quick_reply=QuickReply(items=[
              QuickReplyButton(action=MessageAction(label="ระบบสารบรรณ", text="ระบบสารบรรณ")),
              QuickReplyButton(action=MessageAction(label="ระบบใบลา", text="ระบบใบลา")),
              QuickReplyButton(action=MessageAction(label="ระบบหนังสือเวียน", text="ระบบหนังสือเวียน")),
              QuickReplyButton(action=MessageAction(label="ระบบ S-curve", text="ระบบ S-curve")),
              QuickReplyButton(action=MessageAction(label="ระบบ DPIS", text="ระบบ DPIS")),
              QuickReplyButton(action=MessageAction(label="ระบบ ERP", text="ระบบ ERP")),
              QuickReplyButton(action=MessageAction(label="ระบบ E-Budget", text="ระบบ E-Budget")),
            ]))
            line_bot_api.reply_message(Reply_token, Reply_object)
            put_user_session(uid=userID,data={"Session": 2},firebase_app=firebase,db_name="User Session")
          elif Label_message == "Email" :
            Reply_message = "อีเมลสามารถใช้งานได้ที่ \nhttps://webmail.mhesi.go.th \nหากท่านมีปัญหาการใช้งานโปรดกดปุ่มเรียกเจ้าหน้าที่"
            Reply_object = TextSendMessage(text=Reply_message)
            line_bot_api.reply_message(Reply_token, Reply_object)
          elif Label_message == "Internet" :
            Reply_object = TextSendMessage(text="โปรดระบุปัญหาการใช้งานอินเทอร์เน็ตของท่านให้เจ้าหน้าที่ทราบ")
            line_bot_api.reply_message(Reply_token, Reply_object)
            put_user_session(uid=userID,data={"Session": 4},firebase_app=firebase,db_name="User Session")
          elif Label_message == "Network Security" :
            Reply_message = "รับทราบครับ เดี๋ยวเจ้าหน้าที่ดำเนินการตรวจสอบปัญหาของท่านให้ครับ"
            Reply_object = TextSendMessage(text=Reply_message)
            line_bot_api.reply_message(Reply_token, Reply_object)
            line_notify_NetworkSec(name=user_name,problem=problem)
          elif Label_message == "เครื่องแม่ข่าย VM & Server" :
            Reply_message = "รับทราบครับ เดี๋ยวเจ้าหน้าที่ดำเนินการตรวจสอบให้ครับ"
            Reply_object = TextSendMessage(text=Reply_message)
            line_bot_api.reply_message(Reply_token, Reply_object)
            line_notify_ServerVM(name=user_name,problem=problem)
          elif Label_message == "Printer & Scanner" :
            Reply_object = TextSendMessage(text="โปรดระบุปัญหาการใช้งานเครื่องปริ้นเตอร์และสแกนเนอร์ของท่านให้เจ้าหน้าที่ทราบ")
            line_bot_api.reply_message(Reply_token, Reply_object)
            put_user_session(uid=userID,data={"Session": 4},firebase_app=firebase,db_name="User Session")
          elif Label_message == "ปัญหา Computer" :
            Reply_object = TextSendMessage(text="โปรดระบุปัญหาการใช้งานคอมพิวเตอร์ของท่านให้เจ้าหน้าที่ทราบ")
            line_bot_api.reply_message(Reply_token, Reply_object)
            put_user_session(uid=userID,data={"Session": 4},firebase_app=firebase,db_name="User Session")
          elif Label_message == "ยืมคืน Accessory" :
            Reply_message = "IT Support มีเครื่องคอมพิวเตอร์ Notebook สำหรับให้บริการชั่วคราวเพียงอย่างเดียวครับ"+"\n"+"สามารถแจ้งเราได้เลยครับ ว่าท่านต้องการกี่เครื่อง ใช้เพื่อวัตถุประสงค์อะไร และระยะเวลาในการยืม"
            Reply_object = TextSendMessage(text=Reply_message)
            line_bot_api.reply_message(Reply_token, Reply_object)
            put_user_session(uid=userID,data={"Session": 5},firebase_app=firebase,db_name="User Session")

      elif user_session == 1 :
        if match_menu(def_msg="ปัญหาการใช้งาน VPN",user_msg=message) :
          Reply_object = TextSendMessage(text='วิดีโอการใช้งานระบบ VPN ตามลิงก์ด้านล่างครับ\nhttps://iptv.mhesi.go.th/website/video/detail/1076 \n\nวิดีโอการติดตั้งโปรแกรม Pulse Secure เพื่อใช้งาน VPN ตามลิงก์ด้านล่างครับ\nhttps://iptv.mhesi.go.th/website/video/detail/1074')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ปัญหาการใช้งาน Share Drive",user_msg=message) :
          Reply_message = "วิดีโอการใช้งาน Share Drive ตามลิงก์ด้านล่างครับ\nhttps://iptv.mhesi.go.th/website/video/detail/1078 \n\nหากท่านกำลังใช้ระบบเครือข่ายของ สป.อว.\nโปรดรีสตาร์ทคอมพิวเตอร์ 1 ครั้งครับ"
          Reply_object = TextSendMessage(text=Reply_message)
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="การใช้งานอีเมล Email ",user_msg=message) :
          Reply_message = "อีเมลสามารถใช้งานได้ที่ https://webmail.mhesi.go.th \nหากท่านมีปัญหาการใช้งานโปรดกดปุ่มเรียกเจ้าหน้าที่"
          Reply_object = TextSendMessage(text=Reply_message)
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ปัญหาการใช้งาน Internet",user_msg=message) :
          Reply_object = TextSendMessage(text="โปรดระบุปัญหาการใช้งานอินเทอร์เน็ตของท่านให้เจ้าหน้าที่ทราบ")
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 4},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ปัญหาการใช้งาน Printer & Scanner",user_msg=message) :
          Reply_object = TextSendMessage(text="โปรดระบุปัญหาการใช้งานเครื่องปริ้นเตอร์และสแกนเนอร์ของท่านให้เจ้าหน้าที่ทราบ")
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 4},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ปัญหาการใช้งานเครื่องคอมพิวเตอร์ computer",user_msg=message) :
          Reply_object = TextSendMessage(text="โปรดระบุปัญหาการใช้งานคอมพิวเตอร์ของท่านให้เจ้าหน้าที่ทราบ")
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 4},firebase_app=firebase,db_name="User Session")
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
          Reply_object = TextSendMessage(text='โปรดดูวิดีโอการใช้งานระบบสารบรรณตามลิงก์ด้านล่างครับ\nhttps://iptv.mhesi.go.th/website/video/detail/1206 \n\nหากท่านยังคงมีปัญหา โปรดกดเมนูเรียกเจ้าหน้าที่ครับ')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ระบบใบลา",user_msg=message) :
          Reply_object = TextSendMessage(text='โปรดดูวิดีโอการใช้งานระบบใบลาตามลิงก์ด้านล่างครับ\nhttps://iptv.mhesi.go.th/website/video/detail/1142 \n\nหากท่านยังคงมีปัญหา โปรดกดเมนูเรียกเจ้าหน้าที่ครับ')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ระบบหนังสือเวียน",user_msg=message) :
          Reply_object = TextSendMessage(text='โปรดดูวิดีโอการใช้งานระบบหนังสือเวียนตามลิงก์ด้านล่างครับ\nhttps://iptv.mhesi.go.th/website/video/detail/1140 \n\nหากท่านยังคงมีปัญหา โปรดกดเมนูเรียกเจ้าหน้าที่ครับ')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="Scurve",user_msg=message) :
          Reply_object = TextSendMessage(text='ท่านสามารถใช้งานระบบ Scurve ได้ที่\nhttp://scurve.mhesi.go.th/ \n\nหากท่านยังคงมีปัญหาการใช้งานระบบ Scurve โปรดกดเมนูเรียกเจ้าหน้าที่ครับ')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="DPIS",user_msg=message) :
          Reply_object = TextSendMessage(text='ท่านสามารถใช้งานระบบ DPIS ได้ที่\nhttp://dpis.mhesi.go.th/ \n\nหากท่านยังคงมีปัญหาการใช้งานระบบ DPIS โปรดกดเมนูเรียกเจ้าหน้าที่ครับ')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="ERP",user_msg=message) :
          Reply_object = TextSendMessage(text='โปรดดูวิดีโอการใช้งานระบบ ERP ตามลิงก์ด้านล่างครับ\nhttps://iptv.mhesi.go.th/website/video/detail/1075 \n\nหากท่านยังคงมีปัญหา โปรดกดเมนูเรียกเจ้าหน้าที่ครับ')
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        elif match_menu(def_msg="e-budget",user_msg=message) :
          Reply_object = TextSendMessage(text="ท่านสามารถเข้าใช้งานได้ที่ http://budget.mhesi.go.th/ \nแต่หากท่านยังคงมีปัญหา โปรดกดเมนูเรียกเจ้าหน้าที่ครับ")
          line_bot_api.reply_message(Reply_token, Reply_object)
          put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        else :
          Reply_object = TextSendMessage(text='ฉันไม่เข้าใจ โปรดระบุระบบสารสนเทศที่ท่านใช้งานอีกครั้งครับ',quick_reply=QuickReply(items=[
              QuickReplyButton(action=MessageAction(label="ระบบสารบรรณ", text="ระบบสารบรรณ")),
              QuickReplyButton(action=MessageAction(label="ระบบใบลา", text="ระบบใบลา")),
              QuickReplyButton(action=MessageAction(label="ระบบหนังสือเวียน", text="ระบบหนังสือเวียน")),
              QuickReplyButton(action=MessageAction(label="ระบบ Scurve", text="ระบบ Scurve")),
              QuickReplyButton(action=MessageAction(label="ระบบ DPIS", text="ระบบ DPIS")),
              QuickReplyButton(action=MessageAction(label="ระบบ ERP", text="ระบบ ERP")),
              QuickReplyButton(action=MessageAction(label="ระบบ E-Budget", text="ระบบ E-Budget")),
            ]))
          line_bot_api.reply_message(Reply_token, Reply_object)

      elif user_session == 3 :
        put_vcs(uid=userID,data={"Topic": message},firebase_app=firebase,db_name="Video Conference")
        Reply_object = TextSendMessage(text='โปรดระบุวันที่ในการประชุมครับ (เช่น 15/01/2021)')
        line_bot_api.reply_message(Reply_token, Reply_object)
        put_user_session(uid=userID,data={"Session": 3.1},firebase_app=firebase,db_name="User Session")
      elif user_session == 3.1 :
        put_vcs(uid=userID,data={"Date": message},firebase_app=firebase,db_name="Video Conference")
        Reply_object = TextSendMessage(text='โปรดระบุเวลาการประชุม (เช่น 09:00-15:30)')
        line_bot_api.reply_message(Reply_token, Reply_object)
        put_user_session(uid=userID,data={"Session": 3.2},firebase_app=firebase,db_name="User Session")
      elif user_session == 3.2 :
        put_vcs(uid=userID,data={"Time": message},firebase_app=firebase,db_name="Video Conference")
        Reply_object = TextSendMessage(text='โปรดระบุสถานที่ประชุม (เช่น ห้องประชุมชั้น5 อาคารพระจอมเกล้า)')
        line_bot_api.reply_message(Reply_token, Reply_object)
        put_user_session(uid=userID,data={"Session": 3.3},firebase_app=firebase,db_name="User Session")
      elif user_session == 3.3 :
        put_vcs(uid=userID,data={"Location": message},firebase_app=firebase,db_name="Video Conference")
        Reply_object = TextSendMessage(text='โปรดระบุว่าต้องการใช้อุปกรณ์การประชุมหรือไม่ (ต้องการ หรือ ไม่ต้องการ)')
        line_bot_api.reply_message(Reply_token, Reply_object)
        put_user_session(uid=userID,data={"Session": 3.4},firebase_app=firebase,db_name="User Session")
      elif user_session == 3.4 :
        put_vcs(uid=userID,data={"VCS_Device": message},firebase_app=firebase,db_name="Video Conference")
        vcs = get(uid=userID,firebase_app=firebase,db_name="Video Conference")
        Reply_object = TextSendMessage(text='กรุณารอสักครู่ครับ เจ้าหน้าที่กำลังดำเนินการสร้างลิงก์สำหรับการประชุมให้ครับ โดยมีรายละเอียดดังนี้\n\nชื่อประชุม: '+vcs["Topic"]+'\nวันที่ประชุม: '+vcs["Date"]+' เวลา '+vcs["Time"]+' น. \nสถานที่:'+vcs["Location"]+'\nติดตั้งอุปกรณ์: '+vcs["VCS_Device"]+'\n\nและท่านสามารถดูวิดีโอการใช้งาน Zoom ได้ดังลิงก์ด้านล่างนี้ครับ\nhttps://iptv.mhesi.go.th/website/video/detail/1134')
        line_bot_api.reply_message(Reply_token, Reply_object)
        put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")
        conference_line_notify(name=user_name,topic=vcs["Topic"],date=vcs["Date"],time=vcs["Time"],location=vcs["Location"],vcs_device=vcs["VCS_Device"])

      elif user_session == 4 :
        put_problem_for_emp(uid=userID,data={"Problem": message},firebase_app=firebase,db_name="Call IT Support")
        Reply_object = TextSendMessage(text='ได้ดำเนินการเรียกเจ้าหน้าที่แล้ว กรุณารอสักครู่ครับ')
        line_bot_api.reply_message(Reply_token, Reply_object)
        problem = get(uid=userID,firebase_app=firebase,db_name="Call IT Support")
        problem = problem["Problem"]
        line_notify(name=user_name,problem=problem)
        put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")

      elif user_session == 5 :
        put_problem_for_emp(uid=userID,data={"Detail": message},firebase_app=firebase,db_name="Need_Accessory")
        Reply_object = TextSendMessage(text='เจ้าหน้าที่ขอตรวจสอบสักครู่ครับ')
        line_bot_api.reply_message(Reply_token, Reply_object)
        detail = get(uid=userID,firebase_app=firebase,db_name="Need_Accessory")
        detail = detail["Detail"]
        line_notify_accessory(name=user_name,detail=detail)
        put_user_session(uid=userID,data={"Session": 0},firebase_app=firebase,db_name="User Session")

    else:
      if user_session == 0 :
        Reply_object = StickerSendMessage(package_id=str(1),sticker_id=str(2))
        line_bot_api.reply_message(Reply_token, Reply_object)
      else :
        Reply_object = TextSendMessage(text='ฉันไม่เข้าใจ โปรดให้รายละเอียดกับเราอีกครั้งครับ')
        line_bot_api.reply_message(Reply_token, Reply_object)

if __name__ == '__main__':
    app.run(debug=True)