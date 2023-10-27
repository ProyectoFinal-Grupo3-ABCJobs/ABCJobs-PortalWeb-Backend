from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from flask import jsonify
import hashlib, os, json

directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)

if carpeta_actual=='gestion_empresas' or carpeta_actual=='app':
     from modelo import db, Empresa, EmpresaSchema
else:
     from gestion_empresas.modelo import db, Empresa, EmpresaSchema

empresa_schema = EmpresaSchema()

class VistaSaludServicio(Resource):
    def get(self):
          mensaje:dict = {'mensaje':"healthcheck OK"}
          respuesta = jsonify(mensaje)
          respuesta.status_code = 200
          return respuesta
    
    

class VistaRegistroEmpresa(Resource):
    def post(self):

          try:
                if len(request.json["nit"].strip())==0 or len(request.json["razonSocial"].strip())==0 or len(request.json["direccion"].strip())==0 or len(request.json["telefono"].strip())==0 or len(request.json["idCiudad"].strip())==0 :
                    return "Code 400: Hay campos obligatorios vacíos", 400
          except:
                return "Code 400: Hay campos obligatorios vacíos", 400
          
          razonSocial = Empresa.query.filter(
            Empresa.razonSocial == request.json["razonSocial"]).first()          
          if not razonSocial is None:
            return "No se puede crear la empresa. La Razón Social ya se encuentra registrada", 409
          
          nit = Empresa.query.filter(
            Empresa.nit == request.json["nit"]).first()
          if not nit is None:
            return "No se puede crear la empresa. El Nit ya se encuentra registrado", 409

          nueva_empresa = Empresa(
               nit=request.json["nit"],
               razonSocial=request.json["razonSocial"],
               direccion=request.json["direccion"],
               telefono=request.json["telefono"],
               idCiudad=request.json["idCiudad"]
          )

          db.session.add(nueva_empresa)
          db.session.commit()

          empresa_creada = Empresa.query.filter(
               Empresa.nit == request.json["nit"]
          ).first()

          return {
               "id": empresa_creada.idEmpresa,
               "razonSocial": empresa_creada.razonSocial,
               "nit": empresa_creada.nit,
          }, 201
