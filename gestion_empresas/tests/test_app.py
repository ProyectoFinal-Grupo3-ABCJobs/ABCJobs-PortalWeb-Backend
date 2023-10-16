import unittest, json

from gestion_empresas.app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_response_status_200(self):
        response = self.app.get('/empresas/ping')
        self.assertEqual(response.status_code, 200)


    def test_response_json(self):
        response = self.app.get('/empresas/ping')
        data:dict = {
            "mensaje": "healthcheck OK"
            }
        response_dict = json.loads(response.data)
        self.assertEqual(response_dict, data)


if __name__ == '__main__':
    unittest.main()