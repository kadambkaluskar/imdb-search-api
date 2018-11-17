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
    response_str = '''Please try one of the following URL :
                      to search GET /api/movies?param1=value1&param2=value2
                      to get a movie GET /api/movies/movie_id
                      to add a movie POST /api/movies
                      to edit a movie PUT /api/movies/movie_id
                      to delete a movie DELETE /api/movies/movie_id'''
    return response_str


@app.route('/api/movies',methods=['GET'])
def search_movie():
    #first creating API only to search on the basis of movie name,director and genre
    #add later searching based on imdb_score and 99_popularity, with lower than,greater than or equal to filter
    #this api created only for searching based on filter, and would not return anything if filter is not provided
    #if requried, if no params are sent, we can return first 10 results
    token_response = authObj.check_token(request)
    if  token_response == 'Token Expired' or token_response == 'Invalid token' or token_response == 'Token not found':
        return jsonify({'message' : token_response})

    param = {}
    if request.args.get("movie_name") is not None :
        param['movie_name'] = request.args.get("movie_name")
    if request.args.get("movie_director") is not None :
        param['movie_director'] = request.args.get("movie_director")
    if request.args.get("movie_genre") is not None :
        param['movie_genre'] = request.args.get("movie_genre")
    if not param :
       return jsonify({'message' : 'no filter criteria found'})
    movie_response = movieObj.search_movie(param)
    
    return jsonify(movie_response)

@app.route('/api/movies',methods=['POST'])
def add_movie():
    token_response = authObj.check_token(request)
    if  token_response == 'Token Expired' or token_response == 'Invalid token' or token_response == 'Token not found':
        return jsonify({'message' : token_response}) 
    if not is_admin(token_response) :
        return jsonify({'error' : 'Unauhorized'}),403
    
    request_param = request.get_json()
    validation_response = movieObj.validate_add_movie_param(request_param)
    if validation_response : 
        return jsonify({'message' : validation_response})
    movie_response = movieObj.add_movie(request_param)
    return jsonify(movie_response)


@app.route('/api/movies/<movie_id>',methods=['PUT'])
def edit_movie(movie_id):
    token_response = authObj.check_token(request)
    if  token_response == 'Token Expired' or token_response == 'Invalid token' or token_response == 'Token not found':
        return jsonify({'message' : token_response})
    if not is_admin(token_response) : 
        return jsonify({'error' : 'Unauthorized'}),403
    
    if not movie_id.isdigit() :
        return jsonify({'error' : 'INvalid movie id'})
    request_param = request.get_json()
    validation_response = movieObj.validate_edit_movie_param(request_param)
    if validation_response :
        return jsonify(validation_response)
    request_param['movie_id'] = movie_id
    movie_response = movieObj.edit_movie(request_param)
    
    return jsonify(movie_response)

@app.route('/api/movies/<movie_id>',methods=['DELETE'])
def delete_movie(movie_id) :
    token_response = authObj.check_token(request)
    if  token_response == 'Token Expired' or token_response == 'Invalid token' or token_response == 'Token not found':
        return jsonify({'message' : token_response})
    if not is_admin(token_response) :
        return jsonify({'error' : 'Unauthorized'}),403
    if not movie_id.isdigit():
        return jsonify({'error' : 'Invalid movie id'})

    movie_response = movieObj.delete_movie(movie_id)
    return jsonify(movie_response)

@app.route('/api/movies/<movie_id>',methods=['GET'])
def get_movie(movie_id):
    token_response = authObj.check_token(request)
    if  token_response == 'Token Expired' or token_response == 'Invalid token' or token_response == 'Token not found':
        return jsonify({'message' : token_response})
    if not movie_id.isdigit():
        return jsonify({'error' : 'Invalid movie id'})
    movie_response = movieObj.get_movie(movie_id)
    if not movie_response :
        return jsonify({'message' : 'Movie not found'})

    return jsonify(movie_response)


def is_admin(token_response):
    return True if token_response['is_admin'] == 1 else False

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
    token = authObj.encode_auth_token(login_response['user_id'],login_response['is_admin'])
    return jsonify({ 'token' : token})
if __name__ == '__main__' :
    app.run(host='0.0.0.0')
