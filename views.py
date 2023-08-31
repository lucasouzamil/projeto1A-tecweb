from utils import load_db, load_template
import urllib
from utils import add_in_db, build_response
from database import database

def index(request):

    db = database.Database('LISTA')
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):

        print("\n\n\n OLHA O REQUEST \n\n\n")
        print(request)
        print("\n\n\n\n\n")
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')

        corpo = partes[1]
        print("\n\n\n\n\n")
        print(corpo)
        print("\n\n\n\n\n")
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus

        name = corpo.split('=')[0]
        if name == 'titulo':
            params = {}
            for chave_valor in corpo.split('&'):
                o = chave_valor.split('=')
                params[o[0]]=urllib.parse.unquote_plus(o[1])
            add_in_db(params)
        elif name == 'id':
            id = int(corpo.split('=')[1])
            db.delete(id)

        return build_response(code=303, reason='See Other', headers='Location: /')

    # O RESTO DO CÓDIGO DA FUNÇÃO index CONTINUA DAQUI PARA BAIXO...
    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(identificador=note.id,title=note.title, details=note.content)
        for note in load_db()
    ]
    notes = '\n'.join(notes_li)

    t =  load_template('index.html').format(notes=notes)
    return build_response(body=t)

def edit(request):

    request = request.replace('\r', '') 
    partes = request.split('\n\n')
    corpo = partes[1]
    name = corpo.split('=')[0]

    db = database.Database('LISTA')
    if request.startswith('POST'):
        print('POSTOOOOU')
        print(name)
        if name == 'id':
            print('ENTROOOU')
            id = int(corpo.split('=')[1].split('%')[0])
            titulo = corpo.split('titulo=')[1].split('&')[0]
            descricao = corpo.split('titulo=')[1].split('detalhes=')[1]
            note = database.Note(id=id,title=titulo,content=descricao)
            db.update(note)

        return build_response(code=303, reason='See Other', headers='Location: /')

    
    id = partes[0].split('=')[1]
    id = int(id.split(' ')[0])
    note = db.returncard(id)
    edit_card_template = load_template('components/edit-card.html').format(identificador=note.id,title=note.title,details=note.content)

    t =  load_template('edit.html').format(editcard=edit_card_template)
    return build_response(body=t)