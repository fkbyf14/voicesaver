"""Config values for archivebot."""
import os


class Config:
    TOKEN = os.getenv('TOKEN')
    NAME = "voicesaver"

    REQUEST_KWARGS = {
        'proxy_url': "socks4://35.163.3.95:8080"
    }

    WEBHOOK = False
    IP = '0.0.0.0'
    PORT = 8080
    URL_PATH = TOKEN
    WEBHOOK_URL = 'https://example.com/%s' % (URL_PATH,)


config = Config()
