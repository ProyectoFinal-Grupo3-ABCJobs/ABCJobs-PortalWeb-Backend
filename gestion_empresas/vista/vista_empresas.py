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
        FichaEmpleadoInternoSchema,
        FichaPerfil,
        FichaPerfilSchema,
        FichaCandidatoEmparejadoPerfil,
        FichaCandidatoEmparejadoPerfilSchema
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
        FichaEmpleadoInternoSchema,
        FichaPerfil,
        FichaPerfilSchema,
        FichaCandidatoEmparejadoPerfil
    )

empresa_schema = EmpresaSchema()
proyecto_schema = ProyectoSchema()
empleado_interno_schema = EmpleadoInternoSchema()
perfil_schema = PerfilSchema()
ficha_schema = FichaSchema()
ficha_candidato_emparejado_perfil_schema = FichaCandidatoEmparejadoPerfilSchema()

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
                "idEmpresa": usuario_empresa.idEmpresa
            }
           respuesta = jsonify(mensaje)
           respuesta.status_code = 200
           return respuesta
        else:
           mensaje: dict = {
                "Mensaje 201": "El usuario no tiene empresa asignada",
                "idEmpresa": 'Sin Empresa'
            }
           respuesta = jsonify(mensaje)
           respuesta.status_code = 200
           return respuesta


