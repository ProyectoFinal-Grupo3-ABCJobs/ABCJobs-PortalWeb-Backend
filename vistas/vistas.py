
from time import sleep
from wsgiref import validate
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import requests
import time


   
usuario_schema = UsuarioSchema()


class VistaLogIn(Resource):

    def post(self):
        print(request.json["usuario"])
        print(request.json["contrasena"])
        r1 = requests.get("http://127.0.0.1:5001/login1", json={"usuario": request.json["usuario"], "contrasena": request.json["contrasena"]})
        r2 = requests.get("http://127.0.0.1:5002/login2", json={"usuario": request.json["usuario"], "contrasena": request.json["contrasena"]})
        r3 = requests.get("http://127.0.0.1:5003/login3", json={"usuario": request.json["usuario"], "contrasena": request.json["contrasena"]})
        time.sleep(2)
        validador = requests.post("http://127.0.0.1:5004/validador")