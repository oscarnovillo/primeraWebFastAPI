# 🚀 GitHub Actions CI/CD - Guía de Configuración

Esta guía te ayudará a configurar GitHub Actions para construir y publicar automáticamente tus imágenes Docker en Docker Hub.

## 📋 Requisitos Previos

1. **Cuenta de Docker Hub:** https://hub.docker.com/
2. **Repositorio de GitHub** para tu proyecto
3. **Git** instalado localmente

---

## 🔐 Paso 1: Crear Access Token en Docker Hub

1. **Inicia sesión** en Docker Hub: https://hub.docker.com/
2. Ve a **Account Settings** → **Security**
3. Click en **"New Access Token"**
4. Configuración del token:
   - **Description:** `GitHub Actions CI/CD`
   - **Access permissions:** `Read, Write, Delete`
5. **Copia el token** (solo se muestra una vez)

---

## 🔑 Paso 2: Configurar Secrets en GitHub

1. Ve a tu repositorio en GitHub
2. Click en **Settings** → **Secrets and variables** → **Actions**
3. Click en **"New repository secret"**
4. Crea estos dos secrets:

### Secret 1: DOCKERHUB_USERNAME
```
Name: DOCKERHUB_USERNAME
Value: tu-usuario-de-dockerhub
```

### Secret 2: DOCKERHUB_TOKEN
```
Name: DOCKERHUB_TOKEN
Value: [pega el token copiado del paso 1]
```

**⚠️ Importante:** Los secrets son sensibles a mayúsculas/minúsculas.

---

## 📦 Paso 3: Crear Repositorio en Docker Hub

1. **Login** en Docker Hub
2. Click en **"Create Repository"**
3. Configuración:
   - **Name:** `fastapi-web`
   - **Visibility:** `Private` (o `Public` si prefieres)
   - **Description:** `FastAPI Web Application - CI/CD`
4. Click en **"Create"**

---

## 🔧 Paso 4: Configurar el Repositorio Git

### Si aún no tienes un repositorio remoto:

```powershell
# Inicializar Git (si no está inicializado)
cd c:\tools\proyectos\primeraWebFastAPI
git init

# Añadir archivos
git add .

# Primer commit
git commit -m "Initial commit with Docker CI/CD setup"

# Crear repositorio en GitHub y seguir instrucciones
# Luego:
git remote add origin https://github.com/TU-USUARIO/TU-REPO.git
git branch -M main
git push -u origin main
```

### Si ya tienes un repositorio:

```powershell
cd c:\tools\proyectos\primeraWebFastAPI

# Añadir los nuevos archivos de CI/CD
git add .github/
git add .

# Commit
git commit -m "Add GitHub Actions CI/CD pipeline"

# Push a main (esto activará el workflow)
git push origin main
```

---

## 🎯 Paso 5: Verificar el Pipeline

1. Ve a tu repositorio en GitHub
2. Click en la pestaña **"Actions"**
3. Deberías ver el workflow **"Docker CI/CD Pipeline"** en ejecución
4. Click en el workflow para ver el progreso

---

## 📊 ¿Qué hace el Pipeline?

### 🟢 **Job 1: Build and Test**
- Checkout del código
- Configura Python 3.11
- Instala dependencias
- Ejecuta tests (si existen)

### 🔵 **Job 2: Docker Build and Push**
- Construye **2 imágenes** en paralelo:
  - `Dockerfile` → `fastapi-web:optimized`
  - `Dockerfile.alpine` → `fastapi-web:alpine`
- Genera múltiples tags:
  - `optimized` / `alpine` (latest)
  - `optimized-abc1234` / `alpine-abc1234` (SHA del commit)
  - `optimized-20260122` / `alpine-20260122` (fecha)
  - `v1.0.0-optimized` / `v1.0.0-alpine` (si es un tag)
- Usa **caché de GitHub** para builds más rápidos
- Builds **multi-arquitectura**: AMD64 y ARM64
- Sube las imágenes a Docker Hub

### 🟡 **Job 3: Security**
- Genera SBOM (Software Bill of Materials)
- Escanea vulnerabilidades con Trivy
- Sube resultados a GitHub Security

### 🟣 **Job 4: Release (solo para tags)**
- Crea release en GitHub con notas automáticas
- Incluye instrucciones de uso

---

## 🏷️ Uso con Tags (Versionado)

Para crear una versión específica:

```powershell
# Crear y push un tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

Esto creará imágenes adicionales:
- `fastapi-web:v1.0.0-optimized`
- `fastapi-web:v1.0.0-alpine`
- `fastapi-web:1.0-optimized`
- `fastapi-web:1.0-alpine`

---

## 🐳 Usar las Imágenes

### Desde Docker Hub:

```powershell
# Pull de la imagen
docker pull TU-USUARIO/fastapi-web:alpine

