from DB_CLASS import DB_CLASS
import traceback

class Movies(DB_CLASS):

    global dbObj
    dbObj = DB_CLASS()

    def validate_add_movie_param(self,param) :
        missing_param = ''
        if 'movie_name' not in param : 
            missing_param += 'movie_name,'
        if 'movie_director' not in param :
            missing_param += 'movie_director,'
        if 'movie_99_popularity' not in param :
            missing_param += 'movie_99_popularity,'
        if ('movie_genre' not in param) and (type(param['movie_genre']) != list):
            missing_param += 'movie_genre',
        if 'movie_imdb_score' not in param :
            missing_param += 'movie_imdb_score,'
        if missing_param != '' :
            missing_param = missing_param.strip(',')
            missing_param = 'Following params are missing or invalid : ' + str(missing_param)
        return missing_param

    def add_movie(self,params) :
        pass

    def delete_movie(self,movie_id) :
        try :
            db = dbObj.connect_db()
            cur = db.cursor()
            cur.execute('DELETE FROM movies WHERE movie_id = %s',movie_id)
            db.commit()
            if cur.rowcount :
                return {'message' : 'movie deleted successfully'}
            else :
                return {'message' : 'no movie found to delete'}
        except Exception as ins :
            print ins
            print traceback.print_exc()
            return {'message' : 'Movie could not be deleted. Please try again later.'}
        
    def edit_movie(self,movie_id) :
        #write code to edit movie
        pass

    def get_movie(self,movie_id):
        #write code to get movie data
        try :
            response = {}
            db = dbObj.connect_db()
            cur = db.cursor()
            cur.execute('SELECT * FROM movies WHERE movie_id = %s',movie_id)
            for row in cur :
                response['movie_name'] = row[1]
                response['movie_director'] = row[2]
                response['movie_99_popularity'] = str(row[3])
                response['movie_genre'] = row[4].split(',')
                response['movie_imdb_score'] = str(row[5])
            db.close()
            return response
        except Exception as ins :
            print ins
            print traceback.exc()
            return {'message' : 'Movie could not be fetched. Please try again later'}

    def search_movie(self,req):
        #write code to search for a movie
        pass
