import unittest, json
import os

directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)

if carpeta_actual=='gestion_empresas' or carpeta_actual=='app':
    from app import app
    from modelo import db
else:
    from gestion_empresas.app import app
    from gestion_empresas.modelo import db

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
    
    def test_response_status_200(self):
        response = self.app.get('/company/ping')
        self.assertEqual(response.status_code, 200)


    def test_response_json(self):
        response = self.app.get('/company/ping')
        data:dict = {
            "mensaje": "healthcheck OK"
            }
        response_dict = json.loads(response.data)
        self.assertEqual(response_dict, data)

    def test_create_company(self):

        nueva_empresa = {
            "razonSocial":"EmpresaPrueba",
            "nit": "455889899",
            "direccion": "calle 20",
            "telefono": "89965656565",
            "idCiudad": "12"
        }

        solicitud_nueva_empresa = self.app.post("/company/register",
                                                     data=json.dumps(
                                                         nueva_empresa),
                                                     headers={'Content-Type': 'application/json'})

        self.assertEqual(solicitud_nueva_empresa.status_code, 201)

    def test_create_company_name_exists(self):

        nueva_empresa = {
            "razonSocial":"EmpresaPrueba",
            "nit": "4558898558",
            "direccion": "calle 20",
            "telefono": "89965656565",
            "idCiudad": "12"
        }

        solicitud_nueva_empresa = self.app.post("/company/register",
                                                     data=json.dumps(
                                                         nueva_empresa),
                                                     headers={'Content-Type': 'application/json'})

        nueva_empresa = {
            "razonSocial":"EmpresaPrueba",
            "nit": "455888558",
            "direccion": "calle 20",
            "telefono": "89965656565",
            "idCiudad": "12"
        }

        solicitud_nueva_empresa = self.app.post("/company/register",
                                                     data=json.dumps(
                                                         nueva_empresa),
                                                     headers={'Content-Type': 'application/json'})

        self.assertEqual(solicitud_nueva_empresa.status_code, 409)

    def test_create_company_nit_exists(self):

        nueva_empresa = {
            "razonSocial":"EmpresaPrueba1",
            "nit": "455889855878",
            "direccion": "calle 20",
            "telefono": "89965656565",
            "idCiudad": "12"
        }

        solicitud_nueva_empresa = self.app.post("/company/register",
                                                     data=json.dumps(
                                                         nueva_empresa),
                                                     headers={'Content-Type': 'application/json'})

        nueva_empresa = {
            "razonSocial":"EmpresaPrueba2",
            "nit": "455889855878",
            "direccion": "calle 20",
            "telefono": "89965656565",
            "idCiudad": "12"
        }

        solicitud_nueva_empresa = self.app.post("/company/register",
                                                     data=json.dumps(
                                                         nueva_empresa),
                                                     headers={'Content-Type': 'application/json'})

        self.assertEqual(solicitud_nueva_empresa.status_code, 409)    

if __name__ == '__main__':
    unittest.main()