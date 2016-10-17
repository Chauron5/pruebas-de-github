import sqlite3 as db
import tmdbsimple as tmdb 
tmdb.API_KEY='0bc356480695a04727bb6ce5b689de28'

# Throws sqlite3.Error
class Model():
    def __init__(self):
        self._connection = db.connect('peliculas.db')
        self._cursor = self._connection.cursor()
        self._cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Peliculas
            (ID INT PRIMARY KEY      NOT NULL,
            Titulo         VARCHAR   NOT NULL,
            Director       VARCHAR   NOT NULL,
            Duracion       INT(3)    NOT NULL,   
            Estado         VARCHAR   NOT NULL)
            ''')
        self._connection.commit()


    def insertCompleteFilm(self, ID, Titulo, Director, Duracion, Estado):
        self._cursor.execute('''INSERT INTO Peliculas (ID, Titulo, Director, Duracion, Estado)
            VALUES (?,?,?,?,?) ''', (ID, Titulo, Director, Duracion, Estado))
        self._connection.commit()

    def insert(self, Titulo, Director, Duracion, Estado):
        ID=self.getNewID()
        self.insertCompleteFilm(ID, Titulo, Director, Duracion, Estado)

    def getNewID(self):
        lista = []
        for row in self._cursor.execute("SELECT MAX(ID) FROM Peliculas"): 
            lista.append(row[0])
        return lista[0] + 1

    def changeState(self, ID, Estado):
        self._cursor.execute('UPDATE Peliculas SET Estado=? WHERE ID=?', (Estado, ID))
        self._connection.commit()


    def modify(self, ID, Titulo, Director, Duracion, Estado):
        self._cursor.execute('''UPDATE Peliculas 
            SET Titulo=?, 
                Director=?,
                Duracion=?,
                Estado=? 
            WHERE ID=?''', (Titulo, Director, Duracion, Estado, ID))
        self._connection.commit()


    # La Clave primaria ID se pasa con comillas simples ej: modelo.delete('3')
    def delete(self, ID):
        self._cursor.execute('DELETE FROM Peliculas WHERE ID=?', (ID, ))
        self._connection.commit()


    def getAllFilms(self, lista):
        lista.clear()
        for row in self._cursor.execute('SELECT * FROM Peliculas'):
            lista.append([row[0], row[1], row[2], row[3], row[4]])

    def getFilms(self, lista, Estado):
        lista.clear()
        for row in self._cursor.execute('SELECT * FROM Peliculas WHERE Estado=?', (Estado)):
            lista.append([row[0], row[1], row[2], row[3], row[4]])


    def close(self):
        self._connection.close()


model = Model()
#model.insert(6, 'pendiente', 'bye', 123, 'Pendiente')
#model.insert(7, 'recomendada', 'bye', 123, 'Recomendada')
#model.insert(8, 'favorita', 'bye', 123, 'Favorita')