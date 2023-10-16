from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
from dotenv import load_dotenv
from gestion_autenticacion.vista.vista_autenticacion import VistaGenerarToken, VistaSaludServicio
from gestion_autenticacion.modelo import db, UsuariosSchema
import os

user_schema = UsuariosSchema()

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config["JWT_ALGORITHM"] = "HS256"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config['PROPAGATE_EXEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)

api.add_resource(VistaGenerarToken,'/users/auth')
api.add_resource(VistaSaludServicio,'/users/ping')

jwt = JWTManager(app)