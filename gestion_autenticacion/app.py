from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
from dotenv import load_dotenv
import os

directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)

if carpeta_actual=='gestion_autenticacion' or carpeta_actual=='app':
    from vista.vista_autenticacion import VistaGenerarToken, VistaSaludServicio, VistaRegistroUsuario
    from modelo import db, UsuarioSchema
else:    
    from gestion_autenticacion.vista.vista_autenticacion import VistaGenerarToken, VistaSaludServicio, VistaRegistroUsuario
    from gestion_autenticacion.modelo import db, UsuarioSchema

user_schema = UsuarioSchema()

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../proyectoABCJobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config["JWT_ALGORITHM"] = "HS256"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=10)
app.config['PROPAGATE_EXEPTIONS'] = True
app.config['JWT_HEADER_TYPE'] = ''

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


# if __name__ == "__main__":
#     app.run(host = "0.0.0.0", port = 5000, debug = True)