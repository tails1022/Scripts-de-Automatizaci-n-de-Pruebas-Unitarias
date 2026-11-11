import time
import requests
import pytest


class TestPruebasApiRestReqres:
    """
    Suite de pruebas automatizadas para la API REST pública Reqres (https://reqres.in/).
    Verifica códigos de estado HTTP, cabeceras, tiempos de respuesta, esquemas JSON
    y manejo de errores (casos positivos y negativos).
    """

    URL_BASE = "https://reqres.in/api"
    CABECERAS = {
        "Content-Type": "application/json",
        "User-Agent": "Pruebas-Automatizadas-Universidad/1.0",
    }

    def test_tc_api_01_consultar_lista_usuarios(self):
        """
        TC-API-01: Validar consulta paginada de usuarios (GET /users?page=2).
        Verifica: Código 200, Cabecera application/json, tiempo < 2s, estructura de datos.
        """
        punto_enlace = f"{self.URL_BASE}/users"
        parametros = {"page": 2}

        tiempo_inicio = time.time()
        respuesta = requests.get(punto_enlace, params=parametros, headers=self.CABECERAS, timeout=10)
        tiempo_transcurrido = time.time() - tiempo_inicio

        # Validar código de estado HTTP
        assert respuesta.status_code == 200, f"Se esperaba código 200 pero se recibió {respuesta.status_code}"

        # Validar cabecera de respuesta
        assert "application/json" in respuesta.headers.get("Content-Type", ""), (
            "El tipo de contenido (Content-Type) debe ser application/json"
        )

        # Validar tiempo de respuesta (SLA < 2.0 segundos)
        assert tiempo_transcurrido < 2.0, (
            f"Tiempo de respuesta excesivo: {tiempo_transcurrido:.2f} segundos"
        )

        # Validar cuerpo de la respuesta JSON
        cuerpo = respuesta.json()
        assert cuerpo.get("page") == 2, f"Página esperada 2, obtenida: {cuerpo.get('page')}"
        assert "data" in cuerpo, "La respuesta debe contener el campo 'data'"
        assert isinstance(cuerpo["data"], list), "El campo 'data' debe ser una lista"
        assert len(cuerpo["data"]) > 0, "La lista de usuarios no debe estar vacía"

        # Validar campos del primer usuario
        primer_usuario = cuerpo["data"][0]
        for campo in ["id", "email", "first_name", "last_name", "avatar"]:
            assert campo in primer_usuario, f"El objeto de usuario debe contener el campo '{campo}'"

    def test_tc_api_02_consultar_usuario_por_id(self):
        """
        TC-API-02: Validar consulta de un usuario específico existente (GET /users/2).
        """
        id_usuario = 2
        punto_enlace = f"{self.URL_BASE}/users/{id_usuario}"

        respuesta = requests.get(punto_enlace, headers=self.CABECERAS, timeout=10)

        assert respuesta.status_code == 200, f"Se esperaba código 200 pero se recibió {respuesta.status_code}"
        cuerpo = respuesta.json()
        assert "data" in cuerpo, "La respuesta debe contener el campo 'data'"
        assert cuerpo["data"]["id"] == id_usuario, f"Se esperaba ID {id_usuario}"
        assert "@" in cuerpo["data"]["email"], "El correo electrónico debe contener un formato válido con '@'"
        assert len(cuerpo["data"]["first_name"]) > 0, "El nombre no debe estar vacío"

    def test_tc_api_03_consultar_usuario_inexistente_404(self):
        """
        TC-API-03: Validar respuesta 404 al consultar un recurso inexistente (GET /users/23).
        Caso de prueba negativo.
        """
        id_usuario = 23
        punto_enlace = f"{self.URL_BASE}/users/{id_usuario}"

        respuesta = requests.get(punto_enlace, headers=self.CABECERAS, timeout=10)

        assert respuesta.status_code == 404, (
            f"Se esperaba código 404 para usuario inexistente, obtenido: {respuesta.status_code}"
        )
        assert respuesta.json() == {}, "El cuerpo de la respuesta 404 debe ser un objeto vacío"

    def test_tc_api_04_crear_nuevo_usuario(self):
        """
        TC-API-04: Validar creación de un nuevo usuario (POST /users).
        Verifica: Código 201 Created, persistencia de datos y generación de ID y marca de tiempo.
        """
        punto_enlace = f"{self.URL_BASE}/users"
        datos_envio = {
            "name": "Carlos Gomez",
            "job": "Ingeniero de Automatizacion QA",
        }

        respuesta = requests.post(punto_enlace, json=datos_envio, headers=self.CABECERAS, timeout=10)

        assert respuesta.status_code == 201, (
            f"Se esperaba código 201 Created, obtenido: {respuesta.status_code}"
        )
        cuerpo = respuesta.json()
        assert cuerpo.get("name") == datos_envio["name"], "El nombre recibido no coincide con el enviado"
        assert cuerpo.get("job") == datos_envio["job"], "El cargo recibido no coincide con el enviado"
        assert "id" in cuerpo, "La respuesta debe retornar el campo 'id' autogenerado"
        assert "createdAt" in cuerpo, "La respuesta debe retornar la marca de tiempo 'createdAt'"

    def test_tc_api_05_autenticacion_exitosa(self):
        """
        TC-API-05: Validar autenticación exitosa mediante API (POST /login).
        """
        punto_enlace = f"{self.URL_BASE}/login"
        credenciales = {
            "email": "eve.holt@reqres.in",
            "password": "cityslicka",
        }

        respuesta = requests.post(punto_enlace, json=credenciales, headers=self.CABECERAS, timeout=10)

        assert respuesta.status_code == 200, (
            f"Se esperaba código 200 OK, obtenido: {respuesta.status_code}"
        )
        cuerpo = respuesta.json()
        assert "token" in cuerpo, "La respuesta debe contener el token de autenticación"
        assert len(cuerpo["token"]) > 0, "El token de autenticación no debe estar vacío"

    def test_tc_api_06_autenticacion_fallida_sin_contrasena(self):
        """
        TC-API-06: Validar manejo de error en autenticación incompleta (POST /login sin contraseña).
        Caso de prueba negativo: Espera código HTTP 400 Bad Request y mensaje descriptivo.
        """
        punto_enlace = f"{self.URL_BASE}/login"
        credenciales_incompletas = {
            "email": "sydney@fife",
        }

        respuesta = requests.post(punto_enlace, json=credenciales_incompletas, headers=self.CABECERAS, timeout=10)

        assert respuesta.status_code == 400, (
            f"Se esperaba código 400 Bad Request, obtenido: {respuesta.status_code}"
        )
        cuerpo = respuesta.json()
        assert cuerpo.get("error") == "Missing password", (
            f"Mensaje de error inesperado recibido: {cuerpo.get('error')}"
        )
