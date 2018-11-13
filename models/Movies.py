from DB_CLASS import DB_CLASS

class Movies(DB_CLASS):

    def delete_movie(self,movie_id) :
        #write code to delete movie
        print "Hello"

    def edit_movie(self,movie_id) :
        #write code to edit movie
        pass

    def get_movie(self,movie_id):
        #write code to get movie data
        db = super(Movies,self).connect_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM movies WHERE movie_id = %s',movie_id)
        for row in cur :
            print row
        pass

    def search_movie(self,req):
        #write code to search for a movie
        pass
