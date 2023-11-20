from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Date

db = SQLAlchemy()

class Empresa(db.Model):
    idEmpresa = db.Column(db.Integer, primary_key=True)
    razonSocial = db.Column(db.String(100))
    nit         = db.Column(db.String(20))
    direccion   = db.Column(db.String(100))
    telefono    = db.Column(db.String(20))
    idCiudad    = db.Column(db.Integer)
    idUsuario = db.Column(db.Integer)

class Proyecto(db.Model):
    idProyecto = db.Column(db.Integer, primary_key=True)
    nombreProyecto = db.Column(db.String(100))
    numeroColaboradores = db.Column(db.String(20))
    fechaInicio = db.Column(Date)
    empresa_id = db.Column(db.Integer)

class EmpleadoInterno(db.Model):
    idEmpleado = db.Column(db.Integer, primary_key=True)
    tipoIdentificacion = db.Column(db.String(100))
    identificacion = db.Column(db.String(20))
    nombre = db.Column(db.String(100))
    cargo = db.Column(db.String(100))
    idEmpresa = db.Column(db.Integer)

class Perfil(db.Model):
    idPerfil = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(200))
    idProyecto = db.Column(db.Integer)

class Ficha(db.Model):
    idFicha = db.Column(db.Integer, primary_key=True)
    idProyecto = db.Column(db.Integer)
    estadoEmparejamiento = db.Column(db.Boolean, default=False)
    
class FichaEmpleadoInterno(db.Model):
    idFicha = db.Column(db.Integer, db.ForeignKey('ficha.idFicha'), primary_key=True)
    idEmpleado = db.Column(db.Integer, db.ForeignKey('empleado_interno.idEmpleado'), primary_key=True)

    
class FichaPerfil(db.Model):
    idFicha = db.Column(db.Integer, primary_key=True)
    idPerfil = db.Column(db.Integer, primary_key=True)

class FichaCandidatoEmparejadoPerfil(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    idFicha = db.Column(db.Integer)
    idProyecto = db.Column(db.Integer)
    nombreProyecto = db.Column(db.String(100))
    idEmpresa = db.Column(db.Integer)
    nombreEmpresa = db.Column(db.String(100))
    idCandidato = db.Column(db.Integer)
    nombreCandidato = db.Column(db.String(100))
    idPerfil = db.Column(db.Integer)
    descripcionPerfil = db.Column(db.String(100))
    estado = db.Column(db.Boolean, default=False)


class Contrato(db.Model):
    idContrato = db.Column(db.Integer, primary_key=True)
    numeroContrato = db.Column(db.Integer)
    idCandidato = db.Column(db.Integer)
    idEmpresa = db.Column(db.Integer)
    idProyecto = db.Column(db.Integer)
    idCargo = db.Column(db.Integer)


class DesempenoEmpleado(db.Model):
    idDesempeno = db.Column(db.Integer, primary_key=True)
    idEmpleado = db.Column(db.Integer)
    calificacion = db.Column(db.String(100))
    aspectosResaltar = db.Column(db.String(2000)) 
    aspectosMejorar = db.Column(db.String(2000))


class DesempenoEmpleadoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DesempenoEmpleado
        load_instance = True

class ContratoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Contrato
        load_instance = True


class EmpresaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Empresa
        load_instance = True

class ProyectoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Proyecto
        load_instance = True
        
class EmpleadoInternoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EmpleadoInterno
        load_instance = True
        
class PerfilSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Perfil
        load_instance = True

class FichaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ficha
        load_instance = True
        
class FichaEmpleadoInternoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FichaEmpleadoInterno
        load_instance = True
        
class FichaPerfilSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FichaPerfil
        load_instance = True


class FichaCandidatoEmparejadoPerfilSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FichaCandidatoEmparejadoPerfil
        load_instance = True