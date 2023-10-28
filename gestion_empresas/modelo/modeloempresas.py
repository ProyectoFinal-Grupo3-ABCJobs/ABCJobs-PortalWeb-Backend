from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Date

db = SQLAlchemy()

class Empresa(db.Model):
    idEmpresa   = db.Column(db.Integer, primary_key = True)
    razonSocial = db.Column(db.String(100))
    nit         = db.Column(db.String(20))
    direccion   = db.Column(db.String(100))
    telefono    = db.Column(db.Integer)
    idCiudad    = db.Column(db.Integer)
    # proyectos   = db.relationship('Proyecto', cascade='all, delete, delete-orphan')   
    
class Proyecto(db.Model):
    idProyecto          = db.Column(db.Integer, primary_key = True)
    nombreProyecto      = db.Column(db.String(100))
    numeroColaboradores = db.Column(db.String(20))
    fechaInicio         = db.Column(Date)
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.idEmpresa"), nullable=False)


class EmpresaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Empresa
        load_instance = True

class ProyectoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Proyecto
        load_instance = True