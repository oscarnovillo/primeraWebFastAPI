# Mi Primera Web FastAPI 🚀

## Descripción

Esta es una aplicación web educativa creada con **FastAPI** y **Jinja2** para enseñar los conceptos básicos del desarrollo web backend. Incluye ejemplos prácticos de:

- 🔗 **Parámetros GET** (query parameters y path parameters)
- 📝 **Formularios POST** (simples y complejos)
- 🎨 **Sistema de plantillas Jinja2**
- 📦 **Manejo de datos en memoria**
- 🎯 **Validación de formularios**
- 🌐 **Navegación entre páginas**

## Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Instalar las dependencias:**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Ejecutar la aplicación:**
   ```powershell
   python main.py
   ```
   
   O alternativamente:
   ```powershell
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

3. **Abrir en el navegador:**
   ```
   http://127.0.0.1:8000
   ```

## Estructura del Proyecto

```
primeraWebFastAPI/
├── main.py                     # Aplicación principal FastAPI
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Este archivo
├── static/
│   └── style.css              # Estilos CSS
└── templates/                 # Plantillas Jinja2
    ├── base.html              # Plantilla base
    ├── inicio.html            # Página de inicio
    ├── navegacion.html        # Guía de navegación
    ├── productos.html         # Lista de productos
    ├── producto_detalle.html  # Detalle de producto
    ├── contacto.html          # Formulario de contacto
    ├── contacto_enviado.html  # Confirmación de contacto
    ├── registro.html          # Formulario de registro
    ├── registro_exitoso.html  # Confirmación de registro
    ├── usuarios.html          # Lista de usuarios
    ├── buscar_resultados.html # Resultados de búsqueda
    └── error.html             # Página de error
```

## Funcionalidades y Ejemplos

### 🔗 Parámetros GET

#### Query Parameters (parámetros de consulta)
- **URL:** `/productos?categoria=Tecnología`
- **Código:** `categoria: Optional[str] = None`
- **Uso:** Filtrar productos por categoría

#### Path Parameters (parámetros de ruta)
- **URL:** `/producto/1`
- **Código:** `producto_id: int`
- **Uso:** Mostrar detalles de un producto específico

### 📝 Formularios POST

#### Formulario Simple (Contacto)
```python
@app.post("/contacto")
async def procesar_contacto(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    mensaje: str = Form(...)
):
```

#### Formulario Complejo (Registro)
```python
@app.post("/registro")
async def procesar_registro(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    edad: int = Form(...),
    ciudad: str = Form(...),
    intereses: list = Form(...)
):
```

### 🎨 Sistema de Plantillas

#### Herencia de plantillas
```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

<!-- inicio.html -->
{% extends "base.html" %}
{% block title %}Inicio{% endblock %}
{% block content %}
    <h1>{{ titulo }}</h1>
{% endblock %}
```

## Páginas Disponibles

| Ruta | Método | Descripción | Conceptos |
|------|--------|-------------|-----------|
| `/` | GET | Página de inicio | Plantillas básicas |
| `/navegacion` | GET | Guía de navegación | Enlaces y explicaciones |
| `/productos` | GET | Lista de productos | Query parameters opcionales |
| `/productos?categoria=X` | GET | Productos filtrados | Query parameters |
| `/producto/{id}` | GET | Detalle de producto | Path parameters |
| `/contacto` | GET | Formulario de contacto | Formularios simples |
| `/contacto` | POST | Procesar contacto | POST con validación |
| `/registro` | GET | Formulario de registro | Formularios complejos |
| `/registro` | POST | Procesar registro | POST con múltiples tipos |
| `/usuarios` | GET | Lista de usuarios | Mostrar datos almacenados |
| `/buscar` | POST | Búsqueda de productos | POST con parámetros opcionales |

## Ejemplos de URLs para Probar

### Parámetros GET
```
http://127.0.0.1:8000/productos
http://127.0.0.1:8000/productos?categoria=Tecnología
http://127.0.0.1:8000/productos?categoria=Muebles
http://127.0.0.1:8000/producto/1
http://127.0.0.1:8000/producto/2
http://127.0.0.1:8000/producto/999  (error - no existe)
```

### Formularios POST
- **Contacto:** Llenar y enviar el formulario en `/contacto`
- **Registro:** Completar el registro en `/registro`
- **Búsqueda:** Usar el formulario de búsqueda en `/productos`

## Conceptos Técnicos Demostrados

### 1. **FastAPI**
- Decoradores de rutas (`@app.get`, `@app.post`)
- Parámetros de ruta y consulta
- Validación automática de tipos
- Formularios con `Form(...)`
- Respuestas HTML con `HTMLResponse`

### 2. **Jinja2**
- Herencia de plantillas (`{% extends %}`)
- Variables (`{{ variable }}`)
- Estructuras de control (`{% if %}`, `{% for %}`)
- Filtros (`{{ lista|length }}`)
- URLs estáticas (`{{ url_for('static', path='/style.css') }}`)

### 3. **HTML y CSS**
- Formularios HTML responsivos
- Validación HTML5 (`required`, `type="email"`)
- CSS Grid y Flexbox
- Diseño mobile-first

### 4. **Manejo de Datos**
- Almacenamiento en memoria (listas de Python)
- Validación de entrada
- Procesamiento de formularios
- Búsqueda y filtrado

## Para el Aula

### Ejercicios Sugeridos

1. **Básico:** Navegar por todas las páginas y entender el flujo
2. **Intermedio:** Analizar el código de cada endpoint
3. **Avanzado:** Modificar las plantillas y agregar nuevas funcionalidades
4. **Experto:** Añadir persistencia con base de datos

### Modificaciones Propuestas

1. **Agregar más productos** en `productos_db`
2. **Crear nuevas categorías** de productos
3. **Añadir más campos** al formulario de registro
4. **Implementar validación personalizada**
5. **Agregar paginación** a la lista de productos
6. **Crear sistema de login** básico

## Tecnologías Utilizadas

- **FastAPI** - Framework web moderno y rápido
- **Jinja2** - Motor de plantillas
- **Uvicorn** - Servidor ASGI
- **HTML5** - Estructura de páginas
- **CSS3** - Estilos y diseño responsivo
- **Python** - Lenguaje de programación

## Autor

Creado para el módulo de **Implantación de Aplicaciones Web** del ciclo **ASIR** (Administración de Sistemas Informáticos en Red).

---

¡Disfruta aprendiendo FastAPI! 🚀
