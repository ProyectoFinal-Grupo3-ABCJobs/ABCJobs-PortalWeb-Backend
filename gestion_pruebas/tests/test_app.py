import unittest, json
import os
import requests
import json


directorio_actual = os.getcwd()
carpeta_actual = os.path.basename(directorio_actual)


if carpeta_actual == "gestion_pruebas" or carpeta_actual == "app":
    from app import app
    from modelo import db
else:
    from gestion_pruebas.app import app
    from gestion_pruebas.modelo import db


class TestApp(unittest.TestCase):
    def setUp(self):
        url = "http://loadbalancerproyectoabc-735612126.us-east-2.elb.amazonaws.com:5000/users/auth"

        # url = "http://127.0.0.1:5000/users/auth"

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


if __name__ == "__main__":
    unittest.main()
