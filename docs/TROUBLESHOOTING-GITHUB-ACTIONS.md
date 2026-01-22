# 🔧 GitHub Actions - Troubleshooting de Errores Comunes

## 🎯 Guía Rápida de Solución de Problemas

Esta guía cubre los errores más comunes al ejecutar el pipeline de CI/CD con GitHub Actions.

---

## ❌ Error: "Resource not accessible by integration"

### **Síntoma**
```
Error: Resource not accessible by integration
Step: Subir resultados de seguridad a GitHub Security
```

### **Causa**
El workflow **NO tiene permisos** para escribir en la pestaña Security de GitHub.

### **Solución** ✅

Agregar la sección `permissions` al inicio del workflow:

```yaml
name: Docker CI/CD Pipeline

on:
  push:
    branches:
      - main

# ← AGREGAR ESTO
permissions:
  contents: read           # Leer código del repositorio
  security-events: write   # Escribir en Security tab (CLAVE)
  actions: read            # Leer workflows

env:
  DOCKER_IMAGE_NAME: fastapi-web
```

### **Explicación**

Por defecto, GitHub Actions tiene permisos **limitados**. Necesitas explícitamente dar permiso para:

- `security-events: write` → Subir reportes SARIF a Security tab
- `contents: read` → Leer el código del repo
- `actions: read` → Leer información de workflows

### **Verificar que Funcionó**

Después de hacer push con los permisos agregados:

1. Ve a: **Actions** → Workflow ejecutado
2. Busca el step: **"Subir resultados de seguridad a GitHub Security"**
3. Debe mostrar: ✅ **Success**
4. Ve a: **Security** → **Code scanning**
5. Debes ver las alertas de Trivy

---

## ❌ Error: "Invalid username or password"

### **Síntoma**
```
Error: Error response from daemon: login attempt failed with status: 401 Unauthorized
Step: Login a Docker Hub
```

### **Causa**
El secret `DOCKERHUB_TOKEN` está mal configurado o es incorrecto.

### **Soluciones** ✅

#### **1. Verificar que usas Access Token (NO contraseña)**

```
❌ INCORRECTO: Usar contraseña de Docker Hub
✅ CORRECTO: Usar Access Token generado
```

**Cómo generar Access Token:**
1. https://hub.docker.com/ → Login
2. Account Settings → Security → **New Access Token**
3. Nombre: `GitHub Actions`
4. Permisos: **Read, Write, Delete**
5. **Copiar el token** (se muestra solo una vez)

#### **2. Verificar Secrets en GitHub**

1. Ve a: **Settings** → **Secrets and variables** → **Actions**
2. Verifica que existan:
   ```
   DOCKERHUB_USERNAME = tu-usuario-dockerhub
   DOCKERHUB_TOKEN = dckr_pat_xxxxx...  ← Access Token
   ```
3. Los nombres deben ser **EXACTOS** (case-sensitive)

#### **3. Regenerar Token**

Si el token fue comprometido o expiró:
1. Docker Hub → Security → **Revoke token antiguo**
2. Generar **nuevo token**
3. Actualizar secret en GitHub

---

## ❌ Error: "repository does not exist or may require 'docker login'"

### **Síntoma**
```
Error: repository usuario/fastapi-web not found
Step: Build y Push imagen Docker
```

### **Causa**
El repositorio no existe en Docker Hub o el nombre es incorrecto.

### **Soluciones** ✅

#### **Opción 1: Crear Repositorio Manualmente**

1. https://hub.docker.com/ → **Create Repository**
2. Nombre: `fastapi-web` (debe coincidir con `DOCKER_IMAGE_NAME`)
3. Visibilidad: **Public** (gratis)
4. Click **Create**

#### **Opción 2: Permitir Auto-Creación**

Docker Hub puede crear el repo automáticamente en el primer push:
- No hagas nada, el primer push lo creará
- Por defecto será **público**

#### **Opción 3: Verificar Nombre**

Asegúrate de que el nombre en el workflow coincida:

```yaml
env:
  DOCKER_IMAGE_NAME: fastapi-web  # ← Debe coincidir con repo en Docker Hub
```

---

## ❌ Error: "denied: requested access to the resource is denied"

### **Síntoma**
```
Error: denied: requested access to the resource is denied
Step: Build y Push imagen Docker
```

### **Causa**
El Access Token **NO tiene permisos de escritura** (Write).

### **Solución** ✅

Regenerar token con permisos correctos:

1. Docker Hub → Security → **Revoke token actual**
2. Crear **nuevo token**:
   - Permisos: ✅ **Read, Write, Delete** (todos)
3. Actualizar `DOCKERHUB_TOKEN` en GitHub
4. Re-ejecutar workflow

---

## ❌ Error: "failed to solve: image not found"

### **Síntoma**
```
Error: failed to solve with frontend dockerfile.v0: 
       failed to create LLB definition: dockerfile parse error
Step: Build y Push imagen Docker
```

