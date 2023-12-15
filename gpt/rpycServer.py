import sys
sys.path.append('/src')
from gpt import getAiResp

import rpyc
from rpyc.utils.server import ThreadedServer # or ForkingServer

@rpyc.service
class gptService(rpyc.Service):
    @rpyc.exposed
    def getAiResp(self, message_text):
        getAiResp(message_text)

if __name__ == "__main__":
    server = ThreadedServer(gptService, port = 12345)
    server.start()