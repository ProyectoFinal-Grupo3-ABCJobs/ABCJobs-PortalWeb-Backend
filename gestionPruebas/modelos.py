from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class ResultadoPrueba(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer)
    resultado = db.Column(db.Integer)

class ResultadoPruebaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ResultadoPrueba
        load_instance = True