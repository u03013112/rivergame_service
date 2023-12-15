import sys
sys.path.append('/src')
from feishu import sendMessageDebug

import rpyc
from rpyc.utils.server import ThreadedServer # or ForkingServer

@rpyc.service
class feishuService(rpyc.Service):
    @rpyc.exposed
    def sendMessageDebug(self, message):
        sendMessageDebug(message)

if __name__ == "__main__":
    server = ThreadedServer(feishuService, port = 12345)
    server.start()