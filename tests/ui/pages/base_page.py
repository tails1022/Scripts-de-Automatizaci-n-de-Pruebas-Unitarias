import os
import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    """
    Clase base que implementa el patrón Page Object Model (POM).
    Proporciona métodos genéricos reutilizables para interactuar con la página web,
    gestionar esperas explícitas y capturar evidencias.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def navigate_to(self, url: str) -> None:
        """Navega a una URL específica."""
        self.driver.get(url)

    def find_element(self, locator: tuple[By, str]):
        """Encuentra un elemento esperando a que esté presente en el DOM."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator: tuple[By, str]) -> None:
        """Espera a que un elemento sea clickeable y hace clic en él."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def send_keys(self, locator: tuple[By, str], text: str, clear_first: bool = True) -> None:
        """Escribe texto en un campo de entrada tras esperar su visibilidad."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple[By, str]) -> str:
        """Obtiene el texto visible de un elemento web."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text

    def is_visible(self, locator: tuple[By, str], timeout: int = 5) -> bool:
        """Verifica si un elemento es visible en pantalla dentro del tiempo límite."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def take_screenshot(self, filename: str) -> str:
        """
        Guarda una captura de pantalla en la carpeta de evidencias.
        Retorna la ruta absoluta del archivo generado.
        """
        output_dir = os.path.join(os.getcwd(), "evidencias")
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        self.driver.save_screenshot(filepath)
        return filepath
