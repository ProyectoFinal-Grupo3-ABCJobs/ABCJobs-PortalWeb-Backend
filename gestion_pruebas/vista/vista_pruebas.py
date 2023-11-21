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
            candidatos_aprobados_entrevista = Entrevista.query.filter(
                Entrevista.idEmpresa == id_empresa, Entrevista.aprobado == True ).all()
            
            if candidatos_aprobados_entrevista:
                listaTempCandidatosAprobados = []
                listaProyectos = []
                listaNombreProyectos= []
                listFinalMaster = []
                vlrIdProyecto = ''
                vlrNombreProyecto = ''
                vlrIdproyectoTmp = ''
                listaCandidatosAprobados = [entrevista_schema.dump(tr) for tr in candidatos_aprobados_entrevista]
                listaTempCandidatosAprobados = listaCandidatosAprobados[:]
                
                for dicCandidatosAprobados in listaCandidatosAprobados:
                    vlrIdProyecto = dicCandidatosAprobados['idProyecto']
                    vlrNombreProyecto = dicCandidatosAprobados['proyectoNombre']
                    for candidatosTemp in listaTempCandidatosAprobados:
                        vlrIdproyectoTmp = candidatosTemp['idProyecto']
                
                        if vlrIdProyecto == vlrIdproyectoTmp:

                            if vlrIdProyecto not in listaProyectos:

                                listaProyectos.append(vlrIdProyecto)
                                listaNombreProyectos.append(vlrNombreProyecto)

                # Construccion del maestro 1 - Proyectos Encabezado
                if len(listaProyectos) == len(listaNombreProyectos):
                    for index in range(len(listaProyectos)):
                        dicFicha = {
                            "idProyecto":listaProyectos[index],
                            "proyectoNombre":listaNombreProyectos[index],
                            "perfiles": [],
                        }
                        listFinalMaster.append(dicFicha)               
                #print("El encabezado de la peticion es:: ", listFinalMaster)
                listaPerfiles = []
                dicDetallePerfiles = {}
                for idx in range(len(listFinalMaster)):
                    perfiles_proyecto = (
                        db.session.query(Entrevista.idPerfil,Entrevista.perfilDescripcion)
                        .filter(Entrevista.idProyecto == listFinalMaster[idx]['idProyecto'])
                        .distinct()
                        .all())

                    for perfil in perfiles_proyecto:
                        dicDetallePerfiles = {
                            "idperfil": perfil[0],
                            "perfilNombre": perfil[1],
                            "candidatos":[]
                        }

                        listaPerfiles.append(dicDetallePerfiles)

                    listFinalMaster[idx]['perfiles']=listaPerfiles
                    listaPerfiles=[]
                listaPerfilesDepurados = []
                listarCandidatos = []
                dicDetalleCandidatos = {}
                for idx2 in range(len(listFinalMaster)):
                    listaPerfilesDepurados = listFinalMaster[idx2]['perfiles']
                    for idx3 in range(len(listaPerfilesDepurados)):
                        candidatos_aprobados = Entrevista.query.filter(
                            Entrevista.idProyecto==listFinalMaster[idx2]['idProyecto'], Entrevista.idPerfil == listaPerfilesDepurados[idx3]['idperfil'],Entrevista.aprobado == True ).all()
                        for cand in candidatos_aprobados:
                            dicDetalleCandidatos = {
                            "idCandidato": cand.idCandidato,
                            "nombreCandidato": cand.candidatoNombre,
                            }
                            listarCandidatos.append(dicDetalleCandidatos)

                        listFinalMaster[idx2]['perfiles'][idx3]['candidatos'] = listarCandidatos
                        listarCandidatos = []
                #respuesta = jsonify(listFinalMaster)
                #listFinalMaster.status_code = 200
                return listFinalMaster
            else:
                mensaje: dict = {
                    "mensaje 200": "La empresa no tiene candidatos a contratar"
                }
                respuesta = jsonify(mensaje)
                respuesta.status_code = 200
                return respuesta

# EndPoint para consumo desde empresa - Proceso para cargar la tabla de Entrevista
class VistaAdicionarCandidatosEmparejadosAEntrevista(Resource):
    #@jwt_required()
    def post(self):
        #tokenPayload = get_jwt_identity()
        #if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            
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
            "mensaje 201": "Entrevista registrada correctamente"
        }
        respuesta = jsonify(mensaje)
        respuesta.status_code = 201

        tipoPrueba = ['TECNICA', 'IDIOMA', 'HABILIDADES_BLANDAS', 'PERSONALIDAD']
    
        for i in range(4):
            nuevo_prueba_emparejado = Prueba(
            idProyecto = request.json['idProyecto'],
            tipoPrueba = tipoPrueba[i],
            proyectoNombre = request.json['nombreProyecto'],
            empresaNombre = request.json['nombreEmpresa'],
            idEmpresa = request.json['idEmpresa'],
            idCandidato=request.json['idCandidato'],
            candidatoNombre =request.json['nombreCandidato'],
            idPerfil=request.json['idPerfil'],
            perfilDescripcion =request.json['descripcionPerfil'])
        
            db.session.add(nuevo_prueba_emparejado)                                    
            db.session.commit()
            
            mensaje: dict = {
                "mensaje 201": "Pruebas registrada correctamente"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 201
        
        return respuesta


            

class VistaEliminarCandidatoTblEntrevistaPorIds(Resource):
    @jwt_required()
    def delete(self,id_proyecto,id_candidato,id_empresa):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            # encabezado_autorizacion = request.headers.get("Authorization")
            # datos_json = request.get_json()

            res_candidato_entrevista = Entrevista.query.filter(Entrevista.idProyecto == id_proyecto,Entrevista.idCandidato == id_candidato,Entrevista.idEmpresa == id_empresa).first()

            if res_candidato_entrevista:
                
                db.session.delete(res_candidato_entrevista)
                db.session.commit()

                mensaje: dict = {
                        "Mensaje 204": "Candidato eliminado de la tabla emparejamiento-perfil"
                    }
                respuesta = jsonify(mensaje)
                respuesta.status_code = 204
                return respuesta