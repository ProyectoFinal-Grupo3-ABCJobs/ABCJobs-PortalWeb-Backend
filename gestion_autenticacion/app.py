from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
from dotenv import load_dotenv
import os

directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)

<<<<<<< HEAD
if carpeta_actual=='gestion_autenticacion' or carpeta_actual=='app':
    from vista.vista_autenticacion import VistaGenerarToken, VistaSaludServicio
=======
if carpeta_actual=='gestion_autenticacion':
    from vista.vista_autenticacion import VistaGenerarToken, VistaSaludServicio, VistaRegistroUsuario
>>>>>>> 9a5ee8370da301c8601683aa7062749547b2b1ad
    from modelo import db, UsuariosSchema
else:    
    from gestion_autenticacion.vista.vista_autenticacion import VistaGenerarToken, VistaSaludServicio, VistaRegistroUsuario
    from gestion_autenticacion.modelo import db, UsuariosSchema

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
api.add_resource(VistaRegistroUsuario,'/users/register')

jwt = JWTManager(app)
