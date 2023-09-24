from gestionAutenticacionAutorizacion import create_app
from flask_restful import Resource,Api
from flask import Flask,request
import requests, json
from sqlalchemy.exc import IntegrityError

from datetime import date, datetime


from .modelos import db, Usuario, UsuarioSchema
   
usuario_schema = UsuarioSchema()

app = create_app('default')

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Uniandes123@proyecto1bd.c9mkfgyc1tlh.us-east-1.rds.amazonaws.com:5432/postgres'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../monitoreoABC.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)

class VistaAutenticacionAutorizacion(Resource):
    def get(self):

        print(request.json["usuario"])
        print(request.json["contrasena"])
        fechaActual = datetime.now()
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                       Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()

api.add_resource(VistaAutenticacionAutorizacion,'/login')