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

def createDoc(tenantAccessToken,title,folder_token = 'RRlBfMuTglqODCdjmeYcoOVMn2f'):
    url = f'https://open.feishu.cn/open-apis/docx/v1/documents'
    headers = {
        'Authorization': f'Bearer {tenantAccessToken}',
        'Content-Type': 'application/json'
    }
    data = {
        'folder_token':folder_token,
        'title':title
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['data']['document']['document_id']
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

def addHead1(tenantAccessToken,documentId,blockId,title):
    # blockId 为空的时候 blockId = documentId

    if not blockId or blockId == '':
        blockId = documentId

    url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{documentId}/blocks/{blockId}/children'
    headers = {
        'Authorization': f'Bearer {tenantAccessToken}',
        'Content-Type': 'application/json'
    }
    data = {
        'children': [
            {
                'block_type': 3,
                'heading1': {
                    'elements': [
                        {
                            'text_run': {
                                'content': title
                            }
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")


def addHead2(tenantAccessToken,documentId,blockId,title):
    # blockId 为空的时候 blockId = documentId

    if not blockId or blockId == '':
        blockId = documentId

    url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{documentId}/blocks/{blockId}/children'
    headers = {
        'Authorization': f'Bearer {tenantAccessToken}',
        'Content-Type': 'application/json'
    }
    data = {
        'children': [
            {
                'block_type': 4,
                'heading2': {
                    'elements': [
                        {
                            'text_run': {
                                'content': title
                            }
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

def addText(tenantAccessToken,documentId,blockId,text):
    # blockId 为空的时候 blockId = documentId

    if not blockId or blockId == '':
        blockId = documentId

    url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{documentId}/blocks/{blockId}/children'
    headers = {
        'Authorization': f'Bearer {tenantAccessToken}',
        'Content-Type': 'application/json'
    }
    data = {
        'children': [
            {
                'block_type': 2,
                'text': {
                    'elements': [
                        {
                            'text_run': {
                                'content': text
                            }
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

def addFile(tenantAccessToken,documentId,blockId,file_path):
    # blockId 为空的时候 blockId = documentId

    if not blockId or blockId == '':
        blockId = documentId

    url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{documentId}/blocks/{blockId}/children'
    headers = {
        'Authorization': f'Bearer {tenantAccessToken}',
        'Content-Type': 'application/json'
    }
    data = {
        'children': [
            {
                'block_type': 23,
                'file': {
                    'token': '',
                    'view_type':2
                }
                    
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"addFile Error: {response.status_code}, {response.text}")
    
    blockId = response.json()['data']['children'][0]['children'][0]

    url = f'https://open.feishu.cn/open-apis/drive/v1/medias/upload_all'
    headers = {
        'Authorization': f'Bearer {tenantAccessToken}'
    }

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    form = {
        'file_name': file_name,
        'parent_type': 'docx_file',
        'parent_node': blockId,
        'size': str(file_size),
        'file': (open(file_path, 'rb'))
    }
    
    multi_form = MultipartEncoder(form)
    headers['Content-Type'] = multi_form.content_type
    
    response = requests.post(url, headers=headers, data=multi_form)

    if response.status_code != 200:
        raise Exception(f"uploadFile Error: {response.status_code}, {response.text}")

    file_token = response.json()['data']['file_token']

    url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{documentId}/blocks/{blockId}'
    headers = {
        'Authorization': f'Bearer {tenantAccessToken}',
        'Content-Type': 'application/json'
    }
    data = {
        'replace_file':{
            'token':file_token
        }
    }

    response = requests.patch(url, headers=headers, json=data)

    return

def getAllChatId(tenantAccessToken):
    url = f'https://open.feishu.cn/open-apis/im/v1/chats'
    headers = {
        'Authorization': f'Bearer {tenantAccessToken}'
    }
    response = requests.get(url, headers=headers)
    
    return response.text

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
    
# 封装，为了外部引用，直接给debug群发消息
def sendMessageDebug(message):
    token = getTenantAccessToken()
    sendMessage(token,message,'oc_1e418dff75881d2b0d85a5f701262cb8')

if __name__ == '__main__':
    # print(getTenantAccessToken())
    # print(createDoc(getTenantAccessToken(),'一篇新的文档'))

    token = getTenantAccessToken()
    # sendMessage(token,'今日iOS海外AI速度报告：https://rivergame.feishu.cn/docx/FGWld7bQboqDJux6axPcx5TOnIc')
    # print(getAllChatId(token))
    sendMessage(token,'debug','oc_1e418dff75881d2b0d85a5f701262cb8')

