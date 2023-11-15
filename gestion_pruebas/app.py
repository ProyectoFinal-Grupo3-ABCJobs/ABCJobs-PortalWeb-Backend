from flask import Flask,jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
from dotenv import load_dotenv

import os

directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)

if carpeta_actual=='gestion_pruebas' or carpeta_actual=='app':
    from vista.vista_pruebas import VistaSaludServicio,VistaConsultaPruebasCandidato,VistaConsultaEntrevistasCandidato, VistaResultadoPruebasCandidatosPorIdEmpresa, VistaResultadoEntrevistasCandidatosPorIdEmpresa
    from modelo import db
else:    
    from gestion_pruebas.vista.vista_pruebas import VistaSaludServicio,VistaConsultaPruebasCandidato,VistaConsultaEntrevistasCandidato, VistaResultadoEntrevistasCandidatosPorIdEmpresa, VistaResultadoPruebasCandidatosPorIdEmpresa
    from gestion_pruebas.modelo import db

load_dotenv()

app = Flask(__name__)

if (os.getenv('DEV')=='1'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../proyectoABCJobs.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config["JWT_ALGORITHM"] = "HS256"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
app.config['PROPAGATE_EXEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)

# Endpoints de pruebas
api.add_resource(VistaConsultaPruebasCandidato,'/test/candidate/<int:id_candidato>')
api.add_resource(VistaConsultaEntrevistasCandidato,'/test/candidate/<int:id_candidato>/interviews')
api.add_resource(VistaSaludServicio,'/test/ping')


# EndPoints resultados Pruebas
api.add_resource(VistaResultadoPruebasCandidatosPorIdEmpresa,'/test/company/<int:id_empresa>')

# EndPoints resultados Entrevista
api.add_resource(VistaResultadoEntrevistasCandidatosPorIdEmpresa,'/test/company/<int:id_empresa>/interviews')

jwt = JWTManager(app)

