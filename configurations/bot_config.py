import os

TOKEN = os.getenv('TOKEN')
NAME = "voicesaver"

REQUEST_KWARGS = {
    'proxy_url': "socks4://186.47.85.210:58722"
}

WEBHOOK = True
## The following configuration is only needed if you setted WEBHOOK to True ##
IP = '172.30.138.233'
PORT = 8080
URL_PATH = TOKEN
WEBHOOK_URL = ''
