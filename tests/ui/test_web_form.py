import time
import pytest
from tests.ui.pages.login_page import LoginPage


class TestAutenticacionFormularioWeb:
    """
    Suite de pruebas funcionales automatizadas para el formulario web universitario.
    Verifica los flujos de autenticación, mensajes de validación y control de acceso en español.
    """

    USUARIO_VALIDO = "estudiante"
    CONTRASENA_VALIDA = "ClaveSegura2026!"
    USUARIO_INVALIDO = "usuario_inexistente"
    CONTRASENA_INVALIDA = "ClaveErronea123"

    def test_tc_ui_01_inicio_sesion_exitoso(self, driver):
        """
        TC-UI-01: Validar inicio de sesión exitoso con credenciales correctas.
        """
        pagina = LoginPage(driver)
        pagina.load()

        # Guardar captura del formulario en estado inicial
        pagina.take_screenshot("01_formulario_inicial.png")

        # Diligenciar credenciales válidas
        pagina.login(self.USUARIO_VALIDO, self.CONTRASENA_VALIDA)

        # Comprobar mensaje de bienvenida en español y visibilidad de área segura
        mensaje = pagina.get_flash_message()
        assert "¡Inicio de sesión exitoso!" in mensaje, (
            f"Se esperaba mensaje de bienvenida en español pero se obtuvo: {mensaje}"
        )
        assert pagina.is_logout_button_present(), (
            "El botón 'Cerrar Sesión' debería estar visible en el área segura."
        )

        # Guardar captura de la pantalla de bienvenida y área segura
        pagina.take_screenshot("02_inicio_sesion_exitoso.png")

    def test_tc_ui_02_contrasena_incorrecta(self, driver):
        """
        TC-UI-02: Validar mensaje de error cuando la contraseña es incorrecta.
        """
        pagina = LoginPage(driver)
        pagina.load()

        pagina.login(self.USUARIO_VALIDO, self.CONTRASENA_INVALIDA)

        mensaje = pagina.get_flash_message()
        assert "La contraseña ingresada es incorrecta" in mensaje, (
            f"Se esperaba alerta de contraseña incorrecta pero se obtuvo: {mensaje}"
        )
        assert not pagina.is_logout_button_present(), (
            "No debería mostrar el botón de cerrar sesión ante un intento fallido."
        )

        pagina.take_screenshot("03_error_contrasena_invalida.png")

    def test_tc_ui_03_usuario_inexistente(self, driver):
        """
        TC-UI-03: Validar mensaje de error cuando el usuario no existe.
        """
        pagina = LoginPage(driver)
        pagina.load()

        pagina.login(self.USUARIO_INVALIDO, self.CONTRASENA_VALIDA)

        mensaje = pagina.get_flash_message()
        assert "El usuario ingresado no existe en el sistema" in mensaje, (
            f"Se esperaba alerta de usuario inexistente pero se obtuvo: {mensaje}"
        )

        pagina.take_screenshot("04_error_usuario_invalido.png")

    def test_tc_ui_04_cierre_sesion_exitoso(self, driver):
        """
        TC-UI-04: Validar flujo de cierre de sesión seguro tras autenticación.
        """
        pagina = LoginPage(driver)
        pagina.load()
        pagina.login(self.USUARIO_VALIDO, self.CONTRASENA_VALIDA)
        assert pagina.is_logout_button_present()

        # Presionar botón Cerrar Sesión
        pagina.logout()

        mensaje = pagina.get_flash_message()
        assert "Has cerrado sesión exitosamente" in mensaje, (
            f"Se esperaba confirmación de cierre de sesión pero se obtuvo: {mensaje}"
        )

        pagina.take_screenshot("05_cierre_sesion_exitoso.png")
