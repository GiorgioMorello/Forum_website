from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)
app.config['SECRET_KEY'] = 'c9d66692a61699da0e978ed9cc7bb03c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faça login ou crie uma conta para visualizar esta página'
login_manager.login_message_category = 'alert-info'




from projeto_site import routes
