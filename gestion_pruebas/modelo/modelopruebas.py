from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Date
from datetime import datetime, timedelta

db = SQLAlchemy()

class Prueba(db.Model):
    idPrueba    = db.Column(db.Integer, primary_key=True)
    tipoPrueba  = db.Column(db.String(50))
    fechaPrueba = db.Column(db.DateTime)
    resultado   = db.Column(db.String(50))
    observaciones = db.Column(db.String(2000))
    idEmpresa       = db.Column(db.Integer)
    empresaNombre   = db.Column(db.String(100))
    idCandidato     = db.Column(db.Integer)
    candidatoNombre = db.Column(db.String(100))
    idProyecto      = db.Column(db.Integer)
    proyectoNombre  = db.Column(db.String(100))
    idPerfil         = db.Column(db.Integer)
    perfilDescripcion = db.Column(db.String(100))
    aprobado    = db.Column(db.Boolean, default=False)
    estado      = db.Column(db.Boolean)

def two_days_from_now_at_8_am():
    return (datetime.now() + timedelta(days=2)).replace(hour=8, minute=0, second=0, microsecond=0)

class Entrevista(db.Model):
    idEntrevista    = db.Column(db.Integer, primary_key=True)
    fechaEntrevista = db.Column(db.DateTime, default=two_days_from_now_at_8_am)
    idEmpresa       = db.Column(db.Integer)
    empresaNombre   = db.Column(db.String(100))
    idCandidato     = db.Column(db.Integer)
    candidatoNombre = db.Column(db.String(100))
    idProyecto      = db.Column(db.Integer)
    proyectoNombre  = db.Column(db.String(100))
    idPerfil         = db.Column(db.Integer)
    perfilDescripcion = db.Column(db.String(100))
    detalles        = db.Column(db.String(2000), default="El candidato ha demostrado ser apto para el trabajo en equipo y tiene un buen manejo de las herramientas de desarrollo.")
    estado          = db.Column(db.Boolean, default=False)
    aprobado        = db.Column(db.Boolean, default=False)


class PruebaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Prueba
        load_instance = True

class EntrevistaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Entrevista
        load_instance = True
