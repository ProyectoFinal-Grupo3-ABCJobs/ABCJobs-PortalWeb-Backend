from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Date

db = SQLAlchemy()

class Empresa(db.Model):
    idEmpresa   = db.Column(db.Integer, primary_key = True)
    razonSocial = db.Column(db.String(100))
    nit         = db.Column(db.String(20))
    direccion   = db.Column(db.String(100))
    telefono    = db.Column(db.String(20))
    idCiudad    = db.Column(db.Integer)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True, nullable=True)
    usuario = db.relationship('Usuario', back_populates='empresa', uselist=False)
    

class Proyecto(db.Model):
    idProyecto          = db.Column(db.Integer, primary_key = True)
    nombreProyecto      = db.Column(db.String(100))
    numeroColaboradores = db.Column(db.String(20))
    fechaInicio         = db.Column(Date)
    empresa_id          = db.Column(db.Integer, db.ForeignKey("empresa.idEmpresa"), nullable=False)

class Usuario(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    usuario     = db.Column(db.String(50))
    contrasena  = db.Column(db.String(90))
    tipoUsuario = db.Column(db.String(100))
    empresa = db.relationship('Empresa', back_populates='usuario', uselist=False)

    

# Establecer la relación uno a uno entre Usuario y Empresa
Usuario.empresa = db.relationship('Empresa', back_populates='usuario', uselist=False)
Empresa.usuario = db.relationship('Usuario', back_populates='empresa')


class EmpresaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Empresa
        load_instance = True

class ProyectoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Proyecto
        load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True