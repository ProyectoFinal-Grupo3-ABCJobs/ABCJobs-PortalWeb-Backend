from autorizador import create_app
from flask_restful import Resource, Api
from flask import request
import threading

from datetime import date, datetime
from .modelos import db, LogAutorizador, LogAutorizadorSchema, IpBloqueada, IpBloqueadaSchema

log_autorizador_schema = LogAutorizadorSchema()

app = create_app('default')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Uniandes123@proyecto1bd.c9mkfgyc1tlh.us-east-1.rds.amazonaws.com:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)


class VistAutorizadorDisponibilidad(Resource):
    semaphore = threading.Semaphore(1)

    def post(self):
        with self.semaphore:
            fecha_actual = str(datetime.now().strftime("%Y%m%d"))
            hora_actual = int(str(datetime.now().strftime("%H%M")))
            ipBloqueada = IpBloqueada.query.filter(
                IpBloqueada.ip == request.json["ip"]).with_for_update().first()
            print(ipBloqueada)
            if ipBloqueada:
                return "IP bloqueada", 401
            
            print("USUARIO:" + request.json["usuario"])
            logAutorizadorIP = LogAutorizador.query.filter(
                LogAutorizador.ip == request.json["ip"], LogAutorizador.fecha == fecha_actual, LogAutorizador.hora == hora_actual).with_for_update().first()

            if logAutorizadorIP:
                print("IP registrada")
                if logAutorizadorIP.fecha == fecha_actual:
                    if logAutorizadorIP.hora == hora_actual:
                        if logAutorizadorIP.intentos == 20:
                            ipBloqueada = IpBloqueada(
                                ip=request.json["ip"])
                            db.session.add(ipBloqueada)
                        else:
                            logAutorizadorIP.intentos = logAutorizadorIP.intentos + 1
                    else:
                        logAutorizadorIP.hora = hora_actual
                        logAutorizadorIP.intentos = 0
                else:
                    logAutorizadorIP.fecha = fecha_actual
                    logAutorizadorIP.hora = hora_actual
                    logAutorizadorIP.intentos = 0
                db.session.commit()
                return "IP autorizada", 200
            else:
                print("IP NO registrada")
                logAutorizadorIP = LogAutorizador(
                    ip=request.json["ip"],
                    usuario=None,
                    fecha=fecha_actual,
                    hora=hora_actual,
                    intentos=1, 
                    experimento=2)
                db.session.add(logAutorizadorIP)
            db.session.commit()
            return "IP autorizada", 200
class VistAutorizadorConfidencialidad(Resource):
    semaphore = threading.Semaphore(1)

    def post(self):
        with self.semaphore:
            fecha_actual = str(datetime.now().strftime("%Y%m%d"))
            hora_actual = int(str(datetime.now().strftime("%H%M")))
            ipBloqueada = IpBloqueada.query.filter(
                IpBloqueada.ip == request.json["ip"]).with_for_update().first()
            print(ipBloqueada)
            if ipBloqueada:
                return "IP bloqueada", 401
            
            print("USUARIO:" + request.json["usuario"])
            logAutorizadorUsuario = LogAutorizador.query.filter(
                LogAutorizador.usuario == request.json["usuario"], LogAutorizador.fecha == fecha_actual, LogAutorizador.hora == hora_actual).with_for_update().first()
        
            if logAutorizadorUsuario:
                print("Usuario registrado")
                if logAutorizadorUsuario.fecha == fecha_actual:
                    if logAutorizadorUsuario.hora == hora_actual:
                        if logAutorizadorUsuario.intentos > 2:
                            return "ALERTA Detección ataque fuerza bruta", 401
                        else:
                            logAutorizadorUsuario.intentos = logAutorizadorUsuario.intentos + 1
                    else:
                        logAutorizadorUsuario.hora = hora_actual
                        logAutorizadorUsuario.intentos = 0
                else:
                    logAutorizadorUsuario.fecha = fecha_actual
                    logAutorizadorUsuario.hora = hora_actual
                    logAutorizadorUsuario.intentos = 0
                db.session.commit()
                return "Usuario autorizado", 200
            else:
                print("Usuario NO registrado")
                logAutorizadorUsuario = LogAutorizador(
                    ip=None,
                    usuario=request.json["usuario"],
                    fecha=fecha_actual,
                    hora=hora_actual,
                    intentos=1,
                    experimento=1)
                db.session.add(logAutorizadorUsuario)
            db.session.commit()
            return "Usuario autorizado", 200


api.add_resource(VistAutorizadorDisponibilidad, '/autorizadorDisponibilidad')
api.add_resource(VistAutorizadorConfidencialidad, '/autorizadorConfidencialidad')
