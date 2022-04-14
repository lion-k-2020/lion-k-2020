import uuid
import json

def suid():
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    return suid

def MyEncoder(obj):
    if isinstance(obj, bytes):
        return str(obj, encoding='utf-8')
    return json.JSONEncoder.default(obj)
