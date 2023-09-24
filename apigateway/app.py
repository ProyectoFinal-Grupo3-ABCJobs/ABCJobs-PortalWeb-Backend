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

class VistApiGateway(Resource):
    def get(self):
        ip_cliente = request.remote_addr
        print("ip_cliente: " + ip_cliente)
        #ip_cliente2 = request.headers.get('X-Forwarded-For')
        #print("ip_cliente2: " + str(ip_cliente2))
        
        authorization = request.headers['Authorization']
        authorization = authorization[len('Basic '):]
        usuario_contraseña = base64.b64decode(authorization).decode('utf-8')

        # Divide el usuario y la contraseña
        usuario, contraseña = usuario_contraseña.split(':')
        print("usuario" + str(usuario))
        params = {'usuario': usuario,
                'ip': ip_cliente}

        # Realiza la solicitud GET
        response = requests.post('http://localhost:5001/autorizador', params=params)
        print("response" + str(response))

        # Verifica si la solicitud fue exitosa (código de respuesta 200)
        if response.status_code == 200:
            # Imprime la respuesta JSON recibida
            data = response.json()
            print(data)
        else:
            print(f'Error en la solicitud: Código de respuesta {response.status_code}')

api.add_resource(VistApiGateway,'/apigateway')