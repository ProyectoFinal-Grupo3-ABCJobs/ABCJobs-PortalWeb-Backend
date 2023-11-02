from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
import hashlib, os, json, jwt
from jwt.exceptions import InvalidTokenError

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

            nuevo_proyecto = Proyecto(
                nombreProyecto=request.json["nombreProyecto"],
                fechaInicio=request.json["fechaInicio"],
                empresa_id=id_empresa,
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
            mensaje: dict = {
                "mensaje": "El token enviado no corresponde al perfil del usuario"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta


class VistaConsultaEmpladoInterno(Resource):
    @jwt_required()
    def get(self, id_empresa):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            empleados_empresa = EmpleadoInterno.query.filter(
                EmpleadoInterno.idEmpresa == id_empresa
            ).all()

            if len(empleados_empresa) == 0:
                mensaje: dict = {
                    "mensaje 1212": "La empresa no tiene proyectos creados"
                }
                respuesta = jsonify(mensaje)
                respuesta.status_code = 200
                return respuesta
            else:
                return [empleado_interno_schema.dump(tr) for tr in empleados_empresa]
        else:
            mensaje: dict = {
                "mensaje 1313": "El token enviado no corresponde al perfil del usuario"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta


class VistaConsultaPerfil(Resource):
    @jwt_required()
    def get(self, id_proyecto):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            perfiles_proyecto = Perfil.query.filter(
                Perfil.idProyecto == id_proyecto
            ).all()

            if len(perfiles_proyecto) == 0:
                mensaje: dict = {
                    "mensaje 1212": "El proyecto no tiene perfiles asociados"
                }
                respuesta = jsonify(mensaje)
                respuesta.status_code = 200
                return respuesta
            else:
                return [perfil_schema.dump(tr) for tr in perfiles_proyecto]
        else:
            mensaje: dict = {
                "mensaje 1313": "El token enviado no corresponde al perfil del usuario"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta


class VistaCrearFicha(Resource):
    @jwt_required()
    def post(self, id_proyecto):
        tokenPayload = get_jwt_identity()
        if tokenPayload["tipoUsuario"].upper() == "EMPRESA":
            proyecto = Proyecto.query.filter(Proyecto.idProyecto == id_proyecto).first()
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
            mensaje: dict = {
                "mensaje 1313": "El token enviado no corresponde al perfil del usuario"
            }
            respuesta = jsonify(mensaje)
            respuesta.status_code = 401
            return respuesta
