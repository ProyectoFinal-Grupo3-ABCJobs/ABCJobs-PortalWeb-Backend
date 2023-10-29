from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import jsonify
import hashlib, os, json,jwt
from jwt.exceptions import InvalidTokenError

directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)

if carpeta_actual=='gestion_empresas' or carpeta_actual=='app':
     from modelo import db, Empresa, EmpresaSchema, Proyecto, ProyectoSchema
else:
     from gestion_empresas.modelo import db, Empresa, EmpresaSchema, Proyecto, ProyectoSchema

empresa_schema = EmpresaSchema()
proyecto_schema= ProyectoSchema()

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
    
class VistaConsultaProyectoPorEmpresa(Resource):

     @jwt_required()
     def get(self,id_empresa):

          tokenPayload = get_jwt_identity()
          if tokenPayload['tipoUsuario'].upper() == 'EMPRESA':
               proyectos_empresa = Proyecto.query.filter(
               Proyecto.empresa_id == id_empresa
          ).all()

               if len(proyectos_empresa)==0:
                    
                    mensaje:dict = {'mensaje 1212':"La empresa no tiene proyectos creados"}
                    respuesta = jsonify(mensaje)
                    respuesta.status_code = 200
                    return respuesta
               else:

                    return [proyecto_schema.dump(tr) for tr in proyectos_empresa]
          else:
               mensaje:dict = {'mensaje 1313':"El token enviado no corresponde al perfil del usuario"}
               respuesta = jsonify(mensaje)
               respuesta.status_code = 401
               return respuesta


class VistaCreacionProyecto(Resource):

     @jwt_required()
     def post(self,id_empresa):

          current_user = get_jwt_identity()

          if current_user.upper() == 'EMPRESA':
               
               print("La empresa tiene proyectos")
               try:
                    if len(request.json["nombreProyecto"].strip())==0 or len(str(request.json["fechaInicio"]).strip())==0:
                         return "Code 400: Hay campos obligatorios vacíos", 400
               except:
                    return "Code 400: Hay campos obligatorios vacíos", 400
               
               proyectoNombre = Proyecto.query.filter(
               Proyecto.nombreProyecto == request.json["nombreProyecto"]).first()          
               if not proyectoNombre is None:
                    return "Ya se encuentra un proyecto con ese nombre registrado", 409
               
               nuevo_proyecto = Proyecto(
                    nombreProyecto=request.json["nombreProyecto"],
                    fechaInicio=request.json["fechaInicio"],
                    empresa_id=id_empresa
               )

               db.session.add(nuevo_proyecto)
               db.session.commit()

               proyecto_creado = Proyecto.query.filter(
                    Proyecto.nombreProyecto == request.json["nombreProyecto"]
               ).first()

               return {
                    "id": proyecto_creado.idProyecto,
                    "nombreProyecto": proyecto_creado.nombreProyecto,
                    "fechaInicio": proyecto_creado.fechaInicio,
               }, 201
          


          else:
               mensaje:dict = {'mensaje':"El token enviado no corresponde al perfil del usuario"}
               respuesta = jsonify(mensaje)
               respuesta.status_code = 401
               return respuesta
