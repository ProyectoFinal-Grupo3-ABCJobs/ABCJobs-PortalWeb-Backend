from gestionAutenticacionAutorizacion import create_app
from flask_restful import Resource,Api
from flask import Flask,request
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime
import base64

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

        authorization = request.headers['Authorization']
        authorization = authorization[len('Basic '):]
        usuario_contraseña = base64.b64decode(authorization).decode('utf-8')
        # Divide el usuario y la contraseña
        usuario, contraseña = usuario_contraseña.split(':')

        usuario = Usuario.query.filter(Usuario.usuario == usuario,
                                       Usuario.contrasena == contraseña).first()
        db.session.commit()
        
        print(usuario)
        if usuario:
            return jsonify({"id": usuario.id})
        else:
            # Si no se encontró ningún resultado, puedes devolver un mensaje de error o un JSON vacío
            return "NO se encontró ningún usuario", 204

api.add_resource(VistaAutenticacionAutorizacion,'/login')