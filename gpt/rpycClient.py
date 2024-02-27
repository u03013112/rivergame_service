import rpyc
import json

conn = rpyc.connect("127.0.0.1", 12345)
message = [
    {"role":"system","content":"You are an AI assistant that helps people find information."},
    {"role":"user","content":"你好"}
]
# x = conn.root.getAiResp(message)
message_str = json.dumps(message)  # 将message转换为字符串
x = conn.root.getAiResp(message_str)  # 传递字符串而非原始对象
print(x)