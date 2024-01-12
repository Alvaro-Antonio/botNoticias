from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import sys

from json import dumps
from httplib2 import Http

try:
    print("Capturando Noticias...\n")
    html = urlopen("https://g1.globo.com/tecnologia/")
except HTTPError as e:
    print(e)
except URLError:
    print("Server down or incorrect domain")
else:
    print("Capturando informações...\n")
    res = BeautifulSoup(html.read(), "html5lib")
    tags = res.findAll("a", {"class": "feed-post-link"})
    
    resumes = res.findAll('div',{"class" : "feed-post-body-resumo"})
  
    pictures = res.findAll('img', {"class" : "bstn-fd-picture-image"})
    

    cards = []

    lenth = 0

    print("Processando Noticias...\n")

    for tag in tags:
        print(f'Noticía {lenth + 1} \n')

        title = "<a href=\"" + tag['href'] + "\" ><h1 color=blue >"+tag.getText() + "</h1></a>"
        subtitle = ""

        try:
            subtitle =resumes[lenth].p.string
        except:
            subtitle = ""

        image = pictures[lenth]['src']
        altImage = pictures[lenth]['alt']

        card = {
                "cardId": title,
                "card": {                    
                    "sections": [
                      {
                        "header": title,
                        "collapsible": False,
                        "uncollapsibleWidgetsCount": 0,
                        "widgets": [
                          {
                            "textParagraph": {
                              "text":  "<i>" + subtitle + "</i>" 
                            }
                          },
                          {
                            "image": {
                              "imageUrl": image,
                              "altText": altImage
                            }
                          }
                        ]
                      }
                    ]
                },
              }

        cards.append(card)
        lenth += 1

    """webhook do chat."""

    sys.path.append("urlRoomChat.py") #importanto url da sala do chat
    from urlRoomChat import urlPath
    url = urlPath

    bot_message = {
      "cardsV2": [
      ],
    }
    print("Montando Cards de Noticias...\n")
    for c in cards:
      bot_message["cardsV2"].append(c)


    #print(bot_message)  

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()

    print("Enviando ...\n")

    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    #print(response)
    print("Finalizado...")