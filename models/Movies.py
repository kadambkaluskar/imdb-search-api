from DB_CLASS import DB_CLASS
import traceback

class Movies(DB_CLASS):

    global dbObj
    dbObj = DB_CLASS()


    def validate_edit_movie_param(self,param) :
        #to validate the param and to check that atleast one param is present
        if ('movie_name' not in param and 
            'movie_director' not in param and 
            'movie_genre' not in param and
            'movie_99_popularity' not in param and 
            'movie_imdb_score' not in param) :
            return {'message' : 'please pass atleast one field to update'}
        return False

    def validate_add_movie_param(self,param) :
        missing_param = ''
        if 'movie_name' not in param : #also add regex to allow only characters,number and ',' and space
            missing_param += 'movie_name,'
        if 'movie_director' not in param : #add regex to only allow characers and space
            missing_param += 'movie_director,'
        if 'movie_99_popularity' not in param : # add regex to only allow decimal and between 0 and 100 
            missing_param += 'movie_99_popularity,'
        if ('movie_genre' not in param) and (type(param['movie_genre']) != list): 
            missing_param += 'movie_genre',
        if 'movie_imdb_score' not in param : #add regex to allow only decimal, in the range 0,10
            missing_param += 'movie_imdb_score,'
        if missing_param != '' :
            missing_param = missing_param.strip(',')
            missing_param = 'Following params are missing or invalid : ' + str(missing_param)
        return missing_param


    def edit_movie(self,param) :

        try :
            updateValueList = []
            insertStr = ''
            if 'movie_name' in param :
                insertStr += 'movie_name = %s ,' 
                updateValueList.append(param['movie_name'])
            
            if 'movie_director' in param :
                insertStr += 'movie_director = %s,'
                updateValueList.append(param['movie_director'])

            if 'movie_99_popularity' in param :
                insertStr += 'movie_99_popularity = %s,'
                updateValueList.append(param['movie_99_popularity'])

            if 'movie_imdb_score' in param :
                insertStr += 'movie_imdb_score = %s,'
                updateValueList.append(param['movie_imdb_score'])
           
            if 'movie_genre' in param :
                movie_genre = param['movie_genre']
                movie_genre = ','.join(movie_genre)
                updateValueList.append(movie_genre)
                insertStr += 'movie_genre = %s,'

            insertStr = insertStr.strip(',')
            updateValueList.append(param['movie_id'])
            db = dbObj.connect_db()
            cur = db.cursor()
            cur.execute('UPDATE `movies` SET '+ insertStr + 'WHERE movie_id = %s',updateValueList)
            db.commit()
            if cur.rowcount :
                return {'message' : 'movie updated successfully'}
            else :
                return {'message' : 'movie not found or coulnot be updated'}

        except Exception as ins :
            print ins
            print traceback.print_exc()
            return {'message' : 'movie couldnt not edited.please try again later.'}


      

    def add_movie(self,movie_param) :
        try :
            movie_director = movie_param['movie_director']
            movie_name = movie_param['movie_name']
            movie_99_popularity = movie_param['movie_99_popularity']
            movie_imdb_score = movie_param['movie_imdb_score']
            movie_genre = movie_param['movie_genre']
            movie_genre = ','.join(movie_genre)
        
            db = dbObj.connect_db()
            cur = db.cursor()
            cur.execute('INSERT INTO `imdb_movie`.`movies` (`movie_id`, `movie_name`, `movie_director`, `movie_99_popularity`, `movie_genre`, `movie_imdb_score`) VALUES (NULL, %s, %s, %s, %s, %s)',[movie_name,movie_director,movie_99_popularity,movie_genre,movie_imdb_score])
            db.commit()
            if cur.rowcount :
                movie_id = cur.lastrowid
                return {'message' : 'movie added successfully' , 'movie_id' : movie_id}
            else :
                return {'message' : 'movie couldnot be added'}

        except Exception as ins :
            print ins
            print traceback.print_exc()
            return {'message' : 'Movie could not be added. Please try again later'}

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
        


    def get_movie(self,movie_id):
        #to get movie data
        try :
            response = {}
            db = dbObj.connect_db()
            cur = db.cursor()
            cur.execute('SELECT * FROM movies WHERE movie_id = %s',movie_id)
            for row in cur :
                response['movie_id'] = row[0]
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

    def search_movie(self,search_param):
        try :
            response = []
            search_query = ''
            search_values = []
            for key in search_param :
                search_query += ' '+key +' LIKE %s OR'
                search_values.append('%' + str(search_param[key]) + '%')
            search_query = search_query.strip("OR")
            db = dbObj.connect_db()
            cur = db.cursor()
            cur.execute('SELECT `movie_id`,`movie_name`,`movie_director`,`movie_genre`,`movie_99_popularity`,`movie_imdb_score`  from movies WHERE ' + search_query , search_values)
            print cur._last_executed
            for row in cur :
                movie = {}
                movie['movie_id'] = row[0]
                movie['movie_name'] = row[1]
                movie['movie_director'] = row[2]
                movie['movie_genre'] = row[3].split(',')
                movie['movie_99_popularity'] = str(row[4])
                movie['movie_imdb_score'] = str(row[5])
                response.append(movie)
            return response
        except Exception as ins :
            print ins
            print traceback.print_exc()
            return response

#endOfFile
