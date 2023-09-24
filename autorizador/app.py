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


class VistAutorizador(Resource):
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
            logAutorizador = LogAutorizador.query.filter(
                LogAutorizador.ip == request.json["ip"], LogAutorizador.fecha == fecha_actual, LogAutorizador.hora == hora_actual).with_for_update().first()

            if logAutorizador:
                print("Usuario registrado")
                if logAutorizador.fecha == fecha_actual:
                    if logAutorizador.hora == hora_actual:
                        if logAutorizador.intentos == 100:
                            ipBloqueada = IpBloqueada(
                                ip=request.json["ip"])
                            db.session.add(ipBloqueada)
                        else:
                            logAutorizador.intentos = logAutorizador.intentos + 1
                    else:
                        logAutorizador.hora = hora_actual
                        logAutorizador.intentos = 0
                else:
                    logAutorizador.fecha = fecha_actual
                    logAutorizador.hora = hora_actual
                    logAutorizador.intentos = 0
                db.session.commit()
                return "IP autorizada", 200
            else:
                print("Usuario NO registrado")
                logAutorizador = LogAutorizador(
                    ip=request.json["ip"],
                    usuario=request.json["usuario"],
                    fecha=fecha_actual,
                    hora=hora_actual,
                    intentos=1)
                db.session.add(logAutorizador)
            db.session.commit()
            return "IP autorizada", 201


api.add_resource(VistAutorizador, '/autorizador')