class VistaCreacionProyecto(Resource):
    @jwt_required()
    def post(self, id_empresa):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            print("La empresa tiene proyectos")
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

            fecha_str = proyecto_creado.fechaInicio.strftime('%Y-%m-%d') if proyecto_creado.fechaInicio else None

            return {
                "id": proyecto_creado.idProyecto,
                "nombreProyecto": proyecto_creado.nombreProyecto,
                "fechaInicio": fecha_str
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
                return "La empresa no tiene proyectos creados", 404
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

class VistaCreacionPerfil(Resource):
    @jwt_required()
    def post(self, id_proyecto):
        tokenPayload = get_jwt_identity()
        print("######1")
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            proyecto = Proyecto.query.filter(Proyecto.idProyecto == id_proyecto).first()
            if proyecto is None:
                print("######2")
                return "El proyecto no existe", 404
            else:
                print("######3")
                data = request.get_json()
                print("DATA: " + str(data))
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
                            idFicha=ficha.idFicha, idPerfil=perfil["idPerfil"], nombre=perfil["nombre"], descripcion=perfil["descripcion"]
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
            print("La empresa tiene empleados")
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
        
class VistaMotorEmparejamiento(Resource):
    @jwt_required()
    def post(self):
        print("El token es: ")
        tokenPayload = get_jwt_identity()
        clave_perfiles = 'perfiles'
        clave_ficha = 'idFicha'
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            encabezado_autorizacion = request.headers.get('Authorization')
            
            datos_json = request.get_json()

            encabezados_con_autorizacion = {
                    'Content-Type': 'application/json',
                    'Authorization': encabezado_autorizacion
                    
                    }
            url_candidatos = os.getenv('MS_CANDIDATO')
            
            if clave_perfiles in datos_json and clave_ficha in datos_json:

                if (len(datos_json[clave_perfiles])==0):
                    mensaje: dict = {
                    "Mensaje 200": "La peticion no tiene perfiles para emparejar"
                    }
                    respuesta = jsonify(mensaje)
                    respuesta.status_code = 200
                    return respuesta
                else:

                   
                    #jsonCandidatos = requests.get(f'{url_candidatos}getAll', headers=encabezados_con_autorizacion)
                    jsonCandidatos = requests.get('http://loadbalancerproyectoabc-735612126.us-east-2.elb.amazonaws.com:5001/candidate/getAll', headers=encabezados_con_autorizacion)
                    
                    if(jsonCandidatos.status_code != 200):

                        mensaje: dict = {
                            "Mensaje 401": "El servicio de Candidato en el recurso getAll no esta respondiento"
                        }
                        respuesta = jsonify(mensaje)
                        respuesta.status_code = 401
                        return respuesta

                    if(len(jsonCandidatos.json())==0):
                        mensaje: dict = {
                            "Mensaje 200": "No hay candidatos en la respuesta"
                        }
                        respuesta = jsonify(mensaje)
                        respuesta.status_code = 200
                        return respuesta
                    else:

                        lista_candidatos = jsonCandidatos.json()

                        for candidato in lista_candidatos:
                            listaPalabrasClaves = candidato['palabrasClave'].split(',')

                            # Logica para recorrer la lista de perfiles
                            for perfil in datos_json[clave_perfiles]:

                                porcentajeEmparejamiento = self.motorEmparejamiento(perfil['Descripcion'], listaPalabrasClaves)

                                if porcentajeEmparejamiento > 10:
                                
                                    candidato_perfil_ficha = FichaCandidatoEmparejadoPerfil.query.filter(
                                        FichaCandidatoEmparejadoPerfil.idFicha == datos_json[clave_ficha], FichaCandidatoEmparejadoPerfil.idCandidato == candidato['idCandidato'], FichaCandidatoEmparejadoPerfil.idPerfil == perfil['idPerfil']).all()

                                    # Valida si el persil no exite en la tabla 
                                    if len(candidato_perfil_ficha)==0:

                                        nuevo_candidato_emparejado = FichaCandidatoEmparejadoPerfil(
                                            idFicha=datos_json[clave_ficha],
                                            idCandidato=candidato['idCandidato'],
                                            idPerfil=perfil['idPerfil'],
                                            scoreEmparejamiento=porcentajeEmparejamiento,
                                            )

                                        db.session.add(nuevo_candidato_emparejado)
                                        db.session.commit()

                    
                    # consulto en BD los candidatos emparejados en la ficha_
                    candidato_perfil_ficha = FichaCandidatoEmparejadoPerfil.query.filter(
                                        FichaCandidatoEmparejadoPerfil.idFicha == datos_json[clave_ficha]).all()

                    # NOTA: Se crea EndPoint para el emparejamiento del candidato
                    listaCandidatos=[]
                    for cand_emparejado in candidato_perfil_ficha:
                        resCandidato = requests.get(f'http://loadbalancerproyectoabc-735612126.us-east-2.elb.amazonaws.com:5001/candidate/{cand_emparejado.idCandidato}', headers=encabezados_con_autorizacion)
                        
                        jsonCandidato = resCandidato.json()
                        jsonCandidato['idPerfil'] = cand_emparejado.idPerfil

                        listaCandidatos.append(jsonCandidato)

                    mensaje: dict = {
                                        "idFicha": datos_json[clave_ficha],
                                        "listadoCandidatos": listaCandidatos
                                    }
                    respuesta = jsonify(mensaje)
                    respuesta.status_code = 200
                    return respuesta                       

          
            else:
                mensaje: dict = {
                "Mensaje 401": "La peticion JSON no tiene Idperfiles o idficha o ambos"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta
            
        else:
            mensaje: dict = {
                "Mensaje 401": "El token enviado no corresponde al perfil del usuario"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta
        

    def motorEmparejamiento(self, perfil, listaPalabras):

        # Cargar el modelo de lenguaje pre-entrenado
        nlp = spacy.load("es_core_news_md")

        # Texto en el que deseas buscar la concordancia
        texto = perfil

        # Lista de palabras para las que deseas calcular la concordancia
        lista_palabras = listaPalabras

        # Procesar el texto con spaCy
        doc = nlp(texto)

        # Calcular los vectores de las palabras en el texto
        vectores_texto = [token.vector for token in doc if token.is_alpha]


        # Calcular los vectores de las palabras en la lista
        vectores_lista = [nlp(palabra).vector for palabra in lista_palabras]

        # Calcular las similitudes de coseno entre los vectores de las palabras en la lista y el texto
        similitudes = cosine_similarity(vectores_lista, vectores_texto)


        # Calcular el promedio de las similitudes
        porcentaje_concordancia = np.mean(similitudes) * 100


        return round(porcentaje_concordancia, 2)
