import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from database import db
from models import Projeto, Categoria, Tarefa, Comentario


def seed():
    app = create_app()

    with app.app_context():
        db.create_all()

        if Projeto.query.first():
            print('Banco ja populado.')
            return

        projetos = [
            Projeto(nome='Projeto Alpha', descricao='Projeto de teste Alpha'),
            Projeto(nome='Projeto Beta', descricao='Projeto de teste Beta'),
        ]
        db.session.add_all(projetos)
        db.session.commit()

        categorias = [
            Categoria(nome='Trabalho', cor='#FF0000'),
            Categoria(nome='Pessoal', cor='#00FF00'),
            Categoria(nome='Estudos', cor='#0000FF'),
        ]
        db.session.add_all(categorias)
        db.session.commit()

        tarefas = [
            Tarefa(
                titulo='Implementar login',
                descricao='Criar tela de login com validacao',
                concluida=False,
                prioridade='alta',
                projeto_id=projetos[0].id,
                categoria_id=categorias[0].id
            ),
            Tarefa(
                titulo='Configurar banco',
                descricao='Configurar PostgreSQL com Docker',
                concluida=True,
                prioridade='media',
                projeto_id=projetos[0].id,
                categoria_id=categorias[0].id
            ),
            Tarefa(
                titulo='Ler livro Python',
                descricao='Ler capitulo 5 do livro',
                concluida=False,
                prioridade='baixa',
                projeto_id=None,
                categoria_id=categorias[2].id
            ),
        ]
        db.session.add_all(tarefas)
        db.session.commit()

        comentarios = [
            Comentario(texto='Comecar pela autenticacao OAuth', tarefa_id=tarefas[0].id),
            Comentario(texto='Usar Docker Compose para facilitar', tarefa_id=tarefas[1].id),
        ]
        db.session.add_all(comentarios)
        db.session.commit()

        print('Dados iniciais inseridos com sucesso.')


if __name__ == '__main__':
    seed()
