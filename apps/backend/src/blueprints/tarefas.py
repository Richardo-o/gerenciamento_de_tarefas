from flask import Blueprint, request, jsonify
from database import db
from models import Tarefa
from flasgger import swag_from

tarefas_bp = Blueprint('tarefas', __name__)


@tarefas_bp.route('', methods=['GET'])
@swag_from({
    'tags': ['Tarefas'],
    'summary': 'Listar todas as tarefas',
    'responses': {
        200: {
            'description': 'Lista de tarefas',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'titulo': {'type': 'string'},
                        'descricao': {'type': 'string'},
                        'concluida': {'type': 'boolean'},
                        'prioridade': {'type': 'string'},
                        'criado_em': {'type': 'string'},
                        'projeto_id': {'type': 'integer'},
                        'categoria_id': {'type': 'integer'}
                    }
                }
            }
        }
    }
})
def listar_tarefas():
    tarefas = Tarefa.query.all()
    return jsonify([t.to_dict() for t in tarefas])


@tarefas_bp.route('/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Tarefas'],
    'summary': 'Buscar tarefa por ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Tarefa encontrada'},
        404: {'description': 'Tarefa não encontrada'}
    }
})
def buscar_tarefa(id):
    tarefa = Tarefa.query.get(id)
    if not tarefa:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404
    return jsonify(tarefa.to_dict())


@tarefas_bp.route('', methods=['POST'])
@swag_from({
    'tags': ['Tarefas'],
    'summary': 'Criar nova tarefa',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['titulo'],
                'properties': {
                    'titulo': {'type': 'string'},
                    'descricao': {'type': 'string'},
                    'concluida': {'type': 'boolean'},
                    'prioridade': {'type': 'string'},
                    'projeto_id': {'type': 'integer'},
                    'categoria_id': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Tarefa criada com sucesso'}
    }
})
def criar_tarefa():
    dados = request.get_json()
    tarefa = Tarefa(
        titulo=dados['titulo'],
        descricao=dados.get('descricao'),
        concluida=dados.get('concluida', False),
        prioridade=dados.get('prioridade', 'media'),
        projeto_id=dados.get('projeto_id'),
        categoria_id=dados.get('categoria_id')
    )
    db.session.add(tarefa)
    db.session.commit()
    return jsonify(tarefa.to_dict()), 201


@tarefas_bp.route('/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Tarefas'],
    'summary': 'Atualizar tarefa',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'titulo': {'type': 'string'},
                    'descricao': {'type': 'string'},
                    'concluida': {'type': 'boolean'},
                    'prioridade': {'type': 'string'},
                    'projeto_id': {'type': 'integer'},
                    'categoria_id': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Tarefa atualizada'},
        404: {'description': 'Tarefa não encontrada'}
    }
})
def atualizar_tarefa(id):
    tarefa = Tarefa.query.get(id)
    if not tarefa:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404
    dados = request.get_json()
    tarefa.titulo = dados.get('titulo', tarefa.titulo)
    tarefa.descricao = dados.get('descricao', tarefa.descricao)
    tarefa.concluida = dados.get('concluida', tarefa.concluida)
    tarefa.prioridade = dados.get('prioridade', tarefa.prioridade)
    tarefa.projeto_id = dados.get('projeto_id', tarefa.projeto_id)
    tarefa.categoria_id = dados.get('categoria_id', tarefa.categoria_id)
    db.session.commit()
    return jsonify(tarefa.to_dict())


@tarefas_bp.route('/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Tarefas'],
    'summary': 'Deletar tarefa',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Tarefa deletada'},
        404: {'description': 'Tarefa não encontrada'}
    }
})
def deletar_tarefa(id):
    tarefa = Tarefa.query.get(id)
    if not tarefa:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404
    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({'mensagem': 'Tarefa deletada com sucesso'})
