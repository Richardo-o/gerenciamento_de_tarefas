from flask import Blueprint, request, jsonify
from database import db
from models import Projeto
from flasgger import swag_from

projetos_bp = Blueprint('projetos', __name__)


@projetos_bp.route('', methods=['GET'])
@swag_from({
    'tags': ['Projetos'],
    'summary': 'Listar todos os projetos',
    'responses': {
        200: {
            'description': 'Lista de projetos',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nome': {'type': 'string'},
                        'descricao': {'type': 'string'},
                        'criado_em': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def listar_projetos():
    projetos = Projeto.query.all()
    return jsonify([p.to_dict() for p in projetos])


@projetos_bp.route('/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Projetos'],
    'summary': 'Buscar projeto por ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Projeto encontrado'},
        404: {'description': 'Projeto não encontrado'}
    }
})
def buscar_projeto(id):
    projeto = Projeto.query.get(id)
    if not projeto:
        return jsonify({'erro': 'Projeto não encontrado'}), 404
    return jsonify(projeto.to_dict())


@projetos_bp.route('', methods=['POST'])
@swag_from({
    'tags': ['Projetos'],
    'summary': 'Criar novo projeto',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['nome'],
                'properties': {
                    'nome': {'type': 'string'},
                    'descricao': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Projeto criado com sucesso'}
    }
})
def criar_projeto():
    dados = request.get_json()
    projeto = Projeto(
        nome=dados['nome'],
        descricao=dados.get('descricao')
    )
    db.session.add(projeto)
    db.session.commit()
    return jsonify(projeto.to_dict()), 201


@projetos_bp.route('/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Projetos'],
    'summary': 'Atualizar projeto',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'nome': {'type': 'string'},
                    'descricao': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Projeto atualizado'},
        404: {'description': 'Projeto não encontrado'}
    }
})
def atualizar_projeto(id):
    projeto = Projeto.query.get(id)
    if not projeto:
        return jsonify({'erro': 'Projeto não encontrado'}), 404
    dados = request.get_json()
    projeto.nome = dados.get('nome', projeto.nome)
    projeto.descricao = dados.get('descricao', projeto.descricao)
    db.session.commit()
    return jsonify(projeto.to_dict())


@projetos_bp.route('/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Projetos'],
    'summary': 'Deletar projeto',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Projeto deletado'},
        404: {'description': 'Projeto não encontrado'}
    }
})
def deletar_projeto(id):
    projeto = Projeto.query.get(id)
    if not projeto:
        return jsonify({'erro': 'Projeto não encontrado'}), 404
    db.session.delete(projeto)
    db.session.commit()
    return jsonify({'mensagem': 'Projeto deletado com sucesso'})
