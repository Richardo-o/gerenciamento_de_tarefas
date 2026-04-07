from flask import Flask
from flasgger import Swagger

from database import db
from config import Config
from blueprints import tarefas_bp, categorias_bp, projetos_bp, comentarios_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    Swagger(app, config={
        'headers': [],
        'static_url_path': '/flasgger_static',
        'specs_route': '/swagger/',
        'specs': [
            {
                'endpoint': 'Swagger',
                'route': '/swagger.json',
                'rule_filter': lambda rule: True,
                'model_filter': lambda tag: True,
            }
        ],
        'swagger_ui': True,
    })

    app.register_blueprint(tarefas_bp, url_prefix='/tarefas')
    app.register_blueprint(categorias_bp, url_prefix='/categorias')
    app.register_blueprint(projetos_bp, url_prefix='/projetos')
    app.register_blueprint(comentarios_bp, url_prefix='/comentarios')

    return app
