import os

TOKEN = os.getenv('TOKEN')
NAME = "voicesaver"

REQUEST_KWARGS = {
    'proxy_url': "socks4://23.180.0.14:32409"
}

WEBHOOK = True
## The following configuration is only needed if you setted WEBHOOK to True ##
IP = '0.0.0.0'
PORT = 443
URL_PATH = TOKEN # This is recommended for avoiding random people making fake updates to your bot
WEBHOOK_URL = 'https://example.com/%s' % (URL_PATH,)