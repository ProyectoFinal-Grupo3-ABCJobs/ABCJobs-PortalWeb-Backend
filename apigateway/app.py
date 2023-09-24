from apigateway import create_app
from flask_restful import Resource, Api
from flask import Flask, request
import requests
import base64

app = create_app('default')

app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()
api = Api(app)

class VistApiGatewayDisponibilidad(Resource):
    def get(self):
        ip_cliente = request.remote_addr
        print("ip_cliente: " + ip_cliente)
        
        authorization = request.headers['Authorization']
        authorization = authorization[len('Basic '):]
        usuario_contraseña = base64.b64decode(authorization).decode('utf-8')

        # Divide el usuario y la contraseña
        usuario, contraseña = usuario_contraseña.split(':')
        print("usuario" + str(usuario))
        params = {"usuario": usuario,
                "ip": ip_cliente}
        print("params" + str(params))

        # Realiza la solicitud GET
        response = requests.post('http://localhost:5001/autorizadorDisponibilidad', json=params)
        print("response AUTORIZADOR: " + str(response))

        # Verifica si la solicitud fue exitosa (código de respuesta 200)
        if response.status_code == 200:
            # Imprime la respuesta JSON recibida
            data = response.json()
            print(data)
            
            autorizacion = request.headers['Authorization']            
            headers = {'Authorization': autorizacion}
            response_login = requests.get('http://localhost:5002/login', headers=headers)
            print("response LOGIN: " + str(response_login))
            return response_login.json()
        else:
            return "IP Bloqueada", 401
        
class VistApiGatewayConfidencialidad(Resource):
    def get(self):        
        ip_cliente = request.remote_addr
        print("ip_cliente: " + ip_cliente)
        
        authorization = request.headers['Authorization']
        authorization = authorization[len('Basic '):]
        usuario_contraseña = base64.b64decode(authorization).decode('utf-8')

        # Divide el usuario y la contraseña
        usuario, contraseña = usuario_contraseña.split(':')
        print("usuario" + str(usuario))
        params = {"usuario": usuario,
                "ip": ip_cliente}
        print("params" + str(params))

        # Realiza la solicitud GET
        response = requests.post('http://localhost:5001/autorizadorConfidencialidad', json=params)
        print("response AUTORIZADOR CONFIDENCIALIDAD: " + str(response))

        # Verifica si la solicitud fue exitosa (código de respuesta 200)
        if response.status_code == 200:
            # Imprime la respuesta JSON recibida
            data = response.json()
            print(data)
            
            autorizacion = request.headers['Authorization']            
            headers = {'Authorization': autorizacion}
            response_login = requests.get('http://localhost:5002/login', headers=headers)
            print("response LOGIN: " + str(response_login))
            
            if response.status_code == 200:
                data = response_login.json()
                id = data.get('id')
                response_pruebas = requests.get(f'http://localhost:5003/pruebas?idUsuario={id}')
                return response_pruebas.json()
            else:
                return "Usuario No autorizado", 401    
        else:
            return "ALERTA Detección ataque fuerza bruta", 401

api.add_resource(VistApiGatewayDisponibilidad,'/apigateway/login')
api.add_resource(VistApiGatewayConfidencialidad,'/apigateway/pruebas')