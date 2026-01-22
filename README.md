# Mi Primera Web FastAPI 🚀

[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)

## Descripción

Esta es una aplicación web educativa creada con **FastAPI** y **Jinja2** para enseñar los conceptos básicos del desarrollo web backend. Incluye ejemplos prácticos de:

- 🔗 **Parámetros GET** (query parameters y path parameters)
- 📝 **Formularios POST** (simples y complejos)
- 🎨 **Sistema de plantillas Jinja2**
- 📦 **Manejo de datos en memoria**
- 🎯 **Validación de formularios**
- 🌐 **Navegación entre páginas**
- 🐳 **Docker & CI/CD** (completamente dockerizado con GitHub Actions)

## 🚀 Inicio Rápido

### Opción 1: Docker (Recomendado)

```powershell
# Ejecutar con Docker (más fácil)
docker run -d -p 8000:8000 TU-USUARIO/fastapi-web:alpine

# O con docker-compose
docker-compose up -d
```

**¡Listo!** Abre http://localhost:8000 en tu navegador.

📖 **Documentación completa:** [README-DOCKER.md](docs/README-DOCKER.md)

### Opción 2: Python Local

```powershell
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python main.py
```

## 📚 Documentación Completa

| Documento | Descripción |
|-----------|-------------|
| **[INICIO-RAPIDO-CICD.md](docs/INICIO-RAPIDO-CICD.md)** | 🚀 Activar CI/CD en 5 minutos |
| **[README-DOCKER.md](docs/README-DOCKER.md)** | 🐳 Guía completa de Docker |
| **[RESUMEN-EJECUTIVO.md](docs/RESUMEN-EJECUTIVO.md)** | 📊 Estado del proyecto y checklist |
| **[TRIVY-GUIA-RAPIDA.md](docs/TRIVY-GUIA-RAPIDA.md)** | 🛡️ Ver resultados de seguridad |
| **[EJEMPLOS-USO.md](docs/EJEMPLOS-USO.md)** | 💡 Ejemplos prácticos (K8s, AWS, Azure, etc.) |
| **[OPTIMIZACIONES-DOCKER.md](docs/OPTIMIZACIONES-DOCKER.md)** | ⚡ Técnicas de optimización |
| **[REPORTE-COMPARATIVA-DOCKER.md](docs/REPORTE-COMPARATIVA-DOCKER.md)** | 📈 Benchmarks y comparativas |

## 🎯 Características

### ✅ Desarrollo Web
- Sistema completo de rutas y plantillas
- Formularios con validación
- Búsqueda y filtrado de datos
- Diseño responsive

### ✅ Docker & Contenedores
- 3 variantes de Dockerfile (Simple, Optimized, Alpine)
- Multi-stage builds optimizados
- Imágenes desde 109 MB
- Docker Compose para desarrollo local

### ✅ CI/CD Automatizado
- GitHub Actions pipeline completo
- Build y push automático a Docker Hub
- Multi-arquitectura (AMD64 + ARM64)
- Escaneo de seguridad con Trivy
- Tags automáticos (SHA, fecha, versión)

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
│
├── 🐳 Docker & CI/CD
├── Dockerfile                  # Multi-stage optimizado (201 MB)
├── Dockerfile.alpine           # Ultra-ligero Alpine (109 MB)
├── Dockerfile.simple           # Baseline sin optimización (227 MB)
├── docker-compose.yml          # Orquestación local
├── .dockerignore               # Optimización de contexto
├── validate-cicd.ps1           # Script de validación
├── .github/
│   ├── workflows/
│   │   └── docker-ci-cd.yml    # Pipeline de CI/CD
│   └── GITHUB-ACTIONS-SETUP.md # Guía de configuración
│
├── 📚 docs/                    # Toda la documentación
│   ├── README.md               # Índice de documentación
│   ├── INICIO-RAPIDO-CICD.md   # Setup rápido CI/CD
│   ├── README-DOCKER.md        # Guía de Docker
│   ├── RESUMEN-EJECUTIVO.md    # Estado del proyecto
│   ├── TRIVY-GUIA-RAPIDA.md    # Seguridad (guía rápida)
│   ├── TRIVY-EXPLICACION.md    # Seguridad (detallada)
│   ├── EJEMPLOS-USO.md         # Ejemplos de deployment
│   ├── OPTIMIZACIONES-DOCKER.md     # Técnicas de optimización
│   ├── REPORTE-COMPARATIVA-DOCKER.md # Benchmarks
│   └── CHECKLIST-PRE-PUSH.md   # Validación pre-push
│
├── static/
│   └── style.css              # Estilos CSS
│
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

### Backend & Framework
- **FastAPI** - Framework web moderno y rápido
- **Jinja2** - Motor de plantillas
- **Uvicorn** - Servidor ASGI
- **Python 3.11+** - Lenguaje de programación

### Frontend
- **HTML5** - Estructura de páginas
- **CSS3** - Estilos y diseño responsivo

### DevOps & Deployment
- **Docker** - Containerización
- **Docker Compose** - Orquestación local
- **GitHub Actions** - CI/CD automatizado
- **Trivy** - Escaneo de vulnerabilidades
- **Multi-arch builds** - AMD64 + ARM64

## 🐳 Comparativa de Imágenes Docker

| Variante | Tamaño | Build Time | Uso Recomendado |
|----------|--------|------------|-----------------|
| **Alpine** | 109 MB | <1s (cached) | ✅ Producción |
| **Optimized** | 201 MB | ~5s (cached) | Desarrollo |
| **Simple** | 227 MB | ~10s | Testing/Baseline |

**Reducción:** 52% vs imagen simple (Alpine)

## 🚀 Despliegue en Producción

### Docker Hub (Automático)
Cada push a `main` construye y publica automáticamente en Docker Hub:

```bash
docker pull TU-USUARIO/fastapi-web:alpine
docker run -d -p 80:8000 TU-USUARIO/fastapi-web:alpine
```

### Kubernetes
```bash
kubectl apply -f k8s-deployment.yaml
```

### AWS ECS, Azure, Google Cloud Run
Ver ejemplos completos en [EJEMPLOS-USO.md](docs/EJEMPLOS-USO.md)

## 📊 CI/CD Pipeline

El proyecto incluye un pipeline completo de GitHub Actions que:

1. ✅ Ejecuta tests automáticos
2. ✅ Construye 2 imágenes Docker en paralelo
3. ✅ Publica en Docker Hub con tags automáticos
4. ✅ Escanea vulnerabilidades con Trivy
5. ✅ Genera SBOM (Software Bill of Materials)
6. ✅ Soporta multi-arquitectura (AMD64 + ARM64)

**Configuración:** Ver [INICIO-RAPIDO-CICD.md](docs/INICIO-RAPIDO-CICD.md)

## Autor

Creado para el módulo de **Implantación de Aplicaciones Web** del ciclo **ASIR** (Administración de Sistemas Informáticos en Red).

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

---

## 🎓 Para el Aula - Quick Links

- **📖 Guía básica:** Este README
- **🐳 Usar Docker:** [README-DOCKER.md](docs/README-DOCKER.md)
- **🚀 Activar CI/CD:** [INICIO-RAPIDO-CICD.md](docs/INICIO-RAPIDO-CICD.md)
- **💻 Ejemplos de deployment:** [EJEMPLOS-USO.md](docs/EJEMPLOS-USO.md)
- **📊 Ver benchmarks:** [REPORTE-COMPARATIVA-DOCKER.md](docs/REPORTE-COMPARATIVA-DOCKER.md)

---

¡Disfruta aprendiendo FastAPI con Docker y CI/CD! 🚀🐳
