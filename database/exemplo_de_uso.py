from database import Database,Note

db = Database('banco')
db.add(Note(title='Pini', content='teste'))
db.add(Note(title=None, content='Lembrar de tomar água'))

notes = db.get_all()
for note in notes:
    print(f'Anotação {note.id}:\n  Título: {note.title}\n  Conteúdo: {note.content}\n')