from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from flask import jsonify
import hashlib, os, json


directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)

if carpeta_actual=='gestion_autenticacion' or carpeta_actual=='app':
     from modelo import Usuarios, UsuariosSchema
else:
     from gestion_autenticacion.modelo import Usuarios, UsuariosSchema



user_schema = UsuariosSchema()


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
          print("El has es: ", hashpwd)
          usuario = Usuarios.query.filter(Usuarios.usuario == request.json['usuario'], Usuarios.contrasena == hashpwd).first()

          if usuario is None:
               mensaje:dict = {'error 5050':"El usuario no pudo ser autenticado"}
               respuesta = jsonify(mensaje)
               respuesta.status_code = 400
               return respuesta

          token_de_acceso = create_access_token(identity=request.json["usuario"])
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
