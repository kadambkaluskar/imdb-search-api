from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)
from models.auth import Auth
from models.Movies import Movies

global authObj,movieObj
authObj = Auth()
movieObj = Movies()


@app.route('/')
def index():
    return "Hello World"


@app.route('/api/search/movies')
def search_movie():
    return "API for searching movie"

@app.route('/api/movies',methods=['POST'])
def add_movie():
    return "API to add movies |  only access to admin"

@app.route('/api/movies/<movie_id>',methods=['PUT'])
def edit_movie(movie_id):
    return "API to edit movies | only admin access"

@app.route('/api/movies/<movie_id>',methods=['DELETE'])
def delete_movie(movie_id) :
    token_response = authObj.check_token(request)
    if  token_response == 'Token Expired' or token_response == 'Invalid token' :
        return jsonify({'message' : token_response})
    if not is_admin(token_response) :
        return jsonify({'error' : 'Unauthorized'}),403
    #write code to delete movide
    movie_id = request.data['id']
    return "API to delete movie | only admin access"

@app.route('/api/movies/<movie_id>',methods=['GET'])
def get_movie(movie_id):
    token_response = authObj.check_token(request)
    if  token_response == 'Token Expired' or token_response == 'Invalid token' :
        return jsonify({'message' : token_response})
    movie_response = movieObj.get_movie(movie_id)
    if not movie_response :
        return jsonify({'message' : 'Movie not found'})
    return jsonify(movie_response)


def is_admin(token_response):
    return True if token_response['is_admin'] == 1 else False


def login(username,password) : 
    return True

@app.route('/api/token',methods=['POST'])
def get_auth_token():
    #content type should be application/json
    data = request.get_json()
    username = data['username']
    password = data['password']
    authObj = Auth()
    login_response = authObj.login(username,password)
    if not login_response :
        return jsonify({'message' : 'Invalid username or password'})
    print data
    token = authObj.encode_auth_token(login_response['user_id'],login_response['is_admin'])
    print token
    #write code to verify username and password and return auth token
    return jsonify({ 'token' : token})
if __name__ == '__main__' :
    app.run(host='0.0.0.0')
