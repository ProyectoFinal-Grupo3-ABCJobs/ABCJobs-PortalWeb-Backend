from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
import hashlib, os, json, jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime
import requests
import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)

if carpeta_actual == "gestion_empresas" or carpeta_actual == "app":
    from modelo import (
        db,
        Empresa,
        EmpresaSchema,
        Proyecto,
        ProyectoSchema,
        EmpleadoInterno,
        EmpleadoInternoSchema,
        Ficha,
        FichaSchema,
        Perfil,
        PerfilSchema,
        FichaEmpleadoInterno,
        FichaPerfil,
        FichaPerfilSchema,
        FichaCandidatoEmparejadoPerfil,
        FichaCandidatoEmparejadoPerfilSchema,
        Contrato,
        ContratoSchema,
        DesempenoEmpleado,
        DesempenoEmpleadoSchema
    )
else:
    from gestion_empresas.modelo import (
        db,
        Empresa,
        EmpresaSchema,
        Proyecto,
        ProyectoSchema,
        EmpleadoInterno,
        EmpleadoInternoSchema,
        Ficha,
        FichaSchema,
        Perfil,
        PerfilSchema,
        FichaEmpleadoInterno,
        FichaPerfil,
        FichaPerfilSchema,
        FichaCandidatoEmparejadoPerfil,
        FichaCandidatoEmparejadoPerfilSchema,
        Contrato,
        ContratoSchema,
        DesempenoEmpleado,
        DesempenoEmpleadoSchema
    )

contrato_schema = ContratoSchema()
empresa_schema = EmpresaSchema()
proyecto_schema = ProyectoSchema()
empleado_interno_schema = EmpleadoInternoSchema()
perfil_schema = PerfilSchema()
ficha_schema = FichaSchema()
ficha_candidato_emparejado_perfil_schema = FichaCandidatoEmparejadoPerfilSchema()
ficha_perfil_schema = FichaPerfilSchema()
desempenoEmpleado_schema = DesempenoEmpleadoSchema

class VistaSaludServicio(Resource):
    def get(self):
        mensaje: dict = {"mensaje": "healthcheck OK"}
        respuesta = jsonify(mensaje)
        respuesta.status_code = 200
        return respuesta

