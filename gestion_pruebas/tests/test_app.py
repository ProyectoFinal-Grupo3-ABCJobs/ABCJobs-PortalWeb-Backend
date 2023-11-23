import unittest, json
import os
import requests
import json
from faker import Faker

directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)

if carpeta_actual == "gestion_pruebas" or carpeta_actual == "app":
    from app import app
    from modelo import db
else:
    from gestion_pruebas.app import app
    from gestion_pruebas.modelo import db

fake = Faker()
class TestApp(unittest.TestCase):
    def setUp(self):
        
        url = "http://loadbalancerproyectoabc-735612126.us-east-2.elb.amazonaws.com:5000/users/auth"

        #url = "http://127.0.0.1:5000/users/auth"

        payload = json.dumps({"usuario": "candidato", "contrasena": "candidato"})
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)
        self.token = response.json()["token"]

        payloadCandidato = json.dumps(
            {"usuario": "candidato", "contrasena": "candidato"}
        )
        headers = {"Content-Type": "application/json"}

        responseCandidato = requests.request(
            "POST", url, headers=headers, data=payloadCandidato
        )
        self.tokenCandiato = responseCandidato.json()["token"]


        response = requests.request("POST", url, headers=headers, data=payload)
        self.token = response.json()["token"]

        payloadEmpresa = json.dumps(
            {"usuario": "empresa", "contrasena": "empresa"}
        )
        headers = {"Content-Type": "application/json"}

        responseEmpresa = requests.request(
            "POST", url, headers=headers, data=payloadEmpresa
        )
        self.tokenEmpresa = responseEmpresa.json()["token"]

        self.app = app.test_client()

    def tearDown(self):
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())

    def test_response_status_200(self):
        response = self.app.get("/test/ping")
        self.assertEqual(response.status_code, 200)

    def test_response_json(self):
        response = self.app.get("/test/ping")
        data: dict = {"mensaje": "healthcheck OK"}
        response_dict = json.loads(response.data)
        self.assertEqual(response_dict, data)


    def test_VistaConsultaPruebasCandidato_sin_pruebas(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }

        # Creo el proyecto, sin no funciona debo crear la empresa
        resultado_proyecto = self.app.get(
            '/test/candidate/123',
            headers=encabezados_con_autorizacion,
        )
        self.assertEqual(resultado_proyecto.status_code, 404)

    def test_VistaConsultaPruebasCandidato_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenEmpresa}",
        }

        # Creo el proyecto, sin no funciona debo crear la empresa
        resultado_proyecto = self.app.get(
            '/test/candidate/123',
            headers=encabezados_con_autorizacion,
        )
        self.assertEqual(resultado_proyecto.status_code, 401)

    def test_VistaConsultaEntrevistasCandidato_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenEmpresa}",
        }

        # Creo el proyecto, sin no funciona debo crear la empresa
        resultado_proyecto = self.app.get(
            '/test/candidate/123/interviews',
            headers=encabezados_con_autorizacion,
        )
        self.assertEqual(resultado_proyecto.status_code, 401)


    def test_VistaConsultaEntrevistasCandidato_sin_entrevistas(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }

        # Creo el proyecto, sin no funciona debo crear la empresa
        resultado_proyecto = self.app.get(
            '/test/candidate/123/interviews',
            headers=encabezados_con_autorizacion,
        )
        self.assertEqual(resultado_proyecto.status_code, 404)

    def test_VistaResultadoEntrevistasCandidatosPorIdEmpresa_sin_candidatos(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenEmpresa}",
        }

        # Creo el proyecto, sin no funciona debo crear la empresa
        resultado_proyecto = self.app.get(
            '/test/company/4/interviews',
            headers=encabezados_con_autorizacion,
        )
        self.assertEqual(resultado_proyecto.status_code, 200)


    def test_VistaAdicionarCandidatosEmparejadosAEntrevista_sin_candidatos(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenEmpresa}",
        }


        data = {
            "idProyecto" :str(fake.random_int(min=1, max=99)),
            "nombreProyecto": fake.name(),
            "nombreEmpresa": fake.name(),
            "idEmpresa": str(fake.random_int(min=1, max=99)),
            "idCandidato": str(fake.random_int(min=1, max=99)),
            "nombreCandidato":fake.name(), 
            "idPerfil": str(fake.random_int(min=1, max=99)), 
            "descripcionPerfil": fake.name(),

        }

        # Creo el proyecto, sin no funciona debo crear la empresa
        resultado_proyecto = self.app.post(
            '/test/interviews',
            json= data,
            headers=encabezados_con_autorizacion,
        )
        self.assertEqual(resultado_proyecto.status_code, 201)



    def test_VistaEliminarCandidatoTblEntrevistaPorIds_ok(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenEmpresa}",
        }


        data = {
            "idProyecto" :str(fake.random_int(min=1, max=99)),
            "nombreProyecto": fake.name(),
            "nombreEmpresa": fake.name(),
            "idEmpresa": str(fake.random_int(min=1, max=99)),
            "idCandidato": str(fake.random_int(min=1, max=99)),
            "nombreCandidato":fake.name(), 
            "idPerfil": str(fake.random_int(min=1, max=99)), 
            "descripcionPerfil": fake.name(),

        }

        # Creo el proyecto, sin no funciona debo crear la empresa
        resultado_proyecto = self.app.post(
            '/test/interviews',
            json= data,
            headers=encabezados_con_autorizacion,
        )

        resultado_eliminar = self.app.delete(
            f'/test/proyectos/{data["idProyecto"]}/candidatos/{data["idCandidato"]}/empresas/{data["idEmpresa"]}',
            json= data,
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(resultado_eliminar.status_code, 204)


if __name__ == "__main__":
    unittest.main()
