from microservicioReduntanteLogin1 import create_app
from flask_restful import Resource, Api
from flask import Flask, request
import requests
import json
from sqlalchemy.exc import IntegrityError

from datetime import date, datetime


from modelos import db, Usuario, UsuarioSchema, logValidadorSchema, logValidador
from modelos.modelos import ResultadoValidador

usuario_schema = UsuarioSchema()
log_validador_schema = logValidadorSchema()

app = create_app('default')

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\Users/USER/Documents/ANDES/Ciclo3/Arquitectura Ágil/Git/proyectoABC/monitoreoABC.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../monitoreoABC.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)


class VistaValidador(Resource):
    def post(self):

        resultadoVotacion = "Votación OK"
        fechaActual = datetime.now()

        logValidadorRedundante1 = logValidador.query.filter(
            logValidador.microservicio == "Microservicio Redundante 1 ").order_by(logValidador.id.desc()).first()
        logValidadorRedundante2 = logValidador.query.filter(
            logValidador.microservicio == "Microservicio Redundante 2 ").order_by(logValidador.id.desc()).first()
        logValidadorRedundante3 = logValidador.query.filter(
            logValidador.microservicio == "Microservicio Redundante 3 ").order_by(logValidador.id.desc()).first()
        db.session.commit()

        if(logValidadorRedundante1.mensaje == logValidadorRedundante2.mensaje and logValidadorRedundante2.mensaje != 
        logValidadorRedundante3.mensaje):
            resultadoVotacion = "El Microservicio 3 está fallando"
        elif(logValidadorRedundante1.mensaje == logValidadorRedundante3.mensaje and logValidadorRedundante3.mensaje != 
        logValidadorRedundante2.mensaje):
            resultadoVotacion = "El Microservicio 2 está fallando"
        elif(logValidadorRedundante2.mensaje == logValidadorRedundante3.mensaje and logValidadorRedundante3.mensaje != 
        logValidadorRedundante1.mensaje):
            resultadoVotacion = "El Microservicio 1 está fallando"

        resultadoValidador = ResultadoValidador(resultado= resultadoVotacion, fecha=fechaActual)
        db.session.add(resultadoValidador)
        db.session.commit()
            
api.add_resource(VistaValidador, '/validador')
