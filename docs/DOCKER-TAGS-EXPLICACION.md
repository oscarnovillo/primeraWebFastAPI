# 🏷️ Sistema de Tags de Docker - Explicación Completa

## 📋 Tabla de Contenidos
1. [¿Qué son los tags de Docker?](#qué-son-los-tags-de-docker)
2. [Sistema de tags en tu pipeline](#sistema-de-tags-en-tu-pipeline)
3. [Tipos de tags explicados](#tipos-de-tags-explicados)
4. [¿Por qué NO hay tag `latest`?](#por-qué-no-hay-tag-latest)
5. [Ejemplos prácticos](#ejemplos-prácticos)
6. [Mejores prácticas](#mejores-prácticas)

---

## 🎯 ¿Qué son los tags de Docker?

Un **tag** es una etiqueta que identifica una versión específica de una imagen Docker:

```bash
nombre-imagen:tag
usuario/fastapi-web:alpine     # tag = "alpine"
usuario/fastapi-web:v1.2.3     # tag = "v1.2.3"
usuario/fastapi-web:latest     # tag = "latest"
```

### Función de los tags:
- ✅ **Versionado**: Identificar versiones específicas
- ✅ **Trazabilidad**: Saber exactamente qué código está en producción
- ✅ **Rollback**: Volver a versiones anteriores fácilmente
- ✅ **Entornos**: Diferentes tags para dev/staging/prod

---

## 🔧 Sistema de Tags en tu Pipeline

En tu archivo `docker-ci-cd.yml`, la sección de tags se ve así:

```yaml
tags: |
  type=raw,value=${{ matrix.tag-suffix }}
  type=raw,value=${{ matrix.tag-suffix }}-{{sha}}
  type=raw,value=${{ matrix.tag-suffix }}-{{date 'YYYYMMDD'}}
  type=semver,pattern={{version}},suffix=-${{ matrix.tag-suffix }}
  type=semver,pattern={{major}}.{{minor}},suffix=-${{ matrix.tag-suffix }}
```

Esto utiliza la acción `docker/metadata-action` que **genera automáticamente múltiples tags** según las reglas definidas.

---

## 📚 Tipos de Tags Explicados

### 1️⃣ `type=raw` - Tags Estáticos/Personalizados

**¿Qué es?**  
Un tag "crudo" que defines manualmente. Se genera siempre, sin importar el evento.

**Sintaxis:**
```yaml
type=raw,value=mi-tag-personalizado
```

#### **En tu pipeline:**

```yaml
type=raw,value=${{ matrix.tag-suffix }}
```
- **Genera:** `alpine` o `optimized` (según el Dockerfile)
- **Cuándo:** En **cada push** a main
- **Uso:** Tag principal para cada variante

```yaml
type=raw,value=${{ matrix.tag-suffix }}-{{sha}}
```
- **Genera:** `alpine-a1b2c3d` (con hash del commit)
- **Cuándo:** En **cada push**
- **Uso:** Trazabilidad exacta del código

```yaml
type=raw,value=${{ matrix.tag-suffix }}-{{date 'YYYYMMDD'}}
```
- **Genera:** `alpine-20260122` (con fecha)
- **Cuándo:** En **cada push**
- **Uso:** Identificar versiones por fecha

---

### 2️⃣ `type=semver` - Semantic Versioning

**¿Qué es?**  
Tags basados en **versiones semánticas** (SemVer): `v1.2.3` → Mayor.Menor.Patch

**Sintaxis:**
```yaml
type=semver,pattern={{version}}
```

**⚠️ IMPORTANTE:** Solo se genera cuando haces push de un **tag de Git** con formato `v*.*.*`

#### **En tu pipeline:**

```yaml
type=semver,pattern={{version}},suffix=-${{ matrix.tag-suffix }}
```
- **Genera:** `1.2.3-alpine`, `1.2.3-optimized`
- **Cuándo:** Solo al hacer `git push origin v1.2.3`
- **Uso:** Versiones completas

```yaml
type=semver,pattern={{major}}.{{minor}},suffix=-${{ matrix.tag-suffix }}
```
- **Genera:** `1.2-alpine`, `1.2-optimized`
- **Cuándo:** Solo al hacer `git push origin v1.2.3`
- **Uso:** Versión mayor.menor (sin patch)

---

## 🚫 ¿Por qué NO hay tag `latest`?

### Razones para NO usar `latest` automáticamente:

#### 1️⃣ **Ambigüedad en Producción**
```bash
# ❌ MAL: No sabes qué versión estás usando
docker pull usuario/fastapi-web:latest

# ✅ BIEN: Versión explícita
docker pull usuario/fastapi-web:alpine
docker pull usuario/fastapi-web:1.2.3-alpine
```

#### 2️⃣ **Problemas de Reproducibilidad**
```yaml
# ❌ MAL: Mañana "latest" podría ser diferente
image: usuario/fastapi-web:latest

# ✅ BIEN: Siempre usas la misma versión
image: usuario/fastapi-web:alpine-20260122
```

#### 3️⃣ **Múltiples Variantes**
Tu proyecto tiene 2 Dockerfiles (alpine, optimized). ¿Cuál debería ser `latest`?
- `latest` → ¿alpine o optimized?
- Mejor: `alpine` y `optimized` como tags principales

#### 4️⃣ **Mejores Prácticas de la Industria**
- Google Cloud: No recomienda `latest`
- Kubernetes: Requiere tags específicos
- Docker Inc.: Sugiere tags inmutables

### ✅ Si AÚN quieres agregar `latest`:

```yaml
tags: |
  type=raw,value=latest,enable={{is_default_branch}}  # Solo en main
  type=raw,value=${{ matrix.tag-suffix }}
  type=raw,value=${{ matrix.tag-suffix }}-{{sha}}
  # ...resto de tags...
```

**Nota:** Esto crearía `latest` que apunta a la última imagen (pero se sobrescribiría en cada build).

---

## 📸 Ejemplos Prácticos

### Ejemplo 1: Push a `main` (sin tag de Git)

```bash
git push origin main
```

**Tags generados para Dockerfile.alpine:**
```
usuario/fastapi-web:alpine
usuario/fastapi-web:alpine-a1b2c3d       # SHA del commit
usuario/fastapi-web:alpine-20260122      # Fecha del build
```

**Tags generados para Dockerfile (optimized):**
```
usuario/fastapi-web:optimized
usuario/fastapi-web:optimized-a1b2c3d
usuario/fastapi-web:optimized-20260122
```

**Tags de tipo `semver`:** ❌ NO se generan (no hay tag de Git)

---

### Ejemplo 2: Release con tag de Git `v1.5.2`

```bash
git tag v1.5.2
git push origin v1.5.2
```

**Tags generados para Dockerfile.alpine:**
```
usuario/fastapi-web:alpine
usuario/fastapi-web:alpine-a1b2c3d
usuario/fastapi-web:alpine-20260122
usuario/fastapi-web:1.5.2-alpine        # ← SemVer completo
usuario/fastapi-web:1.5-alpine          # ← SemVer mayor.menor
```

**Tags generados para Dockerfile (optimized):**
```
usuario/fastapi-web:optimized
usuario/fastapi-web:optimized-a1b2c3d
usuario/fastapi-web:optimized-20260122
usuario/fastapi-web:1.5.2-optimized
usuario/fastapi-web:1.5-optimized
```

**Total:** 10 tags (5 por variante)

---

## 🎯 Casos de Uso por Tag

| Tag | Cuándo usarlo | Ejemplo |
|-----|---------------|---------|
| `alpine` | Desarrollo local, última versión Alpine | `docker pull usuario/fastapi-web:alpine` |
| `optimized` | Producción, última versión Debian | `docker pull usuario/fastapi-web:optimized` |
| `alpine-a1b2c3d` | Debug de issue específico | `docker pull usuario/fastapi-web:alpine-a1b2c3d` |
| `alpine-20260122` | Rollback a versión de fecha | `docker pull usuario/fastapi-web:alpine-20260122` |
| `1.5.2-alpine` | Producción con versionado | `docker pull usuario/fastapi-web:1.5.2-alpine` |
| `1.5-alpine` | Últimos patches de v1.5 | `docker pull usuario/fastapi-web:1.5-alpine` |

---

## 🏆 Mejores Prácticas

### ✅ DO (Hacer):

```yaml
# 1. Usa tags específicos en producción
production:
  image: usuario/fastapi-web:1.5.2-alpine

# 2. Usa tags de fecha para rollback
staging:
  image: usuario/fastapi-web:alpine-20260122

# 3. Usa SHA para debugging
debug:
  image: usuario/fastapi-web:alpine-a1b2c3d
```

### ❌ DON'T (No hacer):

```yaml
# 1. No uses "latest" en producción
production:
  image: usuario/fastapi-web:latest  # ❌ Peligroso

# 2. No omitas el tag (default = latest)
production:
  image: usuario/fastapi-web  # ❌ Implícitamente usa :latest

# 3. No uses tags mutables en CI/CD
production:
  image: usuario/fastapi-web:alpine  # ⚠️ Cambia con cada build
```

---

## 🔄 Flujo de Trabajo Recomendado

### 1️⃣ Desarrollo (main branch)
```bash
# Push a main → tags automáticos
git push origin main

# Usar en desarrollo
docker pull usuario/fastapi-web:alpine
```

### 2️⃣ Release (con tag)
```bash
# Crear release
git tag -a v1.5.2 -m "Release 1.5.2"
git push origin v1.5.2

# Esperar a que CI/CD publique
# Luego usar en producción
docker pull usuario/fastapi-web:1.5.2-alpine
```

### 3️⃣ Hotfix urgente
```bash
# Rollback a versión anterior por SHA
docker pull usuario/fastapi-web:alpine-a1b2c3d

# O por fecha
docker pull usuario/fastapi-web:alpine-20260121
```

---

## 📊 Comparativa de Estrategias de Tags

| Estrategia | Ventajas | Desventajas | Cuándo usar |
|------------|----------|-------------|-------------|
| **Solo `latest`** | Simple | No reproducible | ❌ Nunca en producción |
| **SemVer puro** | Estándar de la industria | Requiere disciplina | ✅ Proyectos maduros |
| **SHA commits** | Trazabilidad exacta | Difícil de leer | ✅ Debugging |
| **Fechas** | Fácil de recordar | Varios builds por día | ✅ Deploys diarios |
| **Mixto (tu config)** | Flexibilidad máxima | Más tags | ✅✅ **RECOMENDADO** |

---

## 🔍 Verificar tus Tags en Docker Hub

```bash
# Ver todos los tags disponibles (requiere jq)
curl -s https://hub.docker.com/v2/repositories/USUARIO/fastapi-web/tags/ | jq -r '.results[].name'

# Ejemplo de salida:
# alpine
# alpine-a1b2c3d
# alpine-20260122
# optimized
# optimized-a1b2c3d
# optimized-20260122
```

---

## 🎓 Resumen Ejecutivo

### Tu configuración actual:

✅ **NO crea tag `latest`** → Buena práctica para producción  
✅ **Tags principales:** `alpine`, `optimized`  
✅ **Trazabilidad:** Tags con SHA y fecha  
✅ **Versionado:** SemVer solo en releases  
✅ **Múltiples arquitecturas:** AMD64 + ARM64  

### Resultado:
- **3 tags por build normal** (push a main)
- **5 tags por release** (push de tag v*.*.*)
- **Trazabilidad completa** sin perder simplicidad

---

## 📚 Referencias

- [Docker Metadata Action](https://github.com/docker/metadata-action)
- [Semantic Versioning](https://semver.org/)
- [Docker Tags Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Google Cloud: Container Image Tagging](https://cloud.google.com/architecture/best-practices-for-building-containers#tagging)

---

## 🚀 Siguiente Paso

### Crear tu primera release con SemVer:

```bash
# Crear tag localmente
git tag -a v1.0.0 -m "Primera release con CI/CD"

# Enviar a GitHub (activa el pipeline)
git push origin v1.0.0

# Ver en GitHub Actions
# Verificar en Docker Hub: usuario/fastapi-web:1.0.0-alpine
```

### Auto-updates con Watchtower/Kubernetes:

Si quieres que tus contenedores se **actualicen automáticamente** cuando publiques nuevas versiones:

📖 **Lee:** [AUTO-UPDATES-GUIA.md](AUTO-UPDATES-GUIA.md)

- ✅ Watchtower para Docker Compose
- ✅ Kubernetes con ImagePullPolicy
- ✅ Flux CD (GitOps)
- ✅ Estrategias por entorno (dev/staging/prod)

---

**Actualizado:** 22 de enero de 2026  
**Proyecto:** primeraWebFastAPI  
**Pipeline:** docker-ci-cd.yml
