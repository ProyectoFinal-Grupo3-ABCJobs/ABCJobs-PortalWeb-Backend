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
            "telefono": "8996565",
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
            "telefono": "8996565",
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
            "telefono": "8996565",
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
            "telefono": "8996565",
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
            "telefono": "8996565",
            "idCiudad": "12"
        }

        solicitud_nueva_empresa = self.app.post("/company/register",
                                                     data=json.dumps(
                                                         nueva_empresa),
                                                     headers={'Content-Type': 'application/json'})

        self.assertEqual(solicitud_nueva_empresa.status_code, 409)    

    def obtener_token_acceso(self):

        credenciales_empresa = {
            "usuario":"empresa",
            "contrasena":"empresa"
        }
        respuesta_login = self.app.post("http://loadbalancerproyectoabc-735612126.us-east-2.elb.amazonaws.com:5000/users/auth",
                                data=json.dumps(credenciales_empresa),
                                headers={'Content-Type': 'application/json'})

        print('Respuesta cruda del login:', respuesta_login.data)

        assert respuesta_login.status_code == 200, "El login falló o no devolvió un código de estado 200"

        try:
            data_respuesta = json.loads(respuesta_login.data.decode())
            return data_respuesta['access_token']
        except json.decoder.JSONDecodeError as e:
            print(f"Error al decodificar la respuesta JSON: {e}")
            raise

    def test_create_project(self):

        token_acceso = self.obtener_token_acceso()

        encabezados_con_autorizacion = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token_acceso}'
        }

        nueva_empresa = {
            "razonSocial":"EmpresaTest1",
            "nit": "4558898991",
            "direccion": "calle 20",
            "telefono": "8996565",
            "idCiudad": "12"
        }

        solicitud_nueva_empresa = self.app.post("/company/register",
                                                     data=json.dumps(
                                                         nueva_empresa),
                                                     headers=encabezados_con_autorizacion)
        

        nuevo_proyecto = {
            "nombreProyecto":"ProyectoTest1",
            "numeroColaboradores": "",
            "fechaInicio": "2020-01-01",
            "empresa_id": "1"
        }

        solicitud_nuevo_proyecto = self.app.post(f"/company/1/projectCreate",
                                                     data=json.dumps(
                                                         nuevo_proyecto),
                                                     headers=encabezados_con_autorizacion)

        self.assertEqual(solicitud_nuevo_proyecto.status_code, 201)

    def test_create_project_name_exists(self):

        token_acceso = self.obtener_token_acceso()

        encabezados_con_autorizacion = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token_acceso}'
        }

        nueva_empresa = {
            "razonSocial":"EmpresaTest2",
            "nit": "4558898992",
            "direccion": "calle 20",
            "telefono": "8996565",
            "idCiudad": "12"
        }

        solicitud_nueva_empresa = self.app.post("/company/register",
                                                     data=json.dumps(
                                                         nueva_empresa),
                                                     headers=encabezados_con_autorizacion)
        
        nuevo_proyecto1 = {
            "nombreProyecto":"ProyectoPrueba22",
            "numeroColaboradores": "",
            "fechaInicio": "2020-01-01",
            "empresa_id": "1"
        }

        solicitud_nuevo_proyecto1 = self.app.post("/company/1/projectCreate",
                                                     data=json.dumps(
                                                         nuevo_proyecto1),
                                                     headers=encabezados_con_autorizacion)

        nuevo_proyecto2 = {
            "nombreProyecto":"ProyectoPrueba22",
            "numeroColaboradores": "",
            "fechaInicio": "2020-01-01",
            "empresa_id": "1"
        }

        solicitud_nuevo_proyecto2 = self.app.post("/company/1/projectCreate",
                                                     data=json.dumps(
                                                         nuevo_proyecto2),
                                                     headers=encabezados_con_autorizacion)

        self.assertEqual(solicitud_nuevo_proyecto2.status_code, 409)

    def test_create_project_empty_fields(self):

        token_acceso = self.obtener_token_acceso()

        encabezados_con_autorizacion = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token_acceso}'
        }

        nueva_empresa = {
            "razonSocial":"EmpresaTest3",
            "nit": "4558898993",
            "direccion": "calle 20",
            "telefono": "8996565",
            "idCiudad": "12"
        }

        solicitud_nueva_empresa = self.app.post("/company/register",
                                                     data=json.dumps(
                                                         nueva_empresa),
                                                     headers=encabezados_con_autorizacion)

        nuevo_proyecto = {
            "nombreProyecto":"",
            "numeroColaboradores": "",
            "fechaInicio": "",
            "empresa_id": "1"
        }

        solicitud_nuevo_proyecto = self.app.post("/company/1/projectCreate",
                                                     data=json.dumps(
                                                         nuevo_proyecto),
                                                     headers=encabezados_con_autorizacion)

        self.assertEqual(solicitud_nuevo_proyecto.status_code, 400)

if __name__ == '__main__':
    unittest.main()