from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from flask import jsonify
import hashlib, os, json

from modelo import Empresa, EmpresaSchema
empresa_schema = EmpresaSchema()


class VistaSaludServicio(Resource):
    def get(self):
          mensaje:dict = {'mensaje':"healthcheck OK"}
          respuesta = jsonify(mensaje)
          respuesta.status_code = 200
          return respuesta
