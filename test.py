from flask import Flask, request, abort
from use_model import myPredict, lamda_l
from firebase import firebase
from connect_firebase

import requests
import json
app = Flask(__name__)
@app.route('/', methods=['POST','GET'])

def webhook():
  if request.method == 'POST':
    payload = request.json
    Reply_token = payload['events'][0]['replyToken']
    print(Reply_token)
    message = payload['events'][0]['message']['text']
    # print(message)
    if message :
      Label_messasge = myPredict(message)
      if Label_messasge == "ทักทาย" :
        Reply_messasge = "สวัสดีครับ IT Support ยินดีให้บริการครับ"
      elif Label_messasge == "เสร็จสิ้นและขอบคุณ" :
        Reply_messasge = "IT Support ยินดีให้บริการครับ ขอบคุณครับ"
      elif Label_messasge == "Video Conference" :
        Reply_messasge = "ถ้าท่านต้องการใช้งานระบบ Video Conference"+"\n"+"โปรดแจ้งรายละเอียด ดังนี้"+"\n"+"ชื่อการประชุม วันที่ เวลา และต้องการอุปกรณ์สำหรับประชุม Video Conference หรือไม่"
      elif Label_messasge == "ระบบ E-Budget" :
        Reply_messasge = "Test"
      elif Label_messasge == "ระบบ VPN" :
        Reply_messasge = "ท่านสามารถใช้งานผ่าน Web Browser ได้ที่ลิงก์ https://vpn.mhesi.go.th/dana-na/auth/url_3/welcome.cgi"
      elif Label_messasge == "ระบบ ERP" :
        Reply_messasge = "สามารถใช้ฃานได้ผ่าน https://erp.mhesi.go.th/"
      elif Label_messasge == "Share Drive" :
        Reply_messasge = "Test"
      elif Label_messasge == "Back Office System" :
        Reply_messasge = "Test"
      elif Label_messasge == "Email" :
        Reply_messasge = "สามารถใช้งานได้ที่ webmail.mhesi.go.th"
      elif Label_messasge == "Internet" :
        Reply_messasge = "Test"
      elif Label_messasge == "Network Security" :
        Reply_messasge = "Test"
      elif Label_messasge == "เครื่องแม่ข่าย VM & Server" :
        Reply_messasge = "Test"
      elif Label_messasge == "Printer & Scanner" :
        Reply_messasge = "รับทราบครับ เดี๋ยวเจ้าหน้าที่จะดำเนินการติดตั้งหรือแก้ปัญหาเครื่อง Printer/Scanner ของท่านให้ครับ"
      elif Label_messasge == "ปัญหา Computer" :
        Reply_messasge = "Test"
      elif Label_messasge == "ยืมคืน Accessory" :
        Reply_messasge = "Test"
      ReplyMessage(Reply_token,Reply_messasge)
      return request.json, 200
  else:
    abort(400)

def ReplyMessage(Reply_token, TextMessage):
  LINE_API = 'https://api.line.me/v2/bot/message/reply'

  Authorization = 'Bearer {}'.format('CxoEeTecHEIzApUgMPohAgQALqbSi/i0xq0Qx16YGDjwyqSXUXbtbul7oA8t1EiF6Ti+ylCs3JRmMLhBAyWP3l8r8KoCrPymAt4F+6j0AqO5Dg7ArwsY0YRgN+trYbjUyvbPqywXerDtCBGIbOAd/AdB04t89/1O/w1cDnyilFU=')
  print(Authorization)
  headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Authorization':Authorization
  }
  data = {
    "replyToken":Reply_token,
    "messages":[
      {
        "type":"text",
        "text":TextMessage,
        "quickReply": {
          "items": [
            {
              "type": "action",
              "action": {
                "type": "message",
                "label": "สวัสดี",
                "text": "Hello World!"
              }
            }
          ]
        }
      }
    ]
  }
  data = json.dumps(data)
  r = requests.post(LINE_API, headers=headers, data=data)
  return 200

if __name__ == '__main__':
  app.run(debug=True)