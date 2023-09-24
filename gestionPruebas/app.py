from gestionPruebas import create_app
from flask_restful import Resource,Api
from flask import request
from flask import jsonify
from .modelos import db, ResultadoPrueba, ResultadoPruebaSchema
   
resultado_prueba_schema = ResultadoPruebaSchema()

app = create_app('default')

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Uniandes123@proyecto1bd.c9mkfgyc1tlh.us-east-1.rds.amazonaws.com:5432/postgres'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../monitoreoABC.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)

class VistaGestionPruebas(Resource):
    def get(self):
        resultadoPrueba = ResultadoPrueba.query.filter(ResultadoPrueba.idUsuario == request.args.get('idUsuario')).first()
        db.session.commit()

        print(resultadoPrueba)
        if resultadoPrueba:
            # Crea una instancia del esquema y serializa el objeto
            resultado_schema = ResultadoPruebaSchema()
            resultado_json = resultado_schema.dump(resultadoPrueba)
            return jsonify(resultado_json)
        else:
            # Si no se encontró ningún resultado, puedes devolver un mensaje de error o un JSON vacío
            return "NO se encontró ninguna prueba", 204

api.add_resource(VistaGestionPruebas,'/pruebas')