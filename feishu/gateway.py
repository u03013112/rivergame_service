import sys
sys.path.append('/src')
from feishu import sendMessageDebug,sendMessageWithoutToken

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/sendMessageDebug', methods=['POST'])
def handle_post():
    data = request.get_json()
    if 'message' in data:
        message = data['message']
        sendMessageDebug(message)
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': 'No message in request'}), 400

@app.route('/sendMessageWithoutToken', methods=['POST'])
def handle_post():
    data = request.get_json()
    if 'message' in data and 'chatId' in data:
        message = data['message']
        chatId = data['chatId']
        sendMessageWithoutToken(message, chatId)
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': 'No message or chatId in request'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
