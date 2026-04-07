from flask import Blueprint, request, jsonify
from database import db
from models import Comentario
from flasgger import swag_from

comentarios_bp = Blueprint('comentarios', __name__)


@comentarios_bp.route('', methods=['GET'])
@swag_from({
    'tags': ['Comentarios'],
    'summary': 'Listar todos os comentarios',
    'responses': {
        200: {
            'description': 'Lista de comentarios',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'texto': {'type': 'string'},
                        'criado_em': {'type': 'string'},
                        'tarefa_id': {'type': 'integer'}
                    }
                }
            }
        }
    }
})
def listar_comentarios():
    comentarios = Comentario.query.all()
    return jsonify([c.to_dict() for c in comentarios])


@comentarios_bp.route('/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Comentarios'],
    'summary': 'Buscar comentario por ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Comentario encontrado'},
        404: {'description': 'Comentario não encontrado'}
    }
})
def buscar_comentario(id):
    comentario = Comentario.query.get(id)
    if not comentario:
        return jsonify({'erro': 'Comentario não encontrado'}), 404
    return jsonify(comentario.to_dict())


@comentarios_bp.route('', methods=['POST'])
@swag_from({
    'tags': ['Comentarios'],
    'summary': 'Criar novo comentario',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['texto', 'tarefa_id'],
                'properties': {
                    'texto': {'type': 'string'},
                    'tarefa_id': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Comentario criado com sucesso'}
    }
})
def criar_comentario():
    dados = request.get_json()
    comentario = Comentario(
        texto=dados['texto'],
        tarefa_id=dados['tarefa_id']
    )
    db.session.add(comentario)
    db.session.commit()
    return jsonify(comentario.to_dict()), 201


@comentarios_bp.route('/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Comentarios'],
    'summary': 'Atualizar comentario',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'texto': {'type': 'string'},
                    'tarefa_id': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Comentario atualizado'},
        404: {'description': 'Comentario não encontrado'}
    }
})
def atualizar_comentario(id):
    comentario = Comentario.query.get(id)
    if not comentario:
        return jsonify({'erro': 'Comentario não encontrado'}), 404
    dados = request.get_json()
    comentario.texto = dados.get('texto', comentario.texto)
    comentario.tarefa_id = dados.get('tarefa_id', comentario.tarefa_id)
    db.session.commit()
    return jsonify(comentario.to_dict())


@comentarios_bp.route('/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Comentarios'],
    'summary': 'Deletar comentario',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Comentario deletado'},
        404: {'description': 'Comentario não encontrado'}
    }
})
def deletar_comentario(id):
    comentario = Comentario.query.get(id)
    if not comentario:
        return jsonify({'erro': 'Comentario não encontrado'}), 404
    db.session.delete(comentario)
    db.session.commit()
    return jsonify({'mensagem': 'Comentario deletado com sucesso'})
