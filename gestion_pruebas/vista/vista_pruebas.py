from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
import hashlib, os, json, jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime
import requests
directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)

if carpeta_actual == "gestion_pruebas" or carpeta_actual == "app":
    from modelo import (
        db,
        Prueba,
        Entrevista,
        PruebaSchema,
        EntrevistaSchema
       
    )
else:
    from gestion_pruebas.modelo import (
        db,
        Prueba,
        Entrevista,
        PruebaSchema,
        EntrevistaSchema
    )

pruebas_schema = PruebaSchema()
entrevista_schema = EntrevistaSchema()

class VistaSaludServicio(Resource):
    def get(self):
        mensaje: dict = {"mensaje": "healthcheck OK"}
        respuesta = jsonify(mensaje)
        respuesta.status_code = 200
        return respuesta
    
class VistaConsultaPruebasCandidato(Resource):
    @jwt_required()
    def get(self, id_candidato):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "CANDIDATO":
            return "Hola"
        else:
            mensaje: dict = {
                "mensaje 1313": "El token enviado no corresponde al perfil del usuario"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta
        
class VistaConsultaEntrevistasCandidato(Resource):
    @jwt_required()
    def get(self, id_candidato):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "CANDIDATO":
            return "Entrevista"
        else:
            mensaje: dict = {
                "mensaje 1313": "El token enviado no corresponde al perfil del usuario"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta

