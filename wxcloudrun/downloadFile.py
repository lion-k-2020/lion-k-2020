from urllib import request
import requests

def download_file(open_id, url):
    url = 'https://7072-prod-4gbd4dc41c3a1678-1310533907.tcb.qcloud.la/92ec59b3ec1bf80ccc2d805ef5f6bcdb.mp4'
    r = requests.get(url, allow_redirects=True)
    header = r.headers.get('content-type')
    type = header.split('/')[1]
    save_path = "../upload_files" + open_id + "." + type
    request.urlretrieve(url, save_path)
    return save_path
