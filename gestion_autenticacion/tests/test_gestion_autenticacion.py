import unittest, json

from gestion_autenticacion.app import app
#  from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_response_healthcheck_status_200(self):
        response = self.app.get('/users/ping')
        self.assertEqual(response.status_code, 200)


    def test_response_healthcheck_json(self):
        response = self.app.get('/users/ping')
        data:dict = {
            "mensaje": "healthcheck OK"
            }
        response_dict = json.loads(response.data)
        self.assertEqual(response_dict, data)


    def test_response_auth_json_without_data(self):

        response = self.app.post('/users/auth')
        msg:dict = {
            "error 1010": "Solicitud sin datos"
            }
        response_dict = json.loads(response.data)
        self.assertEqual(response_dict, msg)

    def test_response_auth_without_password(self):

        response = self.app.post('/users/auth',json={"usuario":"user"})
        msg:dict = {
            "error 3030": "Faltan datos en la petición"
            }
        response_dict = json.loads(response.data)
        self.assertEqual(response_dict, msg)


    def test_response_auth_void_user_and_pwd(self):

        response = self.app.post('/users/auth',json={"usuario":"","contrasena":""})
        msg:dict = {
            "error 4040": "Falta informacion en la petición"
            }
        response_dict = json.loads(response.data)
        self.assertEqual(response_dict, msg)


    def test_response_auth_unauthorized(self):

        response = self.app.post('/users/auth',json={"usuario":"123","contrasena":"123"})
        msg:dict = {
            "error 5050": "El usuario no pudo ser autenticado"
            }
        response_dict = json.loads(response.data)
        self.assertEqual(response_dict, msg)


    # def test_response_auth_authorized(self):
    #     response = self.app.post('/users/auth',json={"usuario":"candidato","contrasena":"candidato"})
    #     self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()