class VistaRegistroEmpresa(Resource):
    def post(self):
        try:
            if (
                len(request.json["nit"].strip()) == 0
                or len(request.json["razonSocial"].strip()) == 0
                or len(request.json["direccion"].strip()) == 0
                or len(request.json["telefono"].strip()) == 0
                or len(request.json["idCiudad"].strip()) == 0
            ):
                return "Code 400: Hay campos obligatorios vacíos", 400
        except:
            return "Code 400: Hay campos obligatorios vacíos", 400

        razonSocial = Empresa.query.filter(
            Empresa.razonSocial == request.json["razonSocial"]
        ).first()
        if not razonSocial is None:
            return (
                "No se puede crear la empresa. La Razón Social ya se encuentra registrada",
                409,
            )

        nit = Empresa.query.filter(Empresa.nit == request.json["nit"]).first()
        if not nit is None:
            return (
                "No se puede crear la empresa. El Nit ya se encuentra registrado",
                409,
            )

        nueva_empresa = Empresa(
            nit=request.json["nit"],
            razonSocial=request.json["razonSocial"],
            direccion=request.json["direccion"],
            telefono=request.json["telefono"],
            idCiudad=request.json["idCiudad"],
            idUsuario=request.json["idUsuario"],
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
    def get(self, id_empresa):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            proyectos_empresa = Proyecto.query.filter(
                Proyecto.empresa_id == id_empresa
            ).all()

            if len(proyectos_empresa) == 0:
                mensaje: dict = {
                    "mensaje_1212": "La empresa no tiene proyectos creados"
                }
                respuesta = jsonify(mensaje)
                respuesta.status_code = 200
                return respuesta
            else:
                return [proyecto_schema.dump(tr) for tr in proyectos_empresa]
        else:
            mensaje: dict = {
                "mensaje 1313": "El token enviado no corresponde al perfil del usuario"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta

class VistaConsultaProyectoPorEmpresa(Resource):
    @jwt_required()
    def get(self, id_empresa):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            proyectos_empresa = Proyecto.query.filter(
                Proyecto.empresa_id == id_empresa
            ).all()

            if len(proyectos_empresa) == 0:
                mensaje: dict = {
                    "mensaje 1212": "La empresa no tiene proyectos creados"
                }
                respuesta = jsonify(mensaje)
                respuesta.status_code = 200
                return respuesta
            else:
                return [proyecto_schema.dump(tr) for tr in proyectos_empresa]
        else:
            mensaje: dict = {
                "mensaje 1313": "El token enviado no corresponde al perfil del usuario"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta

class VistaListaProyectosSinFichaPorIdEmpresa(Resource):
    @jwt_required()
    def get(self, id_empresa):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            proyectos_empresa = Proyecto.query.filter(
                Proyecto.empresa_id == id_empresa
            ).all()

            if len(proyectos_empresa) == 0:
                mensaje: dict = {
                    "mensaje 1212": "La empresa no tiene proyectos creados"
                }
                respuesta = jsonify(mensaje)
                respuesta.status_code = 200
                return respuesta
            else:
                dicProyectoSinFicha = {}
                listaProyectoSinFicha = []
                for proyecto in proyectos_empresa:
                    ficha_proyecto = Ficha.query.filter(Ficha.idProyecto == proyecto.idProyecto).all()
                    if not(ficha_proyecto):
                        dicProyectoSinFicha = {
                            "idProyecto": proyecto.idProyecto,
                            "nombreProyecto": proyecto.nombreProyecto,
                            "numeroColaboradores": proyecto.numeroColaboradores,
                            "fechaInicio":proyecto.fechaInicio.strftime("%Y-%m-%d"),
                            "empresa_id": proyecto.empresa_id
                        }
                        listaProyectoSinFicha.append(dicProyectoSinFicha)
                return listaProyectoSinFicha
        else:
            mensaje: dict = {
                "mensaje 1313": "El token enviado no corresponde al perfil del usuario"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta



class VistaObtenerEmpresaPorIdUsuario(Resource):
    @jwt_required()
    def post(self):
        tokenPayload = get_jwt_identity()

        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            usuario_empresa = Empresa.query.filter(
                Empresa.idUsuario == tokenPayload["idUsuario"]
            ).first()

        if usuario_empresa:
            mensaje: dict = {
                "Mensaje": "El usuario con empresa asignada",
                "idEmpresa": usuario_empresa.idEmpresa,
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 200
            return respuesta
        else:
            mensaje: dict = {
                "Mensaje 201": "El usuario no tiene empresa asignada",
                "idEmpresa": "Sin Empresa",
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 200
            return respuesta

class VistaCreacionProyecto(Resource):
    @jwt_required()
    def post(self, id_empresa):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            try:
                if (
                    len(request.json["nombreProyecto"].strip()) == 0
                    or len(str(request.json["fechaInicio"]).strip()) == 0
                ):
                    return "Code 400: Hay campos obligatorios vacíos", 400
            except:
                return "Code 400: Hay campos obligatorios vacíos", 400

            proyectoNombre = Proyecto.query.filter(
                Proyecto.nombreProyecto == request.json["nombreProyecto"]
            ).first()
            if not proyectoNombre is None:
                return "Ya se encuentra un proyecto con ese nombre registrado", 409

            fecha_inicio_str = request.json["fechaInicio"]

            try:
                fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
            except ValueError:
                return "Formato de fecha inválido. Usa YYYY-MM-DD", 400

            nuevo_proyecto = Proyecto(
                nombreProyecto=request.json["nombreProyecto"],
                fechaInicio=fecha_inicio,
                empresa_id=id_empresa,
            )

            db.session.add(nuevo_proyecto)
            db.session.commit()

            proyecto_creado = Proyecto.query.filter(
                Proyecto.nombreProyecto == request.json["nombreProyecto"]
            ).first()

            fecha_str = (
                proyecto_creado.fechaInicio.strftime("%Y-%m-%d")
                if proyecto_creado.fechaInicio
                else None
            )

            return {
                "id": proyecto_creado.idProyecto,
                "nombreProyecto": proyecto_creado.nombreProyecto,
                "fechaInicio": fecha_str,
            }, 201

        else:
            mensaje: dict = {
                "mensaje": "El token enviado no corresponde al perfil del usuario"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta

class VistaEmpladoInterno(Resource):
    @jwt_required()
    def get(self, id_empresa):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            empleados_empresa = EmpleadoInterno.query.filter(
                EmpleadoInterno.idEmpresa == id_empresa
            ).all()

            if len(empleados_empresa) == 0:
                return "La empresa no tiene empleados internos asignados", 404
            else:
                return [empleado_interno_schema.dump(tr) for tr in empleados_empresa]
        else:
            return "El token enviado no corresponde al perfil del usuario", 401

class VistaConsultaPerfil(Resource):
    @jwt_required()
    def get(self, id_proyecto):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            perfiles_proyecto = Perfil.query.filter(
                Perfil.idProyecto == id_proyecto
            ).all()

            if len(perfiles_proyecto) == 0:
                return "El proyecto no tiene perfiles asociados", 404
            else:
                return [perfil_schema.dump(tr) for tr in perfiles_proyecto]
        else:
            return "El token enviado no corresponde al perfil del usuario", 401


class VistaConsultaTodosPerfiles(Resource):
    @jwt_required()
    def get(self):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            perfiles_proyecto = Perfil.query.filter(              
            ).all()

            if len(perfiles_proyecto) == 0:
                return "El proyecto no tiene perfiles asociados", 404
            else:
                return [perfil_schema.dump(tr) for tr in perfiles_proyecto]
        else:
            return "El token enviado no corresponde al perfil del usuario", 401

class VistaCreacionPerfil(Resource):
    @jwt_required()
    def post(self, id_proyecto):
        tokenPayload = get_jwt_identity()        
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            proyecto = Proyecto.query.filter(Proyecto.idProyecto == id_proyecto).first()
            if proyecto is None:
                return "El proyecto no existe", 404
            else:
                data = request.get_json()
                perfil = Perfil(
                    nombre=data.get("nombre"),
                    descripcion=data.get("descripcion"),
                    idProyecto=id_proyecto,
                )
                db.session.add(perfil)
                db.session.commit()

                return {
                    "id": perfil.idPerfil,
                    "nombre": perfil.nombre,
                    "descripcion": perfil.descripcion,
                }, 201

class VistaFicha(Resource):
    @jwt_required()
    def post(self, id_proyecto):
        try:
            tokenPayload = get_jwt_identity()
            if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
                proyecto = Proyecto.query.filter(
                    Proyecto.idProyecto == id_proyecto
                ).first()
                if proyecto is None:
                    return "El proyecto no existe", 404
                else:
                    ficha = Ficha(idProyecto=id_proyecto)
                    db.session.add(ficha)
                    db.session.commit()

                    data = request.get_json()
                    for empleado in data.get("empleados"):
                        empleado = FichaEmpleadoInterno(
                            idFicha=ficha.idFicha, idEmpleado=empleado["idEmpleado"]
                        )
                        db.session.add(empleado)

                    for perfil in data.get("perfiles"):
                        perfil = FichaPerfil(
                            idFicha=ficha.idFicha, idPerfil=perfil["idPerfil"]
                        )
                        db.session.add(perfil)

                    db.session.commit()
                    return "La ficha se creo correctamente", 201
            else:
                return "El token enviado no corresponde al perfil del usuario", 401
        except Exception as e:
            return "Ha ocurrido un error inesperado" + str(e), 500

class VistaAsignacionEmpleado(Resource):
    @jwt_required()
    def post(self, id_empresa):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            try:
                if (
                    len(request.json["tipoIdentificacion"].strip()) == 0
                    or len(str(request.json["identificacion"]).strip()) == 0
                    or len(str(request.json["nombre"]).strip()) == 0
                    or len(str(request.json["cargo"]).strip()) == 0
                ):
                    return "Code 400: Hay campos obligatorios vacíos", 400
            except:
                return "Code 400: Hay campos obligatorios vacíos", 400

            empleadoIdentificacion = EmpleadoInterno.query.filter(
                EmpleadoInterno.identificacion == request.json["identificacion"]
            ).first()
            if not empleadoIdentificacion is None:
                return "Ya se encuentra registrado un empleado con ese documento", 409

            nuevo_empleado = EmpleadoInterno(
                tipoIdentificacion=request.json["tipoIdentificacion"],
                identificacion=request.json["identificacion"],
                nombre=request.json["nombre"],
                cargo=request.json["cargo"],
                idEmpresa=id_empresa,
            )

            db.session.add(nuevo_empleado)
            db.session.commit()

            empleado_creado = EmpleadoInterno.query.filter(
                EmpleadoInterno.identificacion == request.json["identificacion"]
            ).first()

            return {
                "id": empleado_creado.idEmpleado,
                "nombre": empleado_creado.nombre,
                "cargo": empleado_creado.cargo,
            }, 201

        else:
            mensaje: dict = {
                "mensaje": "El token enviado no corresponde al perfil del usuario"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta

class VistaMotorEmparejamientoInterno(Resource):    
    #def ejecutarEmparejamiento(self,token):
    #@jwt_required()
    def post(self):
        token = request.headers.get("Authorization")
        #tokenPayload = get_jwt_identity()
        #clave_perfiles = "perfiles"
        #clave_ficha = "idFicha"
        #if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
        
        fichasEmparejadas = Ficha.query.filter(Ficha.estadoEmparejamiento == True).all()

        if fichasEmparejadas:
            for fichaEmparejada in fichasEmparejadas:
                fichasEmparejadas = FichaCandidatoEmparejadoPerfil.query.filter(FichaCandidatoEmparejadoPerfil.idFicha == fichaEmparejada.idFicha).first()
                if not(fichasEmparejadas):
                    db.session.query(Ficha).filter(Ficha.idFicha == fichaEmparejada.idFicha).update({Ficha.estadoEmparejamiento:False})
                    db.session.commit()

        fichasSinEmparejar = Ficha.query.filter(Ficha.estadoEmparejamiento == False).all()
        
        if fichasSinEmparejar:
            encabezados_con_autorizacion = {
                            "Content-Type": "application/json",
                            "Authorization": token,
                            }

            jsonCandidatos = requests.get("http://127.0.0.1:5001/candidate/getAll",
            #jsonCandidatos = requests.get("http://loadbalancerproyectoabc-735612126.us-east-2.elb.amazonaws.com:5001/candidate/getAll",
                                                        headers=encabezados_con_autorizacion)

            if jsonCandidatos.status_code != 200:
                mensaje: dict = {
                    "Mensaje 401": "El servicio de Candidato en el recurso getAll no esta respondiento"
                }
                respuesta = jsonify(mensaje)
                respuesta.status_code = 401
                return respuesta

            if len(jsonCandidatos.json()) == 0:
                mensaje: dict = {
                    "Mensaje 200": "El servicio candidato GetAll restorno sin datos"
                }
                respuesta = jsonify(mensaje)
                respuesta.status_code = 200
                return respuesta
            else:
                dic_candidatos_emparejados:dict = {}
                # Obtengo la lista de candidatos del requesto
                lista_candidatos = jsonCandidatos.json()

                for ficha in fichasSinEmparejar:
 #                   print("El id de la ficha es: ", ficha.idFicha)
                    perfilesFicha = FichaPerfil.query.filter(FichaPerfil.idFicha == ficha.idFicha).all()

                    listaPerfilesEnFicha = [ficha_perfil_schema.dump(tr) for tr in perfilesFicha]

                    for idperfil in listaPerfilesEnFicha:
                        #print("El nombre perfil: ", idperfil['idPerfil'])
                        descripcionPerfiles = Perfil.query.filter(Perfil.idPerfil == idperfil['idPerfil']).first()
                        if descripcionPerfiles:
                            
                            for candidato in lista_candidatos:

                                # Llamado al motor de emparejamiento
                                resultadoEmparejamiento = self.motorEmparejamiento(descripcionPerfiles.descripcion, candidato['palabrasClave'])
                                if resultadoEmparejamiento:
                                  
                                    # Busco en Ficha el idProyecto
                                    ficha_proyecto = Ficha.query.filter(Ficha.idFicha == ficha.idFicha).first()
                                    if not(ficha):
                                        mensaje: dict = {
                                        "Mensaje 200": f'La ficha {ficha.idFicha} no tiene proyecto asociado '
                                        }
                                        respuesta = jsonify(mensaje)
                                        respuesta.status_code = 200
                                        return respuesta
                                    
                                    # Busco en [Proyecto] el idEmpresa, adicional tomo el nombre del proyecto
                                    proyecto = Proyecto.query.filter(Proyecto.idProyecto == ficha_proyecto.idProyecto).first()
                                    if not(ficha):
                                        mensaje: dict = {
                                        "Mensaje 200": f'El proyecto: {ficha_proyecto.idProyecto} - no existe'
                                        }
                                        respuesta = jsonify(mensaje)
                                        respuesta.status_code = 200
                                        return respuesta
                                    

                                    # Busco en [Empresa] con el idEmpresa, el nombre de la empresa
                                    empresa = Empresa.query.filter(Empresa.idEmpresa == proyecto.empresa_id).first()
                                    if not(ficha):
                                        mensaje: dict = {
                                        "Mensaje 200": f'La empresa: {proyecto.empresa_id} - no existe'
                                        }
                                        respuesta = jsonify(mensaje)
                                        respuesta.status_code = 200
                                        return respuesta

                                    nuevo_candidato_emparejado = FichaCandidatoEmparejadoPerfil(
                                            idFicha=ficha.idFicha,
                                            idProyecto = ficha_proyecto.idProyecto,
                                            nombreProyecto = proyecto.nombreProyecto,
                                            nombreEmpresa = empresa.razonSocial,
                                            idEmpresa = proyecto.empresa_id,
                                            idCandidato=candidato["idCandidato"],
                                            nombreCandidato=candidato["nombre"],
                                            idPerfil=idperfil['idPerfil'],
                                            descripcionPerfil=descripcionPerfiles.descripcion                           
                                        )

                                    dic_candidatos_emparejados = {
                                            "idFicha":ficha.idFicha,
                                            "idProyecto" : ficha_proyecto.idProyecto,
                                            "nombreProyecto" : proyecto.nombreProyecto,
                                            "nombreEmpresa" : empresa.razonSocial,
                                            "idEmpresa" : proyecto.empresa_id,
                                            "idCandidato":candidato["idCandidato"],
                                            "nombreCandidato":candidato["nombre"],
                                            "idPerfil":idperfil['idPerfil'],
                                            "descripcionPerfil":descripcionPerfiles.descripcion
                                    }

                                    db.session.add(nuevo_candidato_emparejado)                                    
                                    db.session.commit()
                                    print("Aca estoy para cada uno candidato emparejado")
                                    # llamo al MS de pruebas y entrevista:
                                    jsonEntrevistas = requests.post("http://127.0.0.1:5003/test/interviews",
                                                                               headers=encabezados_con_autorizacion, json=dic_candidatos_emparejados)
                                    #jsonEntrevistas = requests.post("http://loadbalancerproyectoabc-735612126.us-east-2.elb.amazonaws.com:5003/test/interviews",
                                    #                                            headers=encabezados_con_autorizacion, json=dic_candidatos_emparejados)

                                    if jsonEntrevistas.status_code != 201:
                                        mensaje: dict = {
                                            "mensaje 401": "El servicio de Candidato en el recurso /test/interviews no esta respondiendo"
                                        }
                                        respuesta = jsonify(mensaje)
                                        respuesta.status_code = 401
                                        return respuesta


                    # Actualizar el estado de la ficha
                    db.session.query(Ficha).filter(Ficha.idFicha == ficha.idFicha).update({Ficha.estadoEmparejamiento: True})
                    db.session.commit()

                mensaje: dict = {
                        "Mensaje 200": "Proceso de emparejamiento realizado correctamente!"
                    }
                respuesta = jsonify(mensaje)
                respuesta.status_code = 200
                return respuesta

        else:
            mensaje: dict = {
                        "Mensaje 200": "No hay fichas para emparejar"
                    }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 200
            return respuesta

    # # def motorEmparejamiento(self, perfil, listaPalabras):
    def motorEmparejamiento(self, descripcionCargo, palabrasclaves):
        listaPalabrasClave = []
        listaPalabrasClave = palabrasclaves.split(",")

        nlp = spacy.load("es_core_news_sm")

        # Texto de ejemplo en español
        texto = descripcionCargo.upper().strip()
        lista = []

        # Procesar el texto con spaCy
        doc = nlp(texto)

        # Inicializar una variable para verificar si la palabra está en el texto
        emparejado = False
        
        # Palabra que deseas buscar
        for palabra in listaPalabrasClave:

        # Iterar a través de las palabras tokenizadas
            for token in doc:
                
                    if token.text == palabra.upper().strip():
                        emparejado = True
                        return emparejado
        return emparejado


# class VistaResultadoEmparejamientoPorIdProyecto(Resource):
#     @jwt_required()
#     def get(self,id_proyecto):
      
#         id_ficha = ''
#         tokenPayload = get_jwt_identity()
#         if tokenPayload["tipoUsuario"].upper() == "EMPRESA":

#             ficha = Ficha.query.filter(Ficha.idProyecto == id_proyecto).first()

#             if not(ficha):
#                 mensaje: dict = {
#                     "Mensaje 200": f'El proyecto {id_proyecto} no tiene ficha asociada '
#                 }
#                 respuesta = jsonify(mensaje)
#                 respuesta.status_code = 200
#                 return respuesta

#             registros_ficha = (
#                 FichaCandidatoEmparejadoPerfil.query.filter(
#                     FichaCandidatoEmparejadoPerfil.idFicha
#                     == ficha.idFicha
#                 ).all()
#             )

#             listTemp = []
#             listIdPerfil = []
#             if registros_ficha:

#                 listaTodosRegistrosFicha = [ficha_candidato_emparejado_perfil_schema.dump(tr) for tr in registros_ficha]

#                 listTemp = listaTodosRegistrosFicha[:]
#                 listaPerfiles = []

#                 listaDescperfiles= []

#                 listFinalMaster = []
#                 listFinalDetalle = []
#                 for dicFicha in listaTodosRegistrosFicha:
#                     vlrIdPerfil = dicFicha['idPerfil']
#                     vlrDescPerfil = dicFicha['descripcionPerfil']
#                     for fichaTemp in listTemp:
#                         vlrIdPerfilTmp = fichaTemp['idPerfil']

#                         if vlrIdPerfil == vlrIdPerfilTmp:

#                             if vlrIdPerfil not in listaPerfiles:

#                                 listaPerfiles.append(vlrIdPerfil)
#                                 listaDescperfiles.append(vlrDescPerfil)

#                 # Construccion del maestro
#                 if len(listaPerfiles) == len(listaDescperfiles):
#                     for index in range(len(listaPerfiles)):
#                         dicFicha = {
#                             "idPerfil":listaPerfiles[index],
#                             "descripcionPerfil":listaDescperfiles[index],
#                             "candidatos": [],
#                         }
#                         listFinalMaster.append(dicFicha)

#                 # Contruccion del detalle
#                 for perfil in range(len(listFinalMaster)):
#                     #print("Perfil", perfil['idPerfil'])
                   
#                     for candidato in listaTodosRegistrosFicha:
                   
#                         #print("Hola")
#                         if listFinalMaster[perfil]['idPerfil'] == candidato['idPerfil']:
                            
#                             dicDetalleCandidato = {
#                             "idCandidato": candidato['idCandidato'],
#                             "nombreCandidato": candidato['nombreCandidato'],
#                             "estado": candidato['estado']
#                         }                       

#                             listFinalDetalle.append(dicDetalleCandidato)
                    
#                     listFinalMaster[perfil]['candidatos']= listFinalDetalle
#                     listFinalDetalle = []
               
#                 return listFinalMaster
#             else:
#                 mensaje: dict = {
#                     "Mensaje 200": "La ficha no tiene candidatos emparejados"
#                 }
#                 respuesta = jsonify(mensaje)
#                 respuesta.status_code = 200
#                 return respuesta

class VistaEliminarCandidatoMotorPorIdProyecto(Resource):
    @jwt_required()
    def delete(self,id_proyecto,id_candidato):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            res_ficha_candidato_perfil = FichaCandidatoEmparejadoPerfil.query.filter(FichaCandidatoEmparejadoPerfil.idProyecto == id_proyecto,FichaCandidatoEmparejadoPerfil.idCandidato == id_candidato).first()

            if res_ficha_candidato_perfil:
                
                db.session.delete(res_ficha_candidato_perfil)
                db.session.commit()

                mensaje: dict = {
                        "Mensaje 204": "Candidato eliminado de la tabla emparejamiento-perfil"
                    }
                respuesta = jsonify(mensaje)
                respuesta.status_code = 204
                return respuesta

class VistaContratoCandidato(Resource):
    @jwt_required()
    def post(self):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":

            nuevo_contrato = Contrato(
               numeroContrato=request.json["numeroContrato"],
               idCandidato=request.json["idCandidato"],
               nombreCandidato=request.json["nombreCandidato"],
               idEmpresa=request.json["idEmpresa"],
               idProyecto=request.json["idProyecto"],
               idCargo=request.json["idCargo"])
            db.session.add(nuevo_contrato)
            db.session.commit()

            mensaje: dict = {
                        "Mensaje 201": "Contrato almacenado correctamente"
                    }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 201
            return respuesta

class VistaCreacionDesempenoEmpleado(Resource):
    @jwt_required()
    def post(self, id_contrato):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            try:
                if (
                    len(request.json["calificacion"].strip()) == 0
                    or len(str(request.json["aspectosResaltar"]).strip()) == 0
                    or len(str(request.json["aspectosMejorar"]).strip()) == 0
                ):
                    return "Code 400: Hay campos obligatorios vacíos", 400
            except:
                return "Code 400: Hay campos obligatorios vacíos", 400

            nuevo_desempenoEmpleado = DesempenoEmpleado(
                idContrato=id_contrato,
                calificacion=request.json["calificacion"],
                aspectosResaltar=request.json["aspectosResaltar"],
                aspectosMejorar=request.json["aspectosMejorar"]
            )

            db.session.add(nuevo_desempenoEmpleado)
            db.session.commit()

            desempenoEmpleado_creado = DesempenoEmpleado.query.filter(
                DesempenoEmpleado.idContrato == id_contrato
            ).first()

            return {
                "id": desempenoEmpleado_creado.idDesempeno,
                "calificacion": desempenoEmpleado_creado.calificacion,
                "aspectosResaltar": desempenoEmpleado_creado.aspectosResaltar,
                "aspectosMejorar": desempenoEmpleado_creado.aspectosMejorar,
            }, 201

        else:
            mensaje: dict = {
                "mensaje": "El token enviado no corresponde al perfil del usuario"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta
        
class VistaObtenerContratosPorEmpresa(Resource):
    @jwt_required()
    def get(self, id_empresa):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            contratos = Contrato.query.filter(Contrato.idEmpresa == id_empresa).all()
            if len(contratos) == 0:
                mensaje: dict = {
                    "mensaje_1212": "La empresa no tiene contratos"
                }
                respuesta = jsonify(mensaje)
                respuesta.status_code = 200
                return respuesta
            else:
                return [contrato_schema.dump(tr) for tr in contratos]
        else:
            mensaje: dict = {
                "mensaje": "El token enviado no corresponde al perfil del usuario"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta
            
