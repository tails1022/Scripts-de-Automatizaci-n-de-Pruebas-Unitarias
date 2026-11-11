import os
import pytest
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions


def pytest_addoption(parser):
    """Permite añadir opciones personalizadas en la línea de comandos de pytest."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Ejecuta el navegador en modo sin cabeza (headless) sin abrir la ventana visible.",
    )
    parser.addoption(
        "--browser",
        action="store",
        default="edge",
        help="Navegador a utilizar: 'edge' o 'chrome'. Por defecto: 'edge'.",
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture de Pytest que inicializa y finaliza la instancia del navegador para cada prueba.
    Garantiza aislamiento entre casos de prueba.
    """
    headless = request.config.getoption("--headless")
    browser_name = request.config.getoption("--browser").lower()

    driver_instance = None

    if browser_name == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver_instance = webdriver.Edge(options=options)
    elif browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver_instance = webdriver.Chrome(options=options)
    else:
        raise ValueError(f"Navegador no soportado: {browser_name}. Use 'edge' o 'chrome'.")

    # Tiempo de espera implícito de respaldo
    driver_instance.implicitly_wait(2)

    yield driver_instance

    # Limpieza final: cerrar navegador
    try:
        driver_instance.quit()
    except Exception:
        pass
