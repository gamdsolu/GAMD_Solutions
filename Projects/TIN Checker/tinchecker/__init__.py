from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://gamdsolu_tinchecker_admin:tinchecker_admin_password@localhost:5432/gamdsolu_tinchecker_db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
from tinchecker import routes