import requests
def contact_card(name,pic):
  flex = '''
    {
      "type": "bubble",
      "header": {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "สวัสดีครับ คุณ%s",
            "size": "md",
            "weight": "bold",
            "align": "center",
            "gravity": "center",
            "color": "#2F4F4F"
          }
        ],
        "backgroundColor": "#CCFFFF"
      },
      "hero": {
        "type": "image",
        "url": "%s",
        "size": "xxl",
        "aspectRatio": "20:13",
        "aspectMode": "fit",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        },
        "offsetTop": "none",
        "offsetBottom": "none",
        "offsetStart": "none",
        "offsetEnd": "none",
        "margin": "none"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "ช่องทางการติดต่อ IT Support",
            "weight": "bold",
            "size": "md",
            "margin": "none",
            "gravity": "center",
            "align": "center",
            "color": "#2F4F4F"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "md",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "Tel :",
                    "color": "#2F4F4F",
                    "size": "sm",
                    "flex": 2
                  },
                  {
                    "type": "text",
                    "text": "02-333-3700 ต่อ 1111",
                    "wrap": true,
                    "color": "#4682B4",
                    "size": "sm",
                    "flex": 5
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "E-mail :",
                    "color": "#2F4F4F",
                    "size": "sm",
                    "flex": 2
                  },
                  {
                    "type": "text",
                    "text": "it.support@mhesi.go.th",
                    "wrap": true,
                    "color": "#4682B4",
                    "size": "sm",
                    "flex": 5
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "Line :",
                    "flex": 2,
                    "color": "#2F4F4F",
                    "size": "sm"
                  },
                  {
                    "type": "text",
                    "text": "@it-support",
                    "flex": 5,
                    "color": "#4682B4",
                    "size": "sm"
                  }
                ]
              }
            ]
          }
        ],
        "backgroundColor": "#CCFFFF"
      },
      "styles": {
        "hero": {
          "backgroundColor": "#CCFFFF"
        }
      }
    }'''%(name,pic)
  return flex

def line_notify(name) :
  url = 'https://notify-api.line.me/api/notify'
  token = '2ZQUYSP1cYGQMg2j3aPfHIepEO3PkHO4yiqJkaJaT1w'
  headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

  msg = 'คุณ'+name+' เรียกเจ้าหน้าที่ IT Support ที่ Line Official ครับ'
  r = requests.post(url, headers=headers, data = {'message':msg})
  print (r.text)