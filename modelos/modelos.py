from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class LogAutorizador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50))
    usuario = db.Column(db.String(50))
    fecha = db.Column(db.String(8))
    hora = db.Column(db.Integer())
    intentos = db.Column(db.Integer())
    bloqueado = db.Column(db.Boolean, default=False)

class LogAutorizadorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LogAutorizador
        load_instance = True
