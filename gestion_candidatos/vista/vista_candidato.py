from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from flask import jsonify
import hashlib, os, json

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
               Candidato.email == request.json["email"]
          ).first()

          return {
               "id": candidato_creado.idCandidato,
               "nombre": candidato_creado.nombre,
               "identificacion": candidato_creado.identificacion
          }, 201

class VistaSaludServicio(Resource):
    def get(self):
          mensaje:dict = {'mensaje':"healthcheck OK"}
          respuesta = jsonify(mensaje)
          respuesta.status_code = 200
          return respuesta
