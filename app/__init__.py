from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dateutil import parser


db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config['SECRET_KEY'] = 'wrfewgrw12431th'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/db.db'

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth import auth
    app.register_blueprint(auth)

    from app.blog import blog
    app.register_blueprint(blog)

    @app.template_filter('strftime')
    def _jinja2_filter_datetime(date, fmt=None):
        date = parser.parse(str(date))
        native = date.replace(tzinfo=None)
        format = '%b %d, %Y'
        return native.strftime(format)


    return app

