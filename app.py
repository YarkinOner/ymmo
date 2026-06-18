from flask import Flask
from flask_bcrypt import Bcrypt
from models import db, login_manager

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ymmo-secret-change-in-prod'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ymmo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    login_manager.login_view = 'auth.login'

    from routes.auth import auth_bp
    from routes.listings import listings_bp
    from routes.dashboard import dashboard_bp
    from routes.analytics import analytics_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(listings_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(analytics_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)