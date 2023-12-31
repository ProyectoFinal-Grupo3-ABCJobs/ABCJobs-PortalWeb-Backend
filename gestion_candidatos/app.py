from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
from dotenv import load_dotenv
import os

directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)

if carpeta_actual=='gestion_candidatos' or carpeta_actual=='app':
    from vista.vista_candidato import VistaRegistroInfoCandidato, VistaSaludServicio, VistaObtenerTodosCandidatos, VistaObtenerCandidatoPorId, VistaModificarEstadoCandidato
    from modelo import db, CandidatoSchema
else:
    from gestion_candidatos.vista.vista_candidato import VistaRegistroInfoCandidato, VistaSaludServicio, VistaObtenerTodosCandidatos, VistaObtenerCandidatoPorId, VistaModificarEstadoCandidato
    from gestion_candidatos.modelo import db, CandidatoSchema

import os

candidate_schema = CandidatoSchema()

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

api.add_resource(VistaRegistroInfoCandidato,'/candidate/registerInfo')
api.add_resource(VistaObtenerTodosCandidatos,'/candidate/getAll')
api.add_resource(VistaObtenerCandidatoPorId,'/candidate/<int:id_candidato>')
api.add_resource(VistaModificarEstadoCandidato,'/candidate/isHired/<int:id_candidato>')
api.add_resource(VistaSaludServicio,'/candidate/ping')

jwt = JWTManager(app)
