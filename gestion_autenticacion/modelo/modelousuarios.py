from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Usuarios(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    usuario     = db.Column(db.String(50))
    contrasena  = db.Column(db.String(90))
    tipoUsuario = db.Column(db.String(100))

class UsuariosSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuarios
        load_instance = True