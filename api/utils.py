import hashlib, random, string, uuid

def generate_verification_key(email):
    salt = hashlib.sha256(str(random.random())).hexdigest()[:5]
    email = email
    if isinstance(email, unicode):
        email = email.encode('utf-8')
        return hashlib.sha256(salt + email).hexdigest()[:32]

def generate_temporary_token():
    return uuid.uuid4().hex
