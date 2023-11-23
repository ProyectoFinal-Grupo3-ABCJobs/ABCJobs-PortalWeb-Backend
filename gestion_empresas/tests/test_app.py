import unittest, json
import os
import requests
import json
from faker import Faker
from flask import jsonify


directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)


if carpeta_actual == "gestion_empresas" or carpeta_actual == "app":
    from app import app
    from modelo import db
else:
    from gestion_empresas.app import app
    from gestion_empresas.modelo import db

fake = Faker()
class TestApp(unittest.TestCase):
    def setUp(self):
        url = "http://loadbalancerproyectoabc-735612126.us-east-2.elb.amazonaws.com:5000/users/auth"

        #url = "http://127.0.0.1:5000/users/auth"

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

        self.nueva_empresa_faker_data = {
            "nit": str(fake.random_int(min=0, max=100000))+'-2',
            "razonSocial": fake.company(),
            "direccion": fake.address(),
            "telefono": str(fake.phone_number()),
            "idCiudad": str(fake.random_int(min=1, max=99)),
            'idUsuario':"2",
        }
        self.nuevo_proyecto_faker_data = {
            "nombreProyecto": fake.company(),
            "fechaInicio": '2024-01-06',
        }
        
        self.nuevo_contrato_faker_data = {
            "numeroContrato": str(fake.random_int(min=1, max=99)),
            "idCandidato": str(fake.random_int(min=1, max=99)),
            "nombreCandidato": fake.name(),
            "idProyecto": str(fake.random_int(min=1, max=99)),
            "idCargo": str(fake.random_int(min=1, max=99)),
            "idEmpresa":str(fake.random_int(min=1, max=99)),
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
            "identificacion": str(fake.random_int(min=1, max=999)),
            "nombre": fake.company(),
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
    #@unittest.skip('muchas pruebas')
    def test_sVistaConsultaProyectoPorEmpresa_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }
        resultado_proyectos_de_empresa = self.app.get(
            "/company/416/projects", headers=encabezados_con_autorizacion
        )
        self.assertEqual(resultado_proyectos_de_empresa.status_code, 401)

    #@unittest.skip('muchas pruebas')
    def test_VistaListaProyectosSinFichaPorIdEmpresa_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }
        resultado_proyectos_de_empresa = self.app.get(
            "/company/234/projects/ficha", headers=encabezados_con_autorizacion
        )
        self.assertEqual(resultado_proyectos_de_empresa.status_code, 401)


    #@unittest.skip('muchas pruebas')
    def test_VistaCreacionProyecto_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }
        resultado_proyectos_de_empresa = self.app.post(
            "/company/234/projectCreate", headers=encabezados_con_autorizacion
        )
        self.assertEqual(resultado_proyectos_de_empresa.status_code, 401)

    #@unittest.skip('muchas pruebas')
    def test_VistaConsultaTodosPerfiles_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }
        resultado_proyectos_de_empresa = self.app.get(
            "/company/profiles", headers=encabezados_con_autorizacion
        )
        self.assertEqual(resultado_proyectos_de_empresa.status_code, 401)


    #@unittest.skip('muchas pruebas')
    def test_VistaAsignacionEmpleado_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }
        resultado_proyectos_de_empresa = self.app.post(
            "/company/111/assignEmployee", headers=encabezados_con_autorizacion
        )
        self.assertEqual(resultado_proyectos_de_empresa.status_code, 401)

    #@unittest.skip('muchas pruebas')
    def test_VistaCreacionDesempenoEmpleado_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }
        resultado_proyectos_de_empresa = self.app.post(
            "/company/contrato/111/desempenoEmpleado", headers=encabezados_con_autorizacion
        )
        self.assertEqual(resultado_proyectos_de_empresa.status_code, 401)

    #@unittest.skip('muchas pruebas')
    def test_VistaListaProyectosSinFichaPorIdEmpresa_sin_proyectos(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        resultado__de_empresa_sin_proyectos = self.app.get(
            "/company/133/projects/ficha", headers=encabezados_con_autorizacion
        )
        self.assertEqual(resultado__de_empresa_sin_proyectos.status_code, 200)

    #@unittest.skip('muchas pruebas')
    def test_VistaListaProyectosSinFichaPorIdEmpresa_con_proyectos(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        # Creo empresa
        resultado = self.app.post(
            "/company/register",
            data=json.dumps(self.nueva_empresa_faker_data),
            headers=encabezados_con_autorizacion,
        )

        datos_request= resultado.data
        request_json = datos_request.decode('utf-8')
        request_json_ = json.loads(request_json)
        #request_json_['id']
        #self.assertEqual(request_json_['id'], 555)
        id_empresa= request_json_["id"]
        
        # Creo el proyecto
        resultado_proyecto = self.app.post(
            '/company/{}/projectCreate'.format(id_empresa),
            data=json.dumps(self.nuevo_proyecto_faker_data),
            headers=encabezados_con_autorizacion,
        )
        # Busco la empresa
        resultado_empresa_fichas = self.app.get(
            '/company/{}/projects/ficha'.format(id_empresa),
            data=json.dumps(self.nuevo_proyecto_faker_data),
            headers=encabezados_con_autorizacion,
        )
        self.assertEqual(resultado_empresa_fichas.status_code, 200)

    #@unittest.skip('muchas pruebas')
    def test_VistaObtenerEmpresaPorIdUsuario_con_usuario_asignado(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        # Creo el proyecto
        resultado_empresa = self.app.post(
            '/company/user',
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(resultado_empresa.status_code, 200)

    #@unittest.skip('muchas pruebas')
    def test_VistaEmpladoInterno_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }

        # Creo el proyecto
        resultado_empleado = self.app.get(
            '/company/2/internalEmployees',
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(resultado_empleado.status_code, 401)

    #@unittest.skip('muchas pruebas')
    def test_VistaConsultaTodosPerfiles_sin_perfiles_asociados(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        # Creo el proyecto
        resultado_empleado = self.app.get(
            '/company/profiles',
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(resultado_empleado.status_code, 404)

    #@unittest.skip('muchas pruebas')
    def test_VistaVistaFicha_error_token(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }

        # Creo el proyecto
        resultado_empresa = self.app.post(
            '/company/projects/34/files',
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(resultado_empresa.status_code, 401)

    #@unittest.skip('muchas pruebas')
    def test_VistaVistaFicha_sin_token(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json"
        }

        # Creo el proyecto
        resultado_ficha = self.app.post(
            '/company/projects/1asaa/files',
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(resultado_ficha.status_code, 404)

    #@unittest.skip('muchas pruebas')
    def test_VistaFicha_crear_ficha_bad_request(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        # Creo el proyecto, sin no funciona debo crear la empresa
        resultado_proyecto = self.app.post(
            '/company/2/projectCreate',
            data=json.dumps(self.nuevo_proyecto_faker_data),
            headers=encabezados_con_autorizacion,
        )
        datos_request= resultado_proyecto.data
        request_json = datos_request.decode('utf-8')
        request_json_ = json.loads(request_json)
        if_proyecto = request_json_['id']

        resultado_ficha = self.app.post(
            '/company/projects/{}/files'.format(if_proyecto),
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(resultado_ficha.status_code, 500)


    @unittest.skip('muchas pruebas')
    def test_VistaMotorEmparejamientoInterno_sin_fichas(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        resultado = self.app.post(
            "/company/motorEmparejamientoTempFicha",
            headers=encabezados_con_autorizacion,
        )

        datos_request= resultado.data
        request_json = datos_request.decode('utf-8')
        request_json_ = json.loads(request_json)
        self.assertEqual(request_json_["Mensaje 200"], 'Proceso de emparejamiento realizado correctamente!')


    def test_VistaMotorEmparejamientoInterno_ficha_sin_proyecto(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        # Creo el proyecto, sin no funciona debo crear la empresa
        resultado_proyecto = self.app.post(
            '/company/2/projectCreate',
            data=json.dumps(self.nuevo_proyecto_faker_data),
            headers=encabezados_con_autorizacion,
        )
        datos_request= resultado_proyecto.data
        request_json = datos_request.decode('utf-8')
        request_json_ = json.loads(request_json)
        id_proyecto = request_json_['id']


        resultado_ficha = self.app.post(
            f'/company/projects/{id_proyecto}/files',
            headers=encabezados_con_autorizacion,
        )
        self.assertEqual(resultado_ficha.status_code, 500)



    def test_VistaContratoCandidato_ok(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        # Creo el contrato, sin no funciona debo crear la empresa
        resultado_proyecto = self.app.post(
            '/company/contratoCandidato',
            data=json.dumps(self.nuevo_contrato_faker_data),
            headers=encabezados_con_autorizacion,
        )

        self.assertEqual(resultado_proyecto.status_code, 201)


    def test_VistaCreacionDesempenoEmpleado_campos_vacios(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        data = {
            "calificacion":str(fake.random_int(min=1, max=99)),
        }
        # Creo el proyecto, sin no funciona debo crear la empresa
        resultado_proyecto = self.app.post(
            '/company/contrato/231/desempenoEmpleado',
            data=json.dumps(data),
            headers=encabezados_con_autorizacion,
        )
        self.assertEqual(resultado_proyecto.status_code, 400)



    def test_VistaObtenerContratosPorEmpresa_token_invalido(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokenCandiato}",
        }

        # Creo el proyecto, sin no funciona debo crear la empresa
        resultado_proyecto = self.app.get(
            '/company/123/contratos',
            headers=encabezados_con_autorizacion,
        )
        self.assertEqual(resultado_proyecto.status_code, 401)

    def test_VistaObtenerContratosPorEmpresa_ok(self):
        encabezados_con_autorizacion = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        # Creo el proyecto, sin no funciona debo crear la empresa
        resultado_proyecto = self.app.get(
            '/company/123/contratos',
            headers=encabezados_con_autorizacion,
        )
        self.assertEqual(resultado_proyecto.status_code, 200)



if __name__ == "__main__":
    unittest.main()
