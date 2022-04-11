import uuid

def uuid():
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    return suid[:16]