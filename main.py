from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import sys

from json import dumps
from httplib2 import Http

try:
    html = urlopen("https://g1.globo.com/tecnologia/")
except HTTPError as e:
    print(e)
except URLError:
    print("Server down or incorrect domain")
else:
    res = BeautifulSoup(html.read(), "html5lib")
    tags = res.findAll("a", {"class": "feed-post-link"})
    links = res.findAll('a', href=True)
    titulos = ""

    for tag in tags:
        print(tag.getText())
        titulos += "<" + tag['href'] + "|"+tag.getText() + ">\n\n"

    """webhook do chat."""

    sys.path.append("urlRoomChat.py") #importanto url da sala do chat
    from urlRoomChat import urlPath
    url = urlPath

    bot_message = {
        'text': titulos,
    }
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    print(response)