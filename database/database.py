import sqlite3

class Database():
    def __init__(self, file) -> None:
        self.conn = sqlite3.connect(file+'.db')
        self.conn.execute('CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL);')

    def add(self,note) -> None:
        self.conn.execute(f"INSERT INTO note (title, content) VALUES ('{note.title}','{note.content}')")
        self.conn.commit()

    def get_all(self) -> list:
        lista=[]
        for linha in self.conn.execute("SELECT id, title, content FROM note"):
            identificador = linha[0]
            title = linha[1]
            content = linha[2]  
            lista.append(Note(identificador,title,content))
        return lista
    
    def update(self, entry) -> None:
        self.conn.execute("UPDATE note SET title = ?, content = ?  WHERE id = ?", (entry.title, entry.content, entry.id))
        self.conn.commit()

    def delete(self,note_id) -> None:
        self.conn.execute(f"DELETE FROM note WHERE id = {note_id}")
        self.conn.commit()

class Note():
    def __init__(self, id=None, title=None, content='') -> None:
        self.id = id
        self.title = title
        self.content = content