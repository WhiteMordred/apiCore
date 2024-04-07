import os
import sys
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from flask import Flask
from flask_cors import CORS
from tools import env_loader,api_router, mail_loader, firstboot


def create_app():
    app = Flask(__name__)
    CORS(app)
    env_loader.load_env(app)
    api_router.loader(app)
    mail = mail_loader.mailconfig(app)
    app.extensions['mail'] = mail

    @app.before_first_request
    def initialize():
        firstboot.init()

    if (os.environ.get('FLASKDEBUG') == 'True'):
        app.debug = True
    else:
        app.debug = False
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host=os.environ.get('FLASKHOST'), port=os.environ.get('FLASKPORT')) 