from urllib import request
import requests

def download_file(openid, url, mode):
    r = requests.get(url, allow_redirects=True)
    header = r.headers.get('content-type')
    type = header.split('/')[1]
    save_path = "../upload_files" + openid + "_" + mode + "." + type
    request.urlretrieve(url, save_path)
    return save_path
