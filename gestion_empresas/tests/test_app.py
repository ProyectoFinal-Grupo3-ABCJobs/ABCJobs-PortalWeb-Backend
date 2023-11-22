import unittest, json
import os
import requests
import json


directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)


if carpeta_actual == "gestion_empresas" or carpeta_actual == "app":
    from app import app
    from modelo import db
else:
    from gestion_empresas.app import app
    from gestion_empresas.modelo import db


class TestApp(unittest.TestCase):
    def setUp(self):
        #url = "http://loadbalancerproyectoabc-735612126.us-east-2.elb.amazonaws.com:5000/users/auth"

        url = "http://127.0.0.1:5000/users/auth"

        payload = json.dumps({"usuario": "empresa", "contrasena": "empresa"})
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

        self.nueva_empresa = {
            "razonSocial": "EmpresaPrueba",
            "nit": "455889899",
            "direccion": "calle 20",
            "telefono": "8996565",
            "idCiudad": "12",
            'idUsuario':"2",
        }



        self.app = app.test_client()

    def tearDown(self):
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())

    #@unittest.skip('muchas pruebas')
    def test_response_status_200(self):
        response = self.app.get("/company/ping")
        self.assertEqual(response.status_code, 200)

    #@unittest.skip('muchas pruebas')
    def test_response_json(self):
        response = self.app.get("/company/ping")
        data: dict = {"mensaje": "healthcheck OK"}
        response_dict = json.loads(response.data)
        self.assertEqual(response_dict, data)

    #@unittest.skip('muchas pruebas')
    def test_create_company(self):

        solicitud_nueva_empresa = self.app.post(
            "/company/register",
            data=json.dumps(self.nueva_empresa),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(solicitud_nueva_empresa.status_code, 201)

    #@unittest.skip('muchas pruebas')
    def test_create_company_name_exists(self):
        nueva_empresa = {
            "razonSocial": "EmpresaPrueba",
            "nit": "4558898558",
            "direccion": "calle 20",
            "telefono": "8996565",
            "idCiudad": "12",
            'idUsuario':"2",
        }

        solicitud_nueva_empresa = self.app.post(
            "/company/register",
            data=json.dumps(nueva_empresa),
            headers={"Content-Type": "application/json"},
        )

        nueva_empresa = {
            "razonSocial": "EmpresaPrueba",
            "nit": "455888558",
            "direccion": "calle 20",
            "telefono": "8996565",
            "idCiudad": "12",
            'idUsuario':"2",
        }

        solicitud_nueva_empresa = self.app.post(
            "/company/register",
            data=json.dumps(nueva_empresa),
            headers={"Content-Type": "application/json"},
        )

        self.assertEqual(solicitud_nueva_empresa.status_code, 409)

    #@unittest.skip('muchas pruebas')
    def test_create_company_nit_exists(self):
        nueva_empresa = {
            "razonSocial": "EmpresaPrueba1",
            "nit": "455889855878",
            "direccion": "calle 20",
            "telefono": "8996565",
            "idCiudad": "12",
            'idUsuario':"2",
        }

        solicitud_nueva_empresa = self.app.post(
            "/company/register",
            data=json.dumps(nueva_empresa),
            headers={"Content-Type": "application/json"},
        )

        nueva_empresa = {
            "razonSocial": "EmpresaPrueba2",
            "nit": "455889855878",
            "direccion": "calle 20",
            "telefono": "8996565",
            "idCiudad": "12",
            'idUsuario':"2",
        }

        solicitud_nueva_empresa = self.app.post(
            "/company/register",
            data=json.dumps(nueva_empresa),
            headers={"Content-Type": "application/json"},
        )

        self.assertEqual(solicitud_nueva_empresa.status_code, 409)

    #@unittest.skip('muchas pruebas')
    def test_create_project(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.token),
        }


        self.app.post(
            "/company/register",
            data=json.dumps(self.nueva_empresa),
            headers=encabezados_con_autorizacion,
        )

        nuevo_proyecto = {
            "nombreProyecto": "ProyectoTest1",
            "numeroColaboradores": "",
            "fechaInicio": "2020-01-01",
            "empresa_id": "235",
        }

        solicitud_nuevo_proyecto = self.app.post(
            f"/company/235/projectCreate",
            data=json.dumps(nuevo_proyecto),
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(solicitud_nuevo_proyecto.status_code, 201)

    #@unittest.skip('muchas pruebas')
    def test_create_project_name_exists(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        self.app.post(
            "/company/register",
            data=json.dumps(self.nueva_empresa),
            headers=encabezados_con_autorizacion,
        )

        nuevo_proyecto1 = {
            "nombreProyecto": "ProyectoPrueba22",
            "numeroColaboradores": "",
            "fechaInicio": "2020-01-01",
            "empresa_id": "1",
        }

        self.app.post(
            "/company/1/projectCreate",
            data=json.dumps(nuevo_proyecto1),
            headers=encabezados_con_autorizacion,
        )

        nuevo_proyecto2 = {
            "nombreProyecto": "ProyectoPrueba22",
            "numeroColaboradores": "",
            "fechaInicio": "2020-01-01",
            "empresa_id": "1",
        }

        solicitud_nuevo_proyecto2 = self.app.post(
            "/company/1/projectCreate",
            data=json.dumps(nuevo_proyecto2),
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(solicitud_nuevo_proyecto2.status_code, 409)

    #@unittest.skip('muchas pruebas')
    def test_create_project_empty_fields(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }


        self.app.post(
            "/company/register",
            data=json.dumps(self.nueva_empresa),
            headers=encabezados_con_autorizacion,
        )

        nuevo_proyecto = {
            "nombreProyecto": "",
            "numeroColaboradores": "",
            "fechaInicio": "",
            "empresa_id": "1",
        }

        solicitud_nuevo_proyecto = self.app.post(
            "/company/1/projectCreate",
            data=json.dumps(nuevo_proyecto),
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(solicitud_nuevo_proyecto.status_code, 400)

    # def test_search_projets_for_company_without_projets(self):

    #     encabezados_con_autorizacion = {
    #         'Content-Type': 'application/json',
    #         'Authorization': f'Bearer {self.token}'

    #     }
    #     resultado_proyectos_de_empresa = self.app.get("/company/416/projects",
    #                                                  headers=encabezados_con_autorizacion)
    #     self.assertEqual(resultado_proyectos_de_empresa.status_code, 200)

    # def test_search_projets_with_invalid_token(self):

    #     encabezados_con_autorizacion = {
    #         'Content-Type': 'application/json',
    #         'Authorization': f'Bearer {self.tokenCandiato}'
    #     }

    #     resultado_proyectos_de_empresa = self.app.get("/company/416/projects",
    #                                                  headers=encabezados_con_autorizacion)
    #     self.assertEqual(resultado_proyectos_de_empresa.status_code, 401)

    #@unittest.skip('muchas pruebas')
    def test_search_projets_for_company_without_projets(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        resultado_proyectos_de_empresa = self.app.get(
            "/company/416/projects", headers=encabezados_con_autorizacion
        )
        self.assertEqual(resultado_proyectos_de_empresa.status_code, 200)

    #@unittest.skip('muchas pruebas')
    def test_search_projets_with_invalid_token(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }

        resultado_proyectos_de_empresa = self.app.get(
            "/company/416/projects", headers=encabezados_con_autorizacion
        )
        self.assertEqual(resultado_proyectos_de_empresa.status_code, 401)

    '''def test_create_profile(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        nueva_empresa = {
            "razonSocial": "EmpresaTestPerfil",
            "nit": "999999999",
            "direccion": "calle 20",
            "telefono": "1234567",
            "idCiudad": "12",
        }

        self.app.post(
            "/company/register",
            data=json.dumps(nueva_empresa),
            headers=encabezados_con_autorizacion,
        )

        nuevo_proyecto = {
            "nombreProyecto": "ProyectoTestPerfil",
            "numeroColaboradores": "2",
            "fechaInicio": "2023-11-05",
        }

        self.app.post(
            "/company/1/projectCreate",
            data=json.dumps(nuevo_proyecto),
            headers=encabezados_con_autorizacion,
        )

        nuevo_perfil = {"nombre": "Perfil1", "descripcion": "Descripcion1"}

        solicitud_nuevo_perfil = self.app.post(
            "/company/projects/1/profiles",
            data=json.dumps(nuevo_perfil),
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(solicitud_nuevo_perfil.status_code, 201)

    def test_get_profile(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        solicitud_nuevo_perfil = self.app.get(
            "/company/projects/1/profiles",
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(solicitud_nuevo_perfil.status_code, 200)'''

    #@unittest.skip('muchas pruebas')
    def test_get_profile_without_projets(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        solicitud_nuevo_perfil = self.app.get(
            "/company/projects/999/profiles",
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(solicitud_nuevo_perfil.status_code, 404)

    '''def test_get_internal_employees(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        solicitud_nuevo_perfil = self.app.get(
            "/company/projects/1/internalEmployees",
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(solicitud_nuevo_perfil.status_code, 200)'''

    #@unittest.skip('muchas pruebas')
    def test_get_internal_employees_without_projets(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        solicitud_nuevo_perfil = self.app.get(
            "/company/projects/999/internalEmployees",
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(solicitud_nuevo_perfil.status_code, 404)

    '''def test_create_file(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        nueva_empresa = {
            "razonSocial": "EmpresaTestFile",
            "nit": "888888888",
            "direccion": "calle 20",
            "telefono": "1234567",
            "idCiudad": "12",
        }

        self.app.post(
            "/company/register",
            data=json.dumps(nueva_empresa),
            headers=encabezados_con_autorizacion,
        )

        nuevo_proyecto = {
            "nombreProyecto": "ProyectoTestFile",
            "numeroColaboradores": "1",
            "fechaInicio": "2023-11-05",
        }

        self.app.post(
            "/company/1/projectCreate",
            data=json.dumps(nuevo_proyecto),
            headers=encabezados_con_autorizacion,
        )

        nuevo_perfil = {"nombre": "Perfil1", "descripcion": "Descripcion1"}

        self.app.post(
            "/company/projects/1/profiles",
            data=json.dumps(nuevo_perfil),
            headers=encabezados_con_autorizacion,
        )

        nueva_ficha = {
            "empleados": [{"idEmpleado": 1}],
            "perfiles": [{"idPerfil": 1}],
        }

        solicitud_nueva_ficha = self.app.post(
            "/company/projects/1/files",
            data=json.dumps(nueva_ficha),
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(solicitud_nueva_ficha.status_code, 201)'''

    #@unittest.skip('muchas pruebas')
    def test_create_employee(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        self.app.post(
            "/company/register",
            data=json.dumps(self.nueva_empresa),
            headers=encabezados_con_autorizacion,
        )

        nuevo_empleado = {
            "tipoIdentificacion": "CC",
            "identificacion": "154365",
            "nombre": "Pedro Pérez",
            "cargo": "Ingeniero de Sistemas",
        }

        solicitud_nuevo_empleado = self.app.post(
            "/company/1/assignEmployee",
            data=json.dumps(nuevo_empleado),
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(solicitud_nuevo_empleado.status_code, 201)

    #@unittest.skip('muchas pruebas')
    def test_create_employee_document_exists(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        self.app.post(
            "/company/register",
            data=json.dumps(self.nueva_empresa),
            headers=encabezados_con_autorizacion,
        )

        nuevo_empleado = {
            "tipoIdentificacion": "CC",
            "identificacion": "154365789",
            "nombre": "Pedro Pérez",
            "cargo": "Ingeniero de Sistemas",
        }

        self.app.post(
            "/company/1/assignEmployee",
            data=json.dumps(nuevo_empleado),
            headers=encabezados_con_autorizacion,
        )

        nuevo_empleado2 = {
            "tipoIdentificacion": "CC",
            "identificacion": "154365789",
            "nombre": "Juan Pérez",
            "cargo": "Ingeniero de Sistemas",
        }

        solicitud_nuevo_empleado2 = self.app.post(
            "/company/1/assignEmployee",
            data=json.dumps(nuevo_empleado2),
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(solicitud_nuevo_empleado2.status_code, 409)

    #@unittest.skip('muchas pruebas')
    def test_create_employee_empty_fields(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }


        self.app.post(
            "/company/register",
            data=json.dumps(self.nueva_empresa),
            headers=encabezados_con_autorizacion,
        )

        nuevo_empleado = {
            "tipoIdentificacion": "",
            "identificacion": "",
            "nombre": "",
            "cargo": "Ingeniero de Sistemas",
        }

        solicitud_nuevo_empleado = self.app.post(
            "/company/1/assignEmployee",
            data=json.dumps(nuevo_empleado),
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(solicitud_nuevo_empleado.status_code, 400)



# ---PRUEBAS TOKEN INVALIDO
    def test_sVistaConsultaProyectoPorEmpresa_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }
        resultado_proyectos_de_empresa = self.app.get(
            "/company/416/projects", headers=encabezados_con_autorizacion
        )
        self.assertEqual(resultado_proyectos_de_empresa.status_code, 401)


    def test_VistaListaProyectosSinFichaPorIdEmpresa_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }
        resultado_proyectos_de_empresa = self.app.get(
            "/company/234/projects/ficha", headers=encabezados_con_autorizacion
        )
        self.assertEqual(resultado_proyectos_de_empresa.status_code, 401)



    def test_VistaCreacionProyecto_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }
        resultado_proyectos_de_empresa = self.app.post(
            "/company/234/projectCreate", headers=encabezados_con_autorizacion
        )
        self.assertEqual(resultado_proyectos_de_empresa.status_code, 401)

    def test_VistaConsultaTodosPerfiles_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }
        resultado_proyectos_de_empresa = self.app.get(
            "/company/profiles", headers=encabezados_con_autorizacion
        )
        self.assertEqual(resultado_proyectos_de_empresa.status_code, 401)



    def test_VistaAsignacionEmpleado_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }
        resultado_proyectos_de_empresa = self.app.post(
            "/company/111/assignEmployee", headers=encabezados_con_autorizacion
        )
        self.assertEqual(resultado_proyectos_de_empresa.status_code, 401)

    def test_VistaCreacionDesempenoEmpleado_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }
        resultado_proyectos_de_empresa = self.app.post(
            "/company/contrato/111/desempenoEmpleado", headers=encabezados_con_autorizacion
        )
        self.assertEqual(resultado_proyectos_de_empresa.status_code, 401)



if __name__ == "__main__":
    unittest.main()
