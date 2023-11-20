from flask import Flask,jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
from dotenv import load_dotenv

import os

directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)

if carpeta_actual=='gestion_empresas' or carpeta_actual=='app':
    from vista.vista_empresas import VistaSaludServicio,VistaRegistroEmpresa,VistaConsultaProyectoPorEmpresa, VistaCreacionProyecto, VistaEmpladoInterno, VistaConsultaPerfil, VistaCreacionPerfil, VistaFicha, VistaAsignacionEmpleado, VistaMotorEmparejamiento, VistaObtenerEmpresaPorIdUsuario,VistaResultadoEmparejamientoPorIdProyecto, VistaMotorEmparejamientoTempFicha, VistaEliminarCandidatoMotorPorIdProyecto, VistaContratoCandidato, VistaCreacionDesempenoEmpleado
    from modelo import db
else:    
    from gestion_empresas.vista.vista_empresas import VistaSaludServicio,VistaRegistroEmpresa,VistaConsultaProyectoPorEmpresa, VistaCreacionProyecto, VistaEmpladoInterno, VistaConsultaPerfil, VistaCreacionPerfil, VistaFicha, VistaAsignacionEmpleado, VistaMotorEmparejamiento, VistaObtenerEmpresaPorIdUsuario,VistaResultadoEmparejamientoPorIdProyecto, VistaMotorEmparejamientoTempFicha, VistaEliminarCandidatoMotorPorIdProyecto, VistaContratoCandidato, VistaCreacionDesempenoEmpleado
    from gestion_empresas.modelo import db

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

# Endpoints de Empresa
api.add_resource(VistaRegistroEmpresa,'/company/register')
api.add_resource(VistaObtenerEmpresaPorIdUsuario,'/company/user')
api.add_resource(VistaSaludServicio,'/company/ping')

# Endpoints de Proyecto
api.add_resource(VistaCreacionProyecto,'/company/<int:id_empresa>/projectCreate')
api.add_resource(VistaConsultaProyectoPorEmpresa,'/company/<int:id_empresa>/projects')

# Endpoints de Ficha
api.add_resource(VistaAsignacionEmpleado,'/company/<int:id_empresa>/assignEmployee')
api.add_resource(VistaEmpladoInterno,'/company/<int:id_empresa>/internalEmployees')
api.add_resource(VistaConsultaPerfil,'/company/projects/<int:id_proyecto>/profiles')
api.add_resource(VistaCreacionPerfil,'/company/projects/<int:id_proyecto>/profiles')
api.add_resource(VistaFicha,'/company/projects/<int:id_proyecto>/files')


# Endpoints de Motor de Emparejamiento
api.add_resource(VistaMotorEmparejamiento,'/company/motorEmparejamiento')
api.add_resource(VistaMotorEmparejamientoTempFicha,'/company/motorEmparejamientoTempFicha')
api.add_resource(VistaResultadoEmparejamientoPorIdProyecto,'/company/motorEmparejamiento/proyectos/<int:id_proyecto>')
api.add_resource(VistaEliminarCandidatoMotorPorIdProyecto,'/company/motorEmparejamiento/proyectos/<int:id_proyecto>/candidatos/<int:id_candidato>')

# Endpoints de contratacion
api.add_resource(VistaContratoCandidato,'/company/contratoCandidato')

# Endpoints de Evaluación Desempeño Empleado
api.add_resource(VistaCreacionDesempenoEmpleado,'/company/desempenoEmpleado')

jwt = JWTManager(app)

