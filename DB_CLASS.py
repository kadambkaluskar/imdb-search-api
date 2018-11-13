import MySQLdb
import os

class DB_CLASS :
    
    #- this function will connect with mysql
    def connectMysqlDb(self):
        try :
            hostName = os.getenv('IMDB_MYSQL_HOSTNAME')
            userName = os.getenv('IMDB_MYSQL_USERNAME')
            password = os.getenv('IMDB_MYSQL_PASSWORD')
            dbName   = os.getenv('IMDB_MYSQL_DBNAME')
            db_var = MySQLdb.connect(host = hostName, # hostname
                user = userName, # username to be entered
                passwd = password, # password to be entered
                db = dbName # name of the data base
                )

        except Exception as ins:
            return False
        
        return db_var
