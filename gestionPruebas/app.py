from microservicioRedundanteLogin3 import create_app
from flask_restful import Resource,Api
from flask import Flask,request
import requests, json
from sqlalchemy.exc import IntegrityError

from datetime import date, datetime


from modelos import db, Usuario, UsuarioSchema, logValidadorSchema, logValidador
   
usuario_schema = UsuarioSchema()
log_validador_schema = logValidadorSchema()

app = create_app('default')

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/maestria/proyectoABC-arq-agiles/proyectoABC/monitoreoABC.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../monitoreoABC.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)

class VistaMicroservicio3(Resource):
    def get(self):


        fechaActual = datetime.now()
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                       Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()

        if usuario is None:
            log = logValidador(microservicio="Microservicio Redundante 3 ", mensaje="El usuario no existe", fecha=fechaActual)
            db.session.add(log)
            db.session.commit()
            return "El usuario no existe", 404
        else:      
            log = logValidador(microservicio="Microservicio Redundante 3 ", mensaje="Inicio de sesión exitoso desde microservicio", fecha=fechaActual)
            db.session.add(log)
            db.session.commit()      

            return {"mensaje": "Inicio de sesión exitoso desde microservicio"}
        


api.add_resource(VistaMicroservicio3,'/login3')