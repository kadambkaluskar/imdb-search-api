import jwt
import os
import datetime
from DB_CLASS import DB_CLASS
from hashlib import sha256
class Auth() :


    def check_token (self,req) :
        try :
            #print req
            if 'authorization' not in req.headers :
                return 'Token not found'
            header = req.headers['authorization']
            bearer = header.split(' ')
            token = bearer[1]
            response = self.decode_auth_token(token)
            return response
        except Exception as ins :
            print ins
            return 'Invalid token'

    def encode_auth_token(self,user_id,is_admin=0) :
        try :
            SECRET_KEY = os.getenv('IMDB_SECRET_KEY')
            payload = {
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat' : datetime.datetime.utcnow(),
                'userid' : user_id,
                'is_admin' : is_admin
            }
            token = jwt.encode(payload,SECRET_KEY,algorithm='HS256')
            return token
        except Exception as ins :
            return ins


    def decode_auth_token(self,auth_token) :
        try :
            SECRET_KEY = os.getenv('IMDB_SECRET_KEY')
            payload = jwt.decode(auth_token,SECRET_KEY)
            return payload
        except jwt.ExpiredSignatureError :
            return 'Token Expired.'
        except jwt.InvalidTokenError :
            return 'Invalid token'

    def login(self,username,password) : 
        try :
            response = {}
            password = sha256(password.strip()).hexdigest()
            dbObj = DB_CLASS()
            db = dbObj.connect_db()
            cur = db.cursor()
            cur.execute("SELECT `user_id`,`is_admin` from `users` WHERE `username` = %s and `password` = %s",[username,password])
            for row in cur :
                response['user_id'] = row[0]
                response['is_admin'] = row[0]
            return response
        except Exception as ins :
            print ins
            return {}

