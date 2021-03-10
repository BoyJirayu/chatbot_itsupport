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
            "color": "#FFC500"
          }
        ],
        "backgroundColor": "#5A5A5A"
      },
      "hero": {
        "type": "image",
        "url": "%s",
        "size": "xxl",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        },
        "offsetTop": "none",
        "offsetBottom": "none",
        "offsetStart": "none",
        "offsetEnd": "none",
        "margin": "none",
        "backgroundColor": "#FFDF8A"
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
            "color": "#FFC500"
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
                    "color": "#FFFFFF",
                    "size": "sm",
                    "flex": 2
                  },
                  {
                    "type": "text",
                    "text": "02-333-3700 ต่อ 1111",
                    "wrap": true,
                    "color": "#D5D5D5",
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
                    "color": "#FFFFFF",
                    "size": "sm",
                    "flex": 2
                  },
                  {
                    "type": "text",
                    "text": "it.support@mhesi.go.th",
                    "wrap": true,
                    "color": "#D5D5D5",
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
                    "color": "#FFFFFF",
                    "size": "sm"
                  },
                  {
                    "type": "text",
                    "text": "@it-support",
                    "flex": 5,
                    "color": "#D5D5D5",
                    "size": "sm"
                  }
                ]
              }
            ]
          }
        ],
        "backgroundColor": "#5A5A5A"
      },
      "styles": {
        "hero": {
          "backgroundColor": "#5A5A5A"
        }
      }
    }'''%(name,pic)
  return flex