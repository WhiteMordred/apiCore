from flask import Blueprint
from api.default import default_api
from api.authentication import authentication_api
from api.register import register_api
from api.validation import validate_api
from api.detect import detect_api
from api.ocr import ocr_api

def loader(app):
    app.register_blueprint(default_api, url_prefix="/api")
    app.register_blueprint(authentication_api, url_prefix="/api")
    app.register_blueprint(register_api, url_prefix="/api")
    app.register_blueprint(validate_api, url_prefix="/api")
    app.register_blueprint(detect_api, url_prefix="/api")
    app.register_blueprint(ocr_api, url_prefix="/api")
