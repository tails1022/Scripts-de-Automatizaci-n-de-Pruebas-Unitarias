from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from tests.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object Model que encapsula los elementos y acciones del
    formulario de autenticación web universitario (100% en español).
    """

    # Ruta absoluta del archivo HTML local en formato URI (file:///)
    RUTA_HTML = Path(__file__).resolve().parent.parent.parent.parent / "app" / "index.html"
    URL = RUTA_HTML.as_uri()

    # Localizadores de elementos de la interfaz web
    CAMPO_USUARIO = (By.ID, "campo-usuario")
    CAMPO_CONTRASENA = (By.ID, "campo-contrasena")
    BOTON_INICIAR_SESION = (By.ID, "boton-iniciar-sesion")
    MENSAJE_ALERTA = (By.ID, "mensaje-alerta")
    BOTON_CERRAR_SESION = (By.ID, "boton-cerrar-sesion")
    SECCION_AREA_SEGURA = (By.ID, "seccion-area-segura")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def load(self) -> "LoginPage":
        """Carga la página web del formulario en el navegador."""
        self.navigate_to(self.URL)
        return self

    def login(self, usuario: str, contrasena: str) -> "LoginPage":
        """Diligencia el formulario y presiona el botón Iniciar Sesión."""
        self.send_keys(self.CAMPO_USUARIO, usuario)
        self.send_keys(self.CAMPO_CONTRASENA, contrasena)
        self.click(self.BOTON_INICIAR_SESION)
        return self

    def get_flash_message(self) -> str:
        """Obtiene el texto de la alerta o notificación en pantalla."""
        return self.get_text(self.MENSAJE_ALERTA).strip()

    def is_logout_button_present(self) -> bool:
        """Comprueba si el botón de cerrar sesión está visible."""
        return self.is_visible(self.BOTON_CERRAR_SESION)

    def logout(self) -> "LoginPage":
        """Presiona el botón Cerrar Sesión en el área segura."""
        self.click(self.BOTON_CERRAR_SESION)
        return self
