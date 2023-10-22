import unittest, json

from app import app
from modelo import db


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
    
    def test_response_status_200(self):
        response = self.app.get('/candidate/ping')
        self.assertEqual(response.status_code, 200)


    def test_response_json(self):
        response = self.app.get('/candidate/ping')
        data:dict = {
            "mensaje": "healthcheck OK"
            }
        response_dict = json.loads(response.data)
        self.assertEqual(response_dict, data)

    def test_registrar_info_candidato(self):
            
            nuevo_candidato = {
                "tipoIdentificacion": "CC",
                "identificacion": "123456789",
                "nombre": "CandidatoPrueba",
                "direccion": "calle 20",
                "telefono": "89965656565",
                "profesion": "ingeniero",
                "aniosExperiencia": "5",
                "idCiudad": "12",
                "idDepartamento": "1",
                "idPais": "1",
                "ultimoEstudio": "Maestria",
                "institucion": "Universidad Nacional",
                "anioGrado": "2019",
                "idCiudadInst": "12",
                "idDepartamentoInst": "1",
                "cargoUltimoEmpleo": "ingeniero",
                "empresa": "EmpresaPrueba",
                "anioIngreso": "2019",
                "anioRetiro": "2020",
                "palabrasClave": "palabra1, palabra2, palabra3"
            }

            solicitud_nuevo_candidato = self.app.post("/candidate/registerInfo",
                                                         data=json.dumps(
                                                             nuevo_candidato),
                                                         headers={'Content-Type': 'application/json'})
            
            self.assertEqual(solicitud_nuevo_candidato.status_code, 201)

    def test_campos_obligatorios_vacios(self):
         
            nuevo_candidato = {
                "tipoIdentificacion": "CC",
                "identificacion": "",
                "nombre": "CandidatoTest",
                "direccion": "calle 20",
                "telefono": "",
                "profesion": "ingeniero",
                "aniosExperiencia": "",
                "idCiudad": "12",
                "idDepartamento": "1",
                "idPais": "1",
                "ultimoEstudio": "Pregrado",
                "institucion": "Universidad Piloto",
                "anioGrado": "",
                "idCiudadInst": "12",
                "idDepartamentoInst": "1",
                "cargoUltimoEmpleo": "",
                "empresa": "Empresa1",
                "anioIngreso": "",
                "anioRetiro": "",
                "palabrasClave": "palabra1, palabra2, palabra3"
            }

            solicitud_nuevo_candidato = self.app.post("/candidate/registerInfo",
                                                            data=json.dumps(
                                                                nuevo_candidato),
                                                            headers={'Content-Type': 'application/json'})
            
            self.assertEqual(solicitud_nuevo_candidato.status_code, 400)

    def test_identificacion_exists(self):
         
            nuevo_candidato1 = {
                "tipoIdentificacion": "CC",
                "identificacion": "321321321",
                "nombre": "CandidatoPrueba1",
                "direccion": "calle 20",
                "telefono": "89965656565",
                "profesion": "ingeniero",
                "aniosExperiencia": "5",
                "idCiudad": "12",
                "idDepartamento": "1",
                "idPais": "1",
                "ultimoEstudio": "Maestria",
                "institucion": "Universidad Nacional",
                "anioGrado": "2019",
                "idCiudadInst": "12",
                "idDepartamentoInst": "1",
                "cargoUltimoEmpleo": "ingeniero",
                "empresa": "EmpresaPrueba",
                "anioIngreso": "2019",
                "anioRetiro": "",
                "palabrasClave": "palabra1, palabra2, palabra3"
            }

            solicitud_nuevo_candidato1 = self.app.post("/candidate/registerInfo",
                                                            data=json.dumps(
                                                                nuevo_candidato1),
                                                            headers={'Content-Type': 'application/json'})
            
            nuevo_candidato2 = {
                "tipoIdentificacion": "CC",
                "identificacion": "321321321",
                "nombre": "CandidatoPrueba2",
                "direccion": "calle 20",
                "telefono": "89965656565",
                "profesion": "ingeniero",
                "aniosExperiencia": "5",
                "idCiudad": "12",
                "idDepartamento": "1",
                "idPais": "1",
                "ultimoEstudio": "Maestria",
                "institucion": "Universidad Nacional",
                "anioGrado": "2019",
                "idCiudadInst": "12",
                "idDepartamentoInst": "1",
                "cargoUltimoEmpleo": "ingeniero",
                "empresa": "EmpresaPrueba",
                "anioIngreso": "2019",
                "anioRetiro": "2020",
                "palabrasClave": "palabra1, palabra2, palabra3"
            }

            solicitud_nuevo_candidato2 = self.app.post("/candidate/registerInfo",
                                                            data=json.dumps(
                                                                nuevo_candidato2),
                                                            headers={'Content-Type': 'application/json'})
            
            self.assertEqual(solicitud_nuevo_candidato2.status_code, 400)



if __name__ == '__main__':
    unittest.main()