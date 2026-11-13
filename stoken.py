import os

from itsdangerous import URLSafeTimedSerializer

secret_key=os.environ['TOKEN_SECRET_KEY']
salt=os.environ['TOKEN_SALT']
def endata(data):
    serilalizer=URLSafeTimedSerializer(secret_key)
    return serilalizer.dumps(data,salt=salt)
def dndata(data):
    serilalizer=URLSafeTimedSerializer(secret_key)
    return serilalizer.loads(data,salt=salt)