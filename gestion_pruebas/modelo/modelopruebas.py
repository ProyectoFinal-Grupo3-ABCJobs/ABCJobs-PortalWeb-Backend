from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Date

db = SQLAlchemy()

class Prueba(db.Model):
    idPrueba    = db.Column(db.Integer, primary_key=True)
    tipoPrueba  = db.Column(db.String(50))
    fechaPrueba = db.Column(db.Date)
    resultado   = db.Column(db.String(50))
    observaciones = db.Column(db.String(2000))
    estado      = db.Column(db.Boolean)
    idCandidato = db.Column(db.Integer)
    idEmpresa   = db.Column(db.Integer)


class PruebaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Prueba
        load_instance = True