### **Causa**
Error de sintaxis en el Dockerfile o imagen base no encontrada.

### **Soluciones** ✅

#### **1. Verificar Sintaxis del Dockerfile**

```bash
# Validar localmente
docker build -f Dockerfile.alpine -t test .
```

#### **2. Verificar Imagen Base**

```dockerfile
# En Dockerfile.alpine, verifica que existe:
FROM python:3.11-alpine

# Puedes verificar en: https://hub.docker.com/_/python/tags
```

#### **3. Revisar Errores de Tipeo**

```dockerfile
# ❌ INCORRECTO
FROM python:3.11-apline  # ← Typo: "apline"

# ✅ CORRECTO
FROM python:3.11-alpine
```

---

## ❌ Error: "Timeout waiting for connection"

### **Síntoma**
```
Error: Timeout waiting for connection to Docker daemon
Step: Configurar Docker Buildx
```

### **Causa**
Problemas de red o Docker no disponible en el runner.

### **Solución** ✅

Agregar reintentos al setup de Buildx:

```yaml
- name: Configurar Docker Buildx
  uses: docker/setup-buildx-action@v3
  with:
    install: true
    driver-opts: |
      network=host
  timeout-minutes: 5
```

---

## ❌ Error: "SBOM generation failed"

### **Síntoma**
```
Error: unable to fetch image
Step: Generar SBOM
```

### **Causa**
La imagen no se encuentra en Docker Hub (aún no fue publicada).

### **Solución** ✅

Verificar orden de steps:

```yaml
# ✅ ORDEN CORRECTO
- name: Build y Push imagen Docker
  # ... construye y sube

- name: Generar SBOM
  # ... descarga imagen (debe existir)
```

Si el problema persiste, agregar delay:

```yaml
- name: Esperar propagación de imagen
  run: sleep 10

- name: Generar SBOM
  uses: anchore/sbom-action@v0
```

---

## ❌ Error: "Trivy scan failed"

### **Síntoma**
```
Error: scan failed
Step: Escanear vulnerabilidades con Trivy
```

### **Causa**
Imagen no disponible o problemas de conectividad.

### **Solución** ✅

Hacer el escaneo **no bloqueante**:

```yaml
- name: Escanear vulnerabilidades con Trivy
  uses: aquasecurity/trivy-action@master
  continue-on-error: true  # ← No falla el workflow
  with:
    image-ref: usuario/fastapi-web:alpine
    format: 'sarif'
    output: 'trivy-results-alpine.sarif'
```

---

## ❌ Error: "workflow requires approval"

### **Síntoma**
```
Workflow run is waiting for approval
This workflow requires approval to run
```

### **Causa**
Seguridad de GitHub: workflows en forks o primeras ejecuciones requieren aprobación.

### **Solución** ✅

#### **1. Aprobar Manualmente**

1. Ve a: **Actions** → Workflow pendiente
2. Click **Review pending deployments**
3. Seleccionar el job
4. Click **Approve and run**

#### **2. Desactivar Aprobaciones (Solo Repos Privados)**

1. **Settings** → **Actions** → **General**
2. Scroll a **"Workflow permissions"**
3. Seleccionar: **Allow all actions**
4. Desmarcar: **"Require approval for all outside collaborators"**

---

## ❌ Error: "secret not found"

### **Síntoma**
```
Error: secret DOCKERHUB_USERNAME not found
Step: Login a Docker Hub
```

### **Causa**
Los secrets no están configurados o el nombre es incorrecto.

### **Solución** ✅

#### **1. Verificar Secrets Existen**

1. **Settings** → **Secrets and variables** → **Actions**
2. Debe haber:
   ```
   DOCKERHUB_USERNAME
   DOCKERHUB_TOKEN
   ```

#### **2. Verificar Nombres Exactos**

Los nombres son **case-sensitive**:

```yaml
# ❌ INCORRECTO
username: ${{ secrets.dockerhub_username }}  # Minúsculas
password: ${{ secrets.DockerHubToken }}      # CamelCase

# ✅ CORRECTO
username: ${{ secrets.DOCKERHUB_USERNAME }}  # MAYÚSCULAS
password: ${{ secrets.DOCKERHUB_TOKEN }}     # MAYÚSCULAS
```

---

## ❌ Error: "Cannot read properties of undefined"

### **Síntoma**
```
Error: Cannot read properties of undefined (reading 'tags')
Step: Build y Push imagen Docker
```

### **Causa**
El step de metadata falló o no generó outputs.

### **Solución** ✅

Verificar que el step anterior tenga `id`:

```yaml
- name: Extraer metadata (tags, labels)
  id: meta  # ← DEBE TENER ID
  uses: docker/metadata-action@v5
  # ...

- name: Build y Push imagen Docker
  uses: docker/build-push-action@v5
  with:
    tags: ${{ steps.meta.outputs.tags }}  # ← Usa el ID
```

---

## ❌ Error: "rate limit exceeded"

