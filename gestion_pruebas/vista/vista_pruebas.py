from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from datetime import datetime
import requests
import os
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
            pruebas_candidato = Prueba.query.filter(
                Prueba.idCandidato == id_candidato
            ).all()

            if len(pruebas_candidato) == 0:
                return "El candidato no tiene pruebas registradas", 404
            else:
                return [pruebas_schema.dump(tr) for tr in pruebas_candidato]
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
            print("Entrevista")
            entrevistas_candidato = Entrevista.query.filter(
                Entrevista.idCandidato == id_candidato
            ).all()

            if len(entrevistas_candidato) == 0:
                return "El candidato no tiene entrevistas", 404
            else:
                return [entrevista_schema.dump(tr) for tr in entrevistas_candidato]
        else:
            mensaje: dict = {
                "mensaje 1313": "El token enviado no corresponde al perfil del usuario"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta

# EndPoint para consumo desde empresa
class VistaResultadoEntrevistasCandidatosPorIdEmpresa(Resource):
    @jwt_required()
    def get(self, id_empresa):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            entrevistas_candidato_empresa = Entrevista.query.filter(
                Entrevista.idEmpresa == id_empresa, Entrevista.aprobado == True ).all()
            print("Resultado entrevistas son: ",entrevistas_candidato_empresa)



# EndPoint para consumo desde empresa - Proceso para cargar la tabla de Entrevista
class VistaAdicionarCandidatosEmparejadosAEntrevista(Resource):
    @jwt_required()
    def post(self):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            
            nuevo_entrevista_emparejado = Entrevista(
                idProyecto = request.json['idProyecto'],
                proyectoNombre = request.json['nombreProyecto'],
                empresaNombre = request.json['nombreEmpresa'],
                idEmpresa = request.json['idEmpresa'],
                idCandidato=request.json['idCandidato'],
                candidatoNombre =request.json['nombreCandidato'],
                idPerfil=request.json['idPerfil'],
                perfilDescripcion =request.json['descripcionPerfil'])
            
            db.session.add(nuevo_entrevista_emparejado)                                    
            db.session.commit()
            
            mensaje: dict = {
                "mensaje 201": "Entrevista registraa correctamente"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 201
            return respuesta
            
