import os
from flask import Flask, render_template
# from .server import create_app  # au lieu de app
from . import server


def page_not_found(e):
    return render_template('404.html'), 404


def create_app(clubs, competitions, test_config=None):
    """Facilite les tests. App factory qui englobe toute l'app :
     https://flask.palletsprojects.com/en/2.1.x/patterns/appfactories/"""
    app = Flask(__name__)  # l'ajout de , instance_relative_config=True fait qu'il ne trouve plus config(?)
    app.config.from_pyfile('../config.py')

    # problème dû à la factory pour tester les routes, apparemment il faudrait user des blueprints :
    # si depuis __init__ : from app.main import bp as main_bp ou from . import main +

    from .server import bp
    app.register_blueprint(bp)

    app.register_error_handler(404, page_not_found)

    # impl when app factory is used : https://flask.palletsprojects.com/en/1.0.x/patterns/errorpages/
    # app.secret_key = 'something_special'

    # je peux changer pour suivre : https://www.youtube.com/watch?v=6c_utRUzHG4
    # mais il faudrait mieux comprendre les concepts

    # app.config.from_mapping(
    #     SECRET_KEY='development',
    #     clubs=clubs,
    #     competitions=competitions
    # )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('../config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.config.update(
        {
            'clubs': clubs,
            'competitions': competitions
        }
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
