import uuid

def suid():
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    return suid

