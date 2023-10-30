from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

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

class CandidatoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Candidato
        load_instance = True