import rpyc

conn = rpyc.connect("127.0.0.1", 12345)
message = [
    {"role":"system","content":"You are an AI assistant that helps people find information."},
    {"role":"user","content":"你好"}
]
x = conn.root.getAiResp(message)