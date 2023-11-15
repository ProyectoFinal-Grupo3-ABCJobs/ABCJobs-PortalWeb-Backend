from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Date

db = SQLAlchemy()

class Prueba(db.Model):
    idPrueba    = db.Column(db.Integer, primary_key=True)
    tipoPrueba  = db.Column(db.String(50))
    fechaPrueba = db.Column(db.DateTime)
    resultado   = db.Column(db.String(50))
    observaciones = db.Column(db.String(2000))
    estado      = db.Column(db.Boolean)
    idCandidato = db.Column(db.Integer)
    idEmpresa   = db.Column(db.Integer)
    idProyecto  = db.Column(db.Integer)
    aprobado    = db.Column(db.Boolean, default=False)


class Entrevista(db.Model):
    idEntrevista    = db.Column(db.Integer, primary_key=True)
    fechaEntrevista = db.Column(db.DateTime)
    cargoDesc       = db.Column(db.String(100))
    idCargo         = db.Column(db.Integer)
    detalles        = db.Column(db.String(2000))
    estado          = db.Column(db.Boolean, default=False)
    candidatoNombre = db.Column(db.String(100))
    idCandidato     = db.Column(db.Integer)
    empresaNombre   = db.Column(db.String(100))
    idEmpresa       = db.Column(db.Integer)
    proyectoNombre  = db.Column(db.String(100))
    idProyecto      = db.Column(db.Integer)
    aprobado        = db.Column(db.Boolean, default=False)


class PruebaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Prueba
        load_instance = True

class EntrevistaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Entrevista
        load_instance = True