# O la versión optimizada
docker pull TU-USUARIO/fastapi-web:optimized

# Ejecutar
docker run -d -p 8000:8000 TU-USUARIO/fastapi-web:alpine
```

### Usar versión específica:

```powershell
docker pull TU-USUARIO/fastapi-web:v1.0.0-alpine
docker run -d -p 8000:8000 TU-USUARIO/fastapi-web:v1.0.0-alpine
```

---

## 🔍 Verificar el Estado del Pipeline

### En GitHub:
1. **Actions** tab → Ver workflows
2. **Pull Requests** → Ver checks automáticos
3. **Security** tab → Ver escaneos de vulnerabilidades

### En Docker Hub:
1. Ve a tu repositorio
2. Verás todas las imágenes y tags publicados
3. Revisa la fecha de última actualización

---

## 🛡️ Seguridad

El pipeline incluye:

✅ **Escaneo de vulnerabilidades** (Trivy)  
✅ **SBOM generado** (lista de componentes)  
✅ **Resultados en GitHub Security**  
✅ **Secrets encriptados** (nunca expuestos)  
✅ **Multi-arquitectura** (AMD64 + ARM64)  

---

## ⚡ Optimizaciones del Pipeline

1. **Caché de GitHub Actions:** Builds 5-10x más rápidos
2. **Builds en paralelo:** Optimized y Alpine simultáneamente
3. **Matrix strategy:** Fácil añadir más versiones
4. **Buildx:** Soporte multi-plataforma
5. **Metadata action:** Tags automáticos inteligentes

---

## 🔧 Personalización

### Cambiar el nombre de la imagen:

Edita `.github/workflows/docker-ci-cd.yml`:

```yaml
env:
  DOCKER_IMAGE_NAME: mi-app  # Cambia esto
```

### Añadir más Dockerfiles:

```yaml
strategy:
  matrix:
    dockerfile: [Dockerfile, Dockerfile.alpine, Dockerfile.simple]
    include:
      - dockerfile: Dockerfile
        tag-suffix: optimized
      - dockerfile: Dockerfile.alpine
        tag-suffix: alpine
      - dockerfile: Dockerfile.simple
        tag-suffix: dev
```

### Ejecutar en otras ramas:

```yaml
on:
  push:
    branches:
      - main
      - develop  # Añade más ramas
      - staging
```

---

## 🐛 Troubleshooting

### Error: "Invalid username or password"
- ✅ Verifica que `DOCKERHUB_USERNAME` sea correcto
- ✅ Verifica que `DOCKERHUB_TOKEN` sea un Access Token válido
- ✅ NO uses tu contraseña de Docker Hub, usa el Token

### Error: "repository does not exist"
- ✅ Crea el repositorio en Docker Hub primero
- ✅ Verifica que el nombre coincida exactamente

### Error: "permission denied"
- ✅ Verifica que el token tenga permisos de Write
- ✅ Regenera el token si es necesario

### Builds lentos
- ✅ El primer build será lento
- ✅ Los siguientes usarán caché (mucho más rápidos)
- ✅ Caché se mantiene ~7 días

---

## 📈 Workflow Completo

```
[Commit a main] 
    ↓
[GitHub Actions detecta push]
    ↓
[Job 1: Build and Test]
    ├─ Setup Python
    ├─ Install deps
    └─ Run tests
    ↓
[Job 2: Docker Build (Parallel)]
    ├─ Build Dockerfile → optimized
    └─ Build Dockerfile.alpine → alpine
    ↓
[Login a Docker Hub]
    ↓
[Push imágenes]
    ├─ user/fastapi-web:optimized
    ├─ user/fastapi-web:optimized-abc1234
    ├─ user/fastapi-web:alpine
    └─ user/fastapi-web:alpine-abc1234
    ↓
[Security Scan]
    ↓
[✅ Success!]
```

---

## 📚 Recursos Adicionales

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Docker Hub](https://hub.docker.com/)
- [Trivy Vulnerability Scanner](https://github.com/aquasecurity/trivy)

---

## ✅ Checklist de Setup

- [ ] Token de Docker Hub creado
- [ ] Secrets configurados en GitHub
  - [ ] `DOCKERHUB_USERNAME`
  - [ ] `DOCKERHUB_TOKEN`
- [ ] Repositorio creado en Docker Hub
- [ ] Archivo `.github/workflows/docker-ci-cd.yml` añadido
- [ ] Commit y push a rama `main`
- [ ] Pipeline ejecutándose correctamente
- [ ] Imágenes visibles en Docker Hub

---

**🎉 ¡Listo! Ahora cada commit a `main` construirá y publicará automáticamente tus imágenes Docker!**
