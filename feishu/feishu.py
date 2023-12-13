import os
import json
import sys
sys.path.append('/src')

from config import fsAppId,fsAppSecret

import requests
from requests_toolbelt import MultipartEncoder

def getTenantAccessToken():
    url = f'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/'
    headers = {
        'Content-Type':'application/json'
    }
    data = {
        'app_id':fsAppId,
        'app_secret':fsAppSecret
    }
    r = requests.post(url,headers=headers,json=data)
    return r.json()['tenant_access_token']

def sendMessage(tenantAccessToken,message,chatId = 'oc_3e59fcc0d068e649245cee2478d6a8b9'):
    url = f'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id'
    headers = {
        'Authorization': f'Bearer {tenantAccessToken}',
        'Content-Type': 'application/json'
    }
    content = json.dumps({"text": message})
    data = {
        'receive_id':chatId,
        'msg_type':'text',
        'content':content
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print('data:',data)
        raise Exception(f"sendMessage Error: {response.status_code}, {response.text}")
    
    
    return response.json()
    
def sendMessageDebug(message):
    token = getTenantAccessToken()
    sendMessage(token,message,'oc_1e418dff75881d2b0d85a5f701262cb8')

if __name__ == '__main__':
    sendMessageDebug('test')