### **Síntoma**
```
Error: toomanyrequests: You have reached your pull rate limit
Step: Build y Push imagen Docker
```

### **Causa**
Docker Hub tiene límites de descargas (100 pulls / 6 horas para usuarios anónimos).

### **Solución** ✅

Hacer login ANTES de build:

```yaml
- name: Login a Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}

# Ahora tienes: 200 pulls / 6 horas (autenticado)

- name: Build y Push imagen Docker
  # ...
```

---

## ❌ Error: "GitHub Security disabled"

### **Síntoma**
```
Error: Code scanning is not enabled for this repository
Step: Subir resultados de seguridad a GitHub Security
```

### **Causa**
GitHub Advanced Security no está habilitado (solo en repos privados de pago).

### **Solución** ✅

#### **Para Repos Públicos:**
✅ Code scanning es **GRATIS**, solo asegúrate de tener permisos

#### **Para Repos Privados:**

**Opción 1: Habilitar GitHub Advanced Security** (De pago)
1. **Settings** → **Security** → **Code security and analysis**
2. Habilitar **GitHub Advanced Security**

**Opción 2: Hacer el repo público** (Gratis)

**Opción 3: Deshabilitar upload de SARIF** (Temporal)

```yaml
- name: Subir resultados de seguridad a GitHub Security
  if: false  # ← Deshabilita temporalmente
  uses: github/codeql-action/upload-sarif@v3
```

---

## 🔍 Debugging General

### **Ver Logs Detallados**

En GitHub Actions, activa "debug logging":

1. **Settings** → **Secrets and variables** → **Actions**
2. Crear nuevo secret:
   ```
   Name: ACTIONS_STEP_DEBUG
   Value: true
   ```
3. Re-ejecutar workflow
4. Logs mucho más detallados

### **Ejecutar Steps Localmente**

Usar `act` para simular GitHub Actions en local:

```bash
# Instalar act
# Windows: choco install act-cli

# Ejecutar workflow localmente
act -j docker-build-push --secret-file .secrets
```

### **Verificar Sintaxis del Workflow**

```bash
# Usar actionlint para validar
# Windows: choco install actionlint

actionlint .github/workflows/docker-ci-cd.yml
```

---

## 📊 Checklist de Troubleshooting

Cuando algo falla, verifica en orden:

### **1. Secrets Configurados** ✅
- [ ] `DOCKERHUB_USERNAME` existe
- [ ] `DOCKERHUB_TOKEN` existe
- [ ] Nombres EXACTOS (case-sensitive)
- [ ] Token es Access Token (NO contraseña)

### **2. Permisos del Workflow** ✅
- [ ] `permissions` agregado al workflow
- [ ] `security-events: write` presente
- [ ] Workflow aprobado (si es necesario)

### **3. Repositorio Docker Hub** ✅
- [ ] Repositorio existe en Docker Hub
- [ ] Nombre coincide con `DOCKER_IMAGE_NAME`
- [ ] Access Token tiene permisos Write

### **4. Dockerfiles** ✅
- [ ] Sintaxis correcta
- [ ] Imágenes base existen
- [ ] Archivos referenciados existen

### **5. Red y Conectividad** ✅
- [ ] GitHub Actions tiene acceso a Docker Hub
- [ ] No hay rate limits excedidos
- [ ] Timeout suficiente

---

## 🆘 Si Nada Funciona

### **1. Simplificar el Workflow**

Comentar steps problemáticos:

```yaml
# - name: Generar SBOM
#   uses: anchore/sbom-action@v0
#   # ... comentar temporalmente

# - name: Escanear vulnerabilidades con Trivy
#   # ... comentar temporalmente
```

### **2. Verificar con Docker Local**

Antes de ejecutar en GitHub Actions:

```bash
# Build local
docker build -f Dockerfile.alpine -t test:alpine .

# Push a Docker Hub (manual)
docker tag test:alpine usuario/fastapi-web:alpine
docker push usuario/fastapi-web:alpine
```

### **3. Contactar Soporte**

Si el error persiste:
- GitHub Support: https://support.github.com/
- Docker Hub Support: https://hub.docker.com/support/contact/
- GitHub Community: https://github.community/

---

## 📚 Recursos Adicionales

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Docker Build Push Action:** https://github.com/docker/build-push-action
- **Troubleshooting Guide:** https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows

---

## ✅ Resumen del Error "Resource not accessible"

**Problema:**
```
❌ Error: Resource not accessible by integration
```

**Solución:**
```yaml
# Agregar al inicio del workflow:
permissions:
  contents: read
  security-events: write  # ← CLAVE
  actions: read
```

**Verificar:**
1. Push con los cambios
2. Ejecutar workflow
3. Verificar: Security → Code scanning
4. Debe mostrar alertas de Trivy ✅

---

**Creado:** 2025-01-22  
**Actualizado:** Error "Resource not accessible" resuelto  
**Versión:** 1.0.0
