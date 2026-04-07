from flask import Blueprint, request, jsonify
from database import db
from models import Categoria
from flasgger import swag_from

categorias_bp = Blueprint('categorias', __name__)


@categorias_bp.route('', methods=['GET'])
@swag_from({
    'tags': ['Categorias'],
    'summary': 'Listar todas as categorias',
    'responses': {
        200: {
            'description': 'Lista de categorias',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nome': {'type': 'string'},
                        'cor': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def listar_categorias():
    categorias = Categoria.query.all()
    return jsonify([c.to_dict() for c in categorias])


@categorias_bp.route('/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Categorias'],
    'summary': 'Buscar categoria por ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Categoria encontrada'},
        404: {'description': 'Categoria não encontrada'}
    }
})
def buscar_categoria(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({'erro': 'Categoria não encontrada'}), 404
    return jsonify(categoria.to_dict())


@categorias_bp.route('', methods=['POST'])
@swag_from({
    'tags': ['Categorias'],
    'summary': 'Criar nova categoria',
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
                    'cor': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Categoria criada com sucesso'}
    }
})
def criar_categoria():
    dados = request.get_json()
    categoria = Categoria(
        nome=dados['nome'],
        cor=dados.get('cor', '#000000')
    )
    db.session.add(categoria)
    db.session.commit()
    return jsonify(categoria.to_dict()), 201


@categorias_bp.route('/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Categorias'],
    'summary': 'Atualizar categoria',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'nome': {'type': 'string'},
                    'cor': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Categoria atualizada'},
        404: {'description': 'Categoria não encontrada'}
    }
})
def atualizar_categoria(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({'erro': 'Categoria não encontrada'}), 404
    dados = request.get_json()
    categoria.nome = dados.get('nome', categoria.nome)
    categoria.cor = dados.get('cor', categoria.cor)
    db.session.commit()
    return jsonify(categoria.to_dict())


@categorias_bp.route('/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Categorias'],
    'summary': 'Deletar categoria',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Categoria deletada'},
        404: {'description': 'Categoria não encontrada'}
    }
})
def deletar_categoria(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({'erro': 'Categoria não encontrada'}), 404
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({'mensagem': 'Categoria deletada com sucesso'})
