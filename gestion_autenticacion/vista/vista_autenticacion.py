from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token,get_jwt_identity
from flask import jsonify
import hashlib, os, json


directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)

if carpeta_actual=='gestion_autenticacion' or carpeta_actual=='app':
     from modelo import Usuario, UsuarioSchema, db, Empresa, EmpresaSchema
else:
     from gestion_autenticacion.modelo import Usuario, UsuarioSchema, db, Empresa,EmpresaSchema

user_schema = UsuarioSchema()
empresa_schema = EmpresaSchema()


class VistaGenerarToken(Resource):
    def post(self):
          
          if not request.data:
               mensaje:dict = {'error 1010':"Solicitud sin datos"}
               respuesta = jsonify(mensaje)
               respuesta.status_code = 400
               return respuesta

          try:
               datos_request= request.data
               request_json = datos_request.decode('utf-8')
               request_json = json.loads(request_json)

          except (ValueError, UnicodeDecodeError):
               mensaje:dict = {'error 2020':"La solicitud no contien un JSON válido"}
               respuesta = jsonify(mensaje)
               respuesta.status_code = 400
               return respuesta


          if 'usuario' not in request_json or 'contrasena' not in request_json:
               mensaje:dict = {'error 3030':"Faltan datos en la petición"}
               respuesta = jsonify(mensaje)
               respuesta.status_code = 400
               return respuesta
  
          if len(request_json['usuario'].strip())==0 or len(request_json['contrasena'].strip())==0:
               mensaje:dict = {'error 4040':"Falta informacion en la petición"}
               respuesta = jsonify(mensaje)
               respuesta.status_code = 400
               return respuesta

          # Cifrar la contraseña Salt
          saltedword = os.getenv("SALTEDWORD")
          pwdhasehd = request.json['contrasena'] + saltedword
          hashpwd = hashlib.sha256(pwdhasehd.encode()).hexdigest()
          usuario = Usuario.query.filter(Usuario.usuario == request.json['usuario'], Usuario.contrasena == hashpwd).first()
          
          if usuario is None:
               mensaje:dict = {'error 5050':"El usuario no pudo ser autenticado"}
               respuesta = jsonify(mensaje)
               respuesta.status_code = 400
               return respuesta

          empresa = Empresa.query.filter(Empresa.idUsuario == usuario.id).first()

          
          if empresa is None:
               idEmpCanFunc:str='';
          else:
               idEmpCanFunc = empresa.idEmpresa

          
          data = {
               'idUsuario': usuario.id,
               'usuario':usuario.usuario,
               'tipoUsuario': usuario.usuario.upper(),
               'idEmpCanFunc':idEmpCanFunc
          }

          #token_de_acceso_temp = create_access_token(identity=dataTemp)
          token_de_acceso = create_access_token(identity=data)

          # Genero Token de acceso
          usuario.token = token_de_acceso

          # Usuario autenticado
          mensaje:dict = {"id": usuario.id, "tipoUsuario": usuario.tipoUsuario,"token": token_de_acceso}
          respuesta = jsonify(mensaje)
          respuesta.status_code = 200
          return respuesta

class VistaSaludServicio(Resource):
    def get(self):
          mensaje:dict = {'mensaje':"healthcheck OK"}
          respuesta = jsonify(mensaje)
          respuesta.status_code = 200
          return respuesta
    
class VistaRegistroUsuario(Resource):
    def post(self):
          try:
                if len(request.json["usuario"].strip())==0 or len(request.json["contrasena"].strip())==0 or len(request.json["tipoUsuario"].strip())==0 :
                    return "Code 400: Hay campos obligatorios vacíos", 400
          except:
                return "Code 400: Hay campos obligatorios vacíos", 400
          
          usuario = Usuario.query.filter(
            Usuario.usuario == request.json["usuario"]).first()          
          if not usuario is None:
            return "No se puede crear el usuario. El correo ya se encuentra registrado", 409
     
          nuevo_usuario = Usuario(
               usuario=request.json["usuario"],
               contrasena=request.json["contrasena"],
               tipoUsuario=request.json["tipoUsuario"]
          )

          db.session.add(nuevo_usuario)
          db.session.commit()

          usuario_creado = Usuario.query.filter(
               Usuario.usuario == request.json["usuario"]
          ).first()

          return {
               "id": usuario_creado.id,
               "usuario": usuario_creado.usuario,
               "contrasena": usuario_creado.contrasena,
               "tipoUsuario": usuario_creado.tipoUsuario,
          }, 201