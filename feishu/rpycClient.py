import rpyc

conn = rpyc.connect("127.0.0.1", 12345)
x = conn.root.sendMessageDebug("Hello, World!")