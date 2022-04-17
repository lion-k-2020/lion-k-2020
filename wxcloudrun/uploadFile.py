import json
import requests
import os
import ssl
import urllib3

urllib3.disable_warnings()

s = requests.session()
s.keep_alive = False

ssl._create_default_https_context = ssl._create_unverified_context

def upload_file(file_path, file_name):
    # 获取文件类型
    file = os.path.splitext(file_path)
    # 获取token
    response = requests.get(
        'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx07d53ce7b97ea80a&secret=695e62720ab4c629d0690c135f1b6b15', verify=False)
    # 得到上传链接
    data = {
        "env": "prod-4gbd4dc41c3a1678",
        "path": file_name
    }
    data = json.dumps(data)
    response = requests.post("https://api.weixin.qq.com/tcb/uploadfile?access_token=" + response.json()['access_token'],
                             data)
    # 上传文件到服务端
    data2 = {
        "Content-Type": (None, file[1]),  # 此处为上传文件类型
        "key": (None, file_name),  # 需填入path
        "Signature": (None, response.json()['authorization']),
        'x-cos-security-token': (None, response.json()['token']),
        'x-cos-meta-fileid': (None, response.json()['cos_file_id']),
        'file': ('filename.jpg', open(file_path, "rb"))  # 需填入本地文件路径
    }
    response2 = requests.post(response.json()['url'], files=data2)  # 此处files提交的为表单数据，不为json数据，json数据或其他数据会报错
    return response.json()["file_id"]

