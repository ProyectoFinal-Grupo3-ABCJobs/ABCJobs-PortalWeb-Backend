from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
import hashlib, os, json


directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)

if carpeta_actual=='gestion_candidatos' or carpeta_actual=='app':
     from modelo import db, Candidato, CandidatoSchema
else:
     from gestion_candidatos.modelo import db, Candidato, CandidatoSchema

candidate_schema = CandidatoSchema()

class VistaRegistroInfoCandidato(Resource):
    def post(self):

          try:
                if len(request.json["tipoIdentificacion"].strip())==0 or len(request.json["identificacion"].strip())==0 or len(request.json["nombre"].strip())==0 or len(request.json["direccion"].strip())==0 or len(request.json["telefono"].strip())==0 or len(request.json["profesion"].strip())==0 or len(request.json["aniosExperiencia"].strip())==0 or len(request.json["idCiudad"].strip())==0 or len(request.json["idDepartamento"].strip())==0 or len(request.json["idPais"].strip())==0 or len(request.json["ultimoEstudio"].strip())==0 or len(request.json["institucion"].strip())==0 or len(request.json["anioGrado"].strip())==0 or len(request.json["idCiudadInst"].strip())==0 or len(request.json["idDepartamentoInst"].strip())==0 or len(request.json["cargoUltimoEmpleo"].strip())==0 or len(request.json["empresa"].strip())==0 or len(request.json["anioIngreso"].strip())==0 or len(request.json["palabrasClave"].strip())==0:
                    return "Code 400: Hay campos obligatorios vacíos", 400
          except:
                return "Code 400: Hay campos obligatorios vacíos", 400

          # Validar que la identificación no exista
          candidatoIdentificacion = Candidato.query.filter(
               Candidato.identificacion == request.json["identificacion"]
          ).first()

          if candidatoIdentificacion:
               return "Code 400: La identificación ya existe", 400
     

          nuevo_candidato = Candidato(
               tipoIdentificacion=request.json["tipoIdentificacion"],
               identificacion=request.json["identificacion"],
               nombre=request.json["nombre"],
               direccion=request.json["direccion"],
               telefono=request.json["telefono"],
               profesion=request.json["profesion"],
               aniosExperiencia=request.json["aniosExperiencia"],
               idCiudad=request.json["idCiudad"],
               idDepartamento=request.json["idDepartamento"],
               idPais=request.json["idPais"],
               ultimoEstudio=request.json["ultimoEstudio"],
               institucion=request.json["institucion"],
               anioGrado=request.json["anioGrado"],
               idCiudadInst=request.json["idCiudadInst"],
               idDepartamentoInst=request.json["idDepartamentoInst"],
               cargoUltimoEmpleo=request.json["cargoUltimoEmpleo"],
               empresa=request.json["empresa"],
               anioIngreso=request.json["anioIngreso"],
               anioRetiro=request.json["anioRetiro"],
               palabrasClave=request.json["palabrasClave"],
               estado=False,
          )

          db.session.add(nuevo_candidato)
          db.session.commit()

          candidato_creado = Candidato.query.filter(
               Candidato.identificacion == request.json["identificacion"]
          ).first()

          return {
               "id": candidato_creado.idCandidato,
               "nombre": candidato_creado.nombre,
               "identificacion": candidato_creado.identificacion
          }, 201



class VistaObtenerTodosCandidatos(Resource):
    @jwt_required()
    def get(self):
          tokenPayload = get_jwt_identity()
          if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
               candidatos = Candidato.query.filter(Candidato.estado == False).all()
               return [candidate_schema.dump(tr) for tr in candidatos]
          else:
               mensaje:dict = {'mensaje':"La petición viene de un usuario que no es empresa"}
               respuesta = jsonify(mensaje)
               respuesta.status_code = 400
               return respuesta



class VistaObtenerCandidatoPorId(Resource):
    @jwt_required()
    def get(self,id_candidato):
          tokenPayload = get_jwt_identity()
          if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
               candidato = Candidato.query.filter(Candidato.idCandidato == id_candidato).first()

               if candidato:
                    dicCandidato = {
                         "idCandidato": candidato.idCandidato,
                         "nombre": candidato.nombre,
                         "profesion": candidato.profesion,
                    }
                    respuesta = jsonify(dicCandidato)
                    respuesta.status_code = 200
                    return respuesta
               else:
                    mensaje:dict = {'mensaje 200':"El candidato no Existe"}
                    respuesta = jsonify(mensaje)
                    respuesta.status_code = 200
                    return respuesta


          else:
               mensaje:dict = {'mensaje':"La petición viene de un usuario que no es empresa"}
               respuesta = jsonify(mensaje)
               respuesta.status_code = 400
               return respuesta


class VistaSaludServicio(Resource):
    def get(self):
          mensaje:dict = {'mensaje':"healthcheck OK"}
          respuesta = jsonify(mensaje)
          respuesta.status_code = 200
          return respuesta
