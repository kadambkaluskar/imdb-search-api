from auth.auth import Auth
from time import sleep
authObj = Auth()
token = authObj.encode_auth_token(1234)
print token

sleep(20)
decoded_token = authObj.decode_auth_token(token)
print decoded_token
