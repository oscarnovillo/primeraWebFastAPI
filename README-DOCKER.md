# Guía de uso con Docker

Este proyecto está dockerizado y listo para ejecutarse en un contenedor.

## 📋 Tipos de Dockerfile disponibles

Este proyecto incluye dos versiones de Dockerfile:

1. **Dockerfile** (Multi-stage build - Recomendado para producción)
   - Imagen optimizada y más ligera
   - Usa construcción en dos etapas
   - Elimina archivos innecesarios
   - Ejecuta con usuario no-root (más seguro)
   - Tamaño aproximado: ~150-200 MB

2. **Dockerfile.simple** (Single-stage build - Más simple)
   - Construcción en una sola etapa
   - Más fácil de entender y depurar
   - Contiene todas las herramientas de desarrollo
   - Tamaño aproximado: ~400-500 MB

## Requisitos previos

- Docker instalado en tu sistema
- Docker Compose instalado (normalmente viene con Docker Desktop)

## Cómo ejecutar el proyecto con Docker

### Opción 1: Usando Docker Compose (Recomendado)

**Con el Dockerfile multi-stage (por defecto):**
1. **Construir y ejecutar el contenedor:**
   ```bash
   docker-compose up --build
   ```

**Con el Dockerfile simple:**
1. **Modificar docker-compose.yml temporalmente o construir manualmente:**
   ```bash
   docker build -f Dockerfile.simple -t fastapi-web-simple .
   docker run -d -p 8000:8000 --name fastapi-web-simple fastapi-web-simple
   ```

2. **Ejecutar en segundo plano:**
   ```bash
   docker-compose up -d
   ```

3. **Ver los logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Detener el contenedor:**
   ```bash
   docker-compose down
   ```

### Opción 2: Usando Docker directamente

1. **Construir la imagen:**
   ```bash
   docker build -t fastapi-web . 
   ```

2. **Ejecutar el contenedor:**
   ```bash
   docker run -d -p 8000:8000 --name fastapi-web fastapi-web
   ```

3. **Ver los logs:**
   ```bash
   docker logs -f fastapi-web
   ```

4. **Detener y eliminar el contenedor:**
   ```bash
   docker stop fastapi-web
   docker rm fastapi-web
   ```

## Acceder a la aplicación

Una vez que el contenedor esté en ejecución, abre tu navegador y visita:

```
http://localhost:8000
```

## Desarrollo con hot-reload

Si deseas que los cambios en tu código se reflejen automáticamente sin reconstruir la imagen, modifica el `docker-compose.yml` para agregar el volumen del código fuente:

```yaml
volumes:
  - .:/app
```

Y cambia el comando para incluir `--reload`:

```yaml
command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Comandos útiles

- **Reconstruir la imagen:**
  ```bash
  docker-compose build
  ```

- **Ver contenedores en ejecución:**
  ```bash
  docker ps
  ```

- **Acceder al shell del contenedor:**
  ```bash
  docker-compose exec web bash
  ```

- **Limpiar imágenes y contenedores:**
  ```bash
  docker-compose down --rmi all -v
  ```
