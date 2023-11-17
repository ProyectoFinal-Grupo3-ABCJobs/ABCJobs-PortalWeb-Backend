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
    idUsuario = db.Column(db.Integer)
    # idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True, nullable=True)
    # usuario = db.relationship('Usuario', back_populates='empresa', uselist=False)
    

class Usuario(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    usuario     = db.Column(db.String(50))
    contrasena  = db.Column(db.String(90))
    tipoUsuario = db.Column(db.String(100))
    # empresa = db.relationship('Empresa', back_populates='usuario', uselist=False)
   

# Establecer la relación uno a uno entre Usuario y Empresa
# Usuario.empresa = db.relationship('Empresa', back_populates='usuario', uselist=False)
# Empresa.usuario = db.relationship('Usuario', back_populates='empresa')

class Candidato(db.Model):
    idCandidato         = db.Column(db.Integer, primary_key = True)
    tipoIdentificacion  = db.Column(db.String(50))
    identificacion      = db.Column(db.String(20))
    nombre              = db.Column(db.String(150))
    direccion           = db.Column(db.String(150))
    telefono            = db.Column(db.String(20))
    profesion           = db.Column(db.String(150))
    aniosExperiencia    = db.Column(db.String(150))
    idCiudad            = db.Column(db.String(100))
    idDepartamento      = db.Column(db.String(100))
    idPais              = db.Column(db.String(100))
    ultimoEstudio       = db.Column(db.String(150))
    institucion         = db.Column(db.String(150))
    anioGrado           = db.Column(db.Integer)
    idCiudadInst        = db.Column(db.String(100))
    idDepartamentoInst  = db.Column(db.String(100))
    cargoUltimoEmpleo   = db.Column(db.String(150))
    empresa             = db.Column(db.String(150))
    anioIngreso         = db.Column(db.Integer)
    anioRetiro          = db.Column(db.Integer)
    estado              = db.Column(db.Boolean, default=False)
    palabrasClave       = db.Column(db.String(300))
    idUsuario           = db.Column(db.Integer)

class CandidatoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Candidato
        load_instance = True

class EmpresaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Empresa
        load_instance = True


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True