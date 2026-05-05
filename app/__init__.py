from flask import Flask
from config.config import Config
from app.extensions import db, bcrypt, jwt
from app.routes.opportunity_routes import opp_bp
from app.routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(opp_bp, url_prefix='/api/opportunities')

    return app