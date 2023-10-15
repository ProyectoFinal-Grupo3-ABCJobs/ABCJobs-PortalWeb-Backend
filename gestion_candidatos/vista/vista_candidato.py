from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from flask import jsonify
import hashlib, os, json

from modelo import Candidato, CandidatoSchema
candidate_schema = CandidatoSchema()

 class VistaRegistroCandidato(Resource):
    def post(self):

          try:
                if len(request.json["tipoIdentificacion"].strip())==0 or len(request.json["identificacion"].strip())==0 or len(request.json["nombre"].strip())==0 /
                 or len(request.json["direccion"].strip())==0 or len(request.json["telefono"].strip())==0 or len(request.json["profesion"].strip())==0 /
                 or len(request.json["aniosExperiencia"].strip())==0 or len(request.json["email"].strip())==0 or len(request.json["idCiudad"].strip())==0 /
                 or len(request.json["contrasena"].strip())==0 or len(request.json["ultimoEstudio"].strip())==0 or len(request.json["institucion"].strip())==0 /
                 or len(request.json["anioGrado"].strip())==0 or len(request.json["cargoUltimoEmpleo"].strip())==0 or len(request.json["empresa"].strip())==0 /
                 or len(request.json["anioIngreso"].strip())==0 or len(request.json["anioRetiro"].strip())==0:
                    return "Code 400: Hay campos obligatorios vacíos", 400
            except:
                return "Code 400: Hay campos obligatorios vacíos", 400

          nuevo_candidato = Candidato(
               tipoIdentificacion=request.json["tipoIdentificacion"],
               identificacion=request.json["identificacion"],
               nombre=request.json["nombre"],
               direccion=request.json["direccion"],
               telefono=request.json["telefono"],
               profesion=request.json["profesion"],
               aniosExperiencia=request.json["aniosExperiencia"],
               email=request.json["email"],
               idCiudad=request.json["idCiudad"],
               contrasena=request.json["contrasena"],
               ultimoEstudio=request.json["ultimoEstudio"],
               institucion=request.json["institucion"],
               anioGrado=request.json["anioGrado"],
               cargoUltimoEmpleo=request.json["cargoUltimoEmpleo"],
               empresa=request.json["empresa"],
               anioIngreso=request.json["anioIngreso"],
               anioRetiro=request.json["anioRetiro"],
               estado=False,
          )

          db.session.add(nuevo_candidato)
          db.session.commit()

          candidato_creado = Candidato.query.filter(
               Candidato.email == request.json["email"]
          ).first()

          return {
               "id": candidato_creado.idCandidato,
               "nombre": candidato_creado.nombre,
               "email": candidato_creado.email,
          }, 201

class VistaSaludServicio(Resource):
    def get(self):
          mensaje:dict = {'mensaje':"healthcheck OK"}
          respuesta = jsonify(mensaje)
          respuesta.status_code = 200
          return respuesta
