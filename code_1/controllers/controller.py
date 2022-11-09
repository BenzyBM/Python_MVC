import cherrypy
import os.path
import sqlite3

db_loc = "./bts.db"

class FighterChooser(object):
    @cherrypy.expose
    def index(self):
        return open('./views/view.html')
    
    @cherrypy.expose
    def V(self):
        return open('./views/V.html')
    
    @cherrypy.expose
    def Fighter(self):
        with sqlite3.connect(db_loc) as c:
            query = "SELECT * FROM bts_members ORDER BY RANDOM() LIMIT 1"
            cursor = c.cursor()
            cursor.execute(query)
            str_data = f'{cursor.fetchone}'
            cursor.close()
            return open(str_data)

def setup_bd():
    with sqlite3.connect(db_loc) as con:
        con.execute("CREATE TABLE bts_members (site);")
        con.execute("""INSERT INTO bts_members VALUES
        ("./views/V.html"),("./views/RM.html"),("./views/Jin.html"),("./views/JungKook.html"),("./views/SUGA.html");"""
        )

def delete_db():
    with sqlite3.connect(db_loc) as con:
        con.execute("DROP TABLE bts_members")


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.engine.subscribe('start', setup_bd)
    cherrypy.engine.subscribe('stop', delete_db)
    cherrypy.quickstart(FighterChooser(), '/', conf)