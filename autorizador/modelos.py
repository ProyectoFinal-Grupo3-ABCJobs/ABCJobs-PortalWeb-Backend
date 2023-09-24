from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Index

db = SQLAlchemy()

class LogAutorizador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50))
    usuario = db.Column(db.String(50))
    fecha = db.Column(db.String(8))
    hora = db.Column(db.Integer())
    intentos = db.Column(db.Integer())
    experimento = db.Column(db.Integer())
    
    __table_args__ = (
        Index('idx_ip_fecha_hora', 'ip', 'fecha', 'hora'),
    )

class LogAutorizadorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LogAutorizador
        load_instance = True
        
class IpBloqueada(db.Model):
    ip = db.Column(db.String(50), primary_key=True)

class IpBloqueadaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = IpBloqueada
        load_instance = True
