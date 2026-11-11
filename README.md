# Taller: Scripts de Automatización de Pruebas Unitarias y Funcionales

Repositorio con scripts y frameworks de pruebas automatizadas para **Formularios Web (Selenium WebDriver)** y **Puntos de Enlace API REST (Requests / Postman)**, aplicando principios de calidad de software, el patrón arquitectónico **Modelo de Objetos de Página (Page Object Model - POM)** y aserciones completas en español.

---

## 🏗️ Arquitectura del Proyecto

```text
├── app/
│   ├── index.html                  # Portal académico universitario para pruebas UI
│   └── simulador_postman.html      # Visor interactivo de respuestas y tests de API
├── tests/
│   ├── ui/                         # Pruebas de Interfaz Web (Selenium WebDriver)
│   │   ├── pages/
│   │   │   ├── base_page.py        # Clase base con esperas explícitas y métodos reutilizables
│   │   │   └── login_page.py       # Page Object Model del formulario de inicio de sesión
│   │   ├── conftest.py             # Fixture de Pytest para gestión del navegador
│   │   └── test_web_form.py        # Casos de prueba funcionales (éxito, contraseña errónea, etc.)
│   └── api/                        # Pruebas de Servicios (API REST)
│       ├── test_api_rest.py        # Suite de pruebas automatizadas con Requests + Pytest
│       └── Postman_Collection.json # Colección de Postman v2.1 con aserciones en JavaScript
├── pytest.ini                      # Configuración central de Pytest
├── requirements.txt                # Dependencias requeridas del proyecto
├── run_tests.bat                   # Ejecutable por lotes en 1 clic para Windows
└── .gitignore                      # Exclusión de entornos virtuales, reportes y evidencias
```

---

## 🧪 Casos de Prueba Implementados

### 1. Formulario Web (Selenium WebDriver)
- **`TC-UI-01`**: Inicio de sesión exitoso con credenciales válidas y acceso a área segura.
- **`TC-UI-02`**: Manejo de error y denegación de acceso por contraseña incorrecta.
- **`TC-UI-03`**: Control de acceso por usuario no registrado en el sistema.
- **`TC-UI-04`**: Cierre de sesión seguro (`logout`) y retorno al formulario.

### 2. API REST (Requests / Postman)
- **`TC-API-01`**: `GET /api/users?page=2` - Consulta paginada, validación de código 200 OK, SLA de tiempo < 2s y esquema JSON.
- **`TC-API-02`**: `GET /api/users/2` - Consulta de usuario por ID con validación de campos y formato de correo.
- **`TC-API-03`**: `GET /api/users/23` - Caso negativo para recurso inexistente (código 404 Not Found y cuerpo vacío).
- **`TC-API-04`**: `POST /api/users` - Creación de nuevo usuario (código 201 Created, persistencia y marca de tiempo).
- **`TC-API-05`**: `POST /api/login` - Autenticación exitosa mediante API con generación de token.
- **`TC-API-06`**: `POST /api/login` - Caso negativo: rechazo por omisión de contraseña (código 400 Bad Request y mensaje de error).

---

## 🚀 Instalación y Ejecución

### Opción 1: Ejecución en 1 Clic (Windows)
Haz doble clic sobre el archivo:
```bat
run_tests.bat
```

### Opción 2: Ejecución desde la Consola
1. Crear y activar el entorno virtual de Python:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
2. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar las pruebas de API REST:
   ```bash
   python -m pytest tests/api/test_api_rest.py -v
   ```
4. Ejecutar las pruebas de Formulario Web (Selenium):
   ```bash
   python -m pytest tests/ui/test_web_form.py -v
   ```
   *(Para ejecución en segundo plano sin desplegar el navegador, añade `--headless`)*.

---

## 📮 Uso en Postman
1. Abrir **Postman** y presionar **Import**.
2. Seleccionar el archivo `tests/api/Postman_Collection.json`.
3. Ejecutar la colección para observar las 6 solicitudes y sus pruebas pasando al 100%.
