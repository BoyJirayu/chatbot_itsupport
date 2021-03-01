from flask import Flask
app = Flask(__name__)
@app.route('/')
def MainFunction():
    return 'Hello world'
if __name__ == '__main__':
    app.run()

# from flask import Flask, request, abort
# import requests
# import json
# app = Flask(__name__)
# @app.route('/', methods=['POST','GET'])

# def webhook():
#   if request.method == 'POST':
#     payload = request.json
#     Reply_token = payload['events'][0]['replyToken']
#     print(Reply_token)
#     message = payload['events'][0]['message']['text']
#     print(message)
#     if 'ดี' in message :
#       Reply_messasge = 'ดีมาก'
#       ReplyMessage(Reply_token,Reply_messasge,'CxoEeTecHEIzApUgMPohAgQALqbSi/i0xq0Qx16YGDjwyqSXUXbtbul7oA8t1EiF6Ti+ylCs3JRmMLhBAyWP3l8r8KoCrPymAt4F+6j0AqO5Dg7ArwsY0YRgN+trYbjUyvbPqywXerDtCBGIbOAd/AdB04t89/1O/w1cDnyilFU=') #ใส่ Channel access token
#       return request.json, 200
#   else:
#     abort(400)

# def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
#   LINE_API = 'https://api.line.me/v2/bot/message/reply'

#   Authorization = 'Bearer {}'.format(Line_Acees_Token)
#   print(Authorization)
#   headers = {
#     'Content-Type': 'application/json; charset=UTF-8',
#     'Authorization':Authorization
#   }
#   data = {
#     "replyToken":Reply_token,
#     "messages":[{
#       "type":"text",
#       "text":TextMessage
#     }]
#   }
#   data = json.dumps(data)
#   r = requests.post(LINE_API, headers=headers, data=data)
#   return 200

# if __name__ == '__main__':
#   app.run(debug=True)