from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
import hashlib, os, json, jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime

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
    )

empresa_schema = EmpresaSchema()
proyecto_schema = ProyectoSchema()
empleado_interno_schema = EmpleadoInternoSchema()
perfil_schema = PerfilSchema()
ficha_schema = FichaSchema()


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

                    print("###################: " + str(data.get("perfiles")))
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
        tokenPayload = get_jwt_identity()

        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            perfiles_proyecto = Perfil.query.filter(
                Perfil.idProyecto == id_proyecto
            ).all()

        #     if len(perfiles_proyecto) == 0:
        #         mensaje: dict = {
        #             "mensaje 1212": "El proyecto no tiene perfiles asociados"
        #         }
        #         respuesta = jsonify(mensaje)
        #         respuesta.status_code = 200
        #         return respuesta
        #     else:
        #         return [perfil_schema.dump(tr) for tr in perfiles_proyecto]
        # else:
        #     mensaje: dict = {
        #         "mensaje 1313": "El token enviado no corresponde al perfil del usuario"
        #     }
        #     respuesta = jsonify(mensaje)
        #     respuesta.status_code = 401
        #     return respuesta
