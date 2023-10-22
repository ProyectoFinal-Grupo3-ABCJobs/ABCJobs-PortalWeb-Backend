from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Empresa(db.Model):
    idEmpresa   = db.Column(db.Integer, primary_key = True)
    razonSocial = db.Column(db.String(100))
    nit         = db.Column(db.String(20))
    direccion   = db.Column(db.String(100))
    telefono    = db.Column(db.Integer)
    idCiudad    = db.Column(db.Integer)
    

class EmpresaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Empresa
        load_instance = True