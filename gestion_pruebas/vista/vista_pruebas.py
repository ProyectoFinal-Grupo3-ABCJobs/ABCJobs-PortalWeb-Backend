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
            

class VistaRegistroResultadoPruebaTecnicaCandidatoEmparejado(Resource):
    @jwt_required()
    def put(self,id_proyecto,id_candidato,id_empresa,id_perfil):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            # encabezado_autorizacion = request.headers.get("Authorization")
            # datos_json = request.get_json()
            pruebaTecnica='TECNICA'
            res_candidato_pruebas_tecnica = Prueba.query.filter(Prueba.idProyecto == id_proyecto,Prueba.idCandidato == id_candidato,Prueba.idEmpresa == id_empresa,Prueba.tipoPrueba == pruebaTecnica,Prueba.idPerfil == id_perfil).first()
            
            if res_candidato_pruebas_tecnica:
                res_candidato_pruebas_tecnica.resultado = request.json['resultado']
                res_candidato_pruebas_tecnica.observaciones = request.json['observaciones']
                res_candidato_pruebas_tecnica.aprobado = bool(request.json['aprobado'])
                db.session.commit()
                dicCandidato = {
                         "idPrueba": res_candidato_pruebas_tecnica.idPrueba,
                         "tipoPrueba": res_candidato_pruebas_tecnica.tipoPrueba,
                         "fechaPrueba": res_candidato_pruebas_tecnica.fechaPrueba,
                         "resultado":res_candidato_pruebas_tecnica.resultado,
                         "observaciones": res_candidato_pruebas_tecnica.observaciones,
                         "idCandidato": res_candidato_pruebas_tecnica.idCandidato,
                         "candidatoNombre": res_candidato_pruebas_tecnica.candidatoNombre,
                         "idProyecto":res_candidato_pruebas_tecnica.idProyecto,
                         "proyectoNombre": res_candidato_pruebas_tecnica.proyectoNombre,
                         "idPerfil": res_candidato_pruebas_tecnica.idPerfil,
                         "perfilDescripcion":res_candidato_pruebas_tecnica.perfilDescripcion,
                         "aprobado": res_candidato_pruebas_tecnica.aprobado,
                         "candidatoNombre": res_candidato_pruebas_tecnica.candidatoNombre,
                         "estado":res_candidato_pruebas_tecnica.estado
                         }
                respuesta = jsonify(dicCandidato)
                respuesta.status_code = 200
                return respuesta
            else:
                mensaje = {
                    "menaje":"El candidato no tiene prueba tecnica"
                }
                respuesta = jsonify(mensaje)
                respuesta.status_code = 200
                return respuesta
        else:
            mensaje = {
                    "menaje":"Token invalido"
                }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta




class VistaObtenerPerfilesPorIdProyectoIdEmpresa(Resource):
    @jwt_required()
    def get(self,id_proyecto,id_empresa):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            # encabezado_autorizacion = request.headers.get("Authorization")
            # datos_json = request.get_json()
            pruebaTecnica='TECNICA'
            # id_empresa= 1000
            res_perfiles_proyecto = Prueba.query.filter(Prueba.idProyecto == id_proyecto,Prueba.idEmpresa == id_empresa,Prueba.tipoPrueba == pruebaTecnica).all()
            
            listaPerfiles = []
            lista_perfiles_unicos = []
            dicPerfiles = {}
            for res_perfil in res_perfiles_proyecto:
                dicPerfiles = {
                    "idPerfil": res_perfil.idPerfil,
                    "perfilDescripcion": res_perfil.perfilDescripcion
                }
                listaPerfiles.append(dicPerfiles)
            
            if len(listaPerfiles)>0:
                conjunto_diccionarios_unicos = {tuple(sorted(dic.items())) for dic in listaPerfiles}
                lista_perfiles_unicos = [dict(tupla) for tupla in conjunto_diccionarios_unicos]
            
            # return lista_perfiles_unicos

            listaPrincipalPerfiles = []
            dicMaestroPerfil ={    
                "idPerfil":"",
                "perfilDescripcion":"",
                "candidatos":[]     
            } 

            dicDetalleCandidatos ={    
                "idCandidato":"",
                "candidatoNombre":"",
            } 
            listaDetalleCandidatos = []

            # Buscar los candidatos por perfil
            for perfil_unico in lista_perfiles_unicos:

                res_candidatos_perfiles = Prueba.query.filter(Prueba.idProyecto == id_proyecto,Prueba.idEmpresa == id_empresa,Prueba.idPerfil == perfil_unico['idPerfil'],Prueba.tipoPrueba == pruebaTecnica).all()
                for res_candidato_perfil in res_candidatos_perfiles:
                    dicDetalleCandidatos ={    
                        "idCandidato":res_candidato_perfil.idCandidato,
                        "candidatoNombre":res_candidato_perfil.candidatoNombre,
                    } 
                    listaDetalleCandidatos.append(dicDetalleCandidatos)
                dicMaestroPerfil ={
                    "idPerfil":perfil_unico['idPerfil'],
                    "perfilDescripcion":perfil_unico['perfilDescripcion'],
                    "candidatos":listaDetalleCandidatos
                }
                listaDetalleCandidatos = []
                listaPrincipalPerfiles.append(dicMaestroPerfil)

            # print("El id del perfil a evaluar es: ", perfil_unico['idPerfil'])
            return listaPrincipalPerfiles

        else:
            mensaje = {
                    "menaje":"Token invalido"
                }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta
