import sys
sys.path.append('/src')
from gpt import getAiResp as getAiRespIn

import json
import rpyc
from rpyc.utils.server import ThreadedServer # or ForkingServer

@rpyc.service
class gptService(rpyc.Service):
    @rpyc.exposed
    def getAiResp(self, message_text):
        message = json.loads(message_text) 
        return getAiRespIn(message)

if __name__ == "__main__":
    server = ThreadedServer(gptService, port = 12345)
    server.start()