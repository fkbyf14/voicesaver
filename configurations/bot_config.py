import os

TOKEN = os.getenv('TOKEN')
NAME = "voicesaver"

REQUEST_KWARGS = {
    'proxy_url': "socks4://23.180.0.14:32409"
}

WEBHOOK = True
## The following configuration is only needed if you setted WEBHOOK to True ##
IP = '172.30.138.233'
PORT = 8080
URL_PATH = TOKEN
WEBHOOK_URL = 'http://voicesaver-voicesaver.1d35.starter-us-east-1.openshiftapps.com/' % (URL_PATH,)
