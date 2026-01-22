# 🛡️ Trivy Security Scanner - Guía Completa

## ¿Qué es Trivy?

**Trivy** es un escáner de vulnerabilidades de código abierto desarrollado por Aqua Security que analiza:

- 🐳 **Imágenes Docker** - CVEs en paquetes del sistema
- 📦 **Dependencias** - Vulnerabilidades en Python, Node.js, Go, etc.
- 📋 **Archivos de configuración** - IaC (Kubernetes, Terraform)
- 🔐 **Secretos expuestos** - API keys, passwords en el código
- 📜 **Licencias** - Identificación de licencias problemáticas

---

## 🔄 Flujo en el Pipeline CI/CD

### Paso a Paso en tu Workflow

```yaml
# 1. Construir y subir imagen
- name: Build y Push imagen Docker
  uses: docker/build-push-action@v5
  # ... imagen se sube a Docker Hub

# 2. Escanear la imagen publicada
- name: Escanear vulnerabilidades con Trivy
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: usuario/fastapi-web:alpine  # Imagen a escanear
    format: 'sarif'                         # Formato compatible con GitHub
    output: 'trivy-results-alpine.sarif'    # Archivo de resultados

# 3. Subir resultados a GitHub Security
- name: Subir resultados de seguridad
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: 'trivy-results-alpine.sarif'
```

### ¿Qué Escanea?

**En tu imagen Docker Alpine (109 MB):**
```
Escaneando:
✅ Alpine Linux base (apk packages)
✅ Python 3.11 binario
✅ Dependencias de requirements.txt:
   - fastapi==0.109.0
   - uvicorn[standard]==0.27.0
   - jinja2==3.1.3
   - python-multipart==0.0.6
✅ Librerías del sistema (openssl, musl, etc.)
```

**En tu imagen Optimized (201 MB):**
```
Escaneando:
✅ Debian slim base (apt packages)
✅ Python 3.11
✅ Mismas dependencias Python
✅ Librerías del sistema (glibc, libssl, etc.)
```

---

## 📍 Dónde Ver los Resultados

### Opción 1: GitHub Security Tab ⭐ (Recomendado)

**Paso a Paso:**

1. **Ve a tu repositorio en GitHub**
   ```
   https://github.com/TU-USUARIO/primeraWebFastAPI
   ```

2. **Click en la pestaña "Security"** (junto a Settings)

3. **Sidebar izquierdo → "Code scanning"**
   ```
   Security
   ├── Overview
   ├── Vulnerability alerts
   │   ├── Dependabot alerts
   │   └── Code scanning alerts  ← AQUÍ
   └── Security advisories
   ```

4. **Ver alertas por severidad:**
   - 🔴 **Critical** - Vulnerabilidades críticas (score 9.0-10.0)
   - 🟠 **High** - Alta severidad (score 7.0-8.9)
   - 🟡 **Medium** - Media severidad (score 4.0-6.9)
   - 🟢 **Low** - Baja severidad (score 0.1-3.9)

**Ejemplo de alerta:**
```
┌─────────────────────────────────────────────────────────────┐
│ 🔴 CRITICAL                                                 │
│ CVE-2024-6345: Memory corruption in libssl                 │
├─────────────────────────────────────────────────────────────┤
│ Severity:        9.8 (Critical)                             │
│ Package:         libssl3                                    │
│ Installed:       3.0.1-1                                    │
│ Fixed in:        3.0.2-1                                    │
│ Detected in:     Dockerfile.alpine                          │
│                                                             │
│ Description:                                                │
│ A memory corruption vulnerability in OpenSSL can lead to    │
│ remote code execution when parsing malformed certificates.  │
│                                                             │
│ Remediation:                                                │
│ Update the Alpine base image to use a newer version that   │
│ includes the patched libssl package.                        │
│                                                             │
│ References:                                                 │
│ - https://nvd.nist.gov/vuln/detail/CVE-2024-6345          │
│ - https://security.alpinelinux.org/vuln/CVE-2024-6345     │
└─────────────────────────────────────────────────────────────┘
```

### Opción 2: GitHub Actions Logs

**Paso a Paso:**

1. **Ve a la pestaña "Actions"**
   ```
   https://github.com/TU-USUARIO/primeraWebFastAPI/actions
   ```

2. **Selecciona el workflow más reciente**
   - Click en "Docker CI/CD Pipeline"

3. **Click en el job "Docker Build and Push"**

4. **Expandir el step "Escanear vulnerabilidades con Trivy"**

**Verás algo como:**
```
Run aquasecurity/trivy-action@master
  with:
    image-ref: usuario/fastapi-web:alpine
    format: sarif
    output: trivy-results-alpine.sarif

2025-01-22T10:30:45.123Z  INFO  Vulnerability scanning is enabled
2025-01-22T10:30:45.456Z  INFO  Detecting Alpine Linux vulnerabilities...
2025-01-22T10:30:46.789Z  INFO  Number of language-specific files: 1
2025-01-22T10:30:46.790Z  INFO  Detecting Python vulnerabilities...

usuario/fastapi-web:alpine (alpine 3.19.1)
==========================================
Total: 15 (CRITICAL: 0, HIGH: 2, MEDIUM: 8, LOW: 5)

┌─────────────┬────────────────┬──────────┬─────────────┬───────────────┬───────────────────┐
│   Library   │ Vulnerability  │ Severity │  Installed  │ Fixed Version │      Title        │
├─────────────┼────────────────┼──────────┼─────────────┼───────────────┼───────────────────┤
│ openssl     │ CVE-2024-1234  │ HIGH     │ 3.1.4-r5    │ 3.1.5-r0      │ Memory corruption │
│ python3.11  │ CVE-2023-5678  │ MEDIUM   │ 3.11.6-r0   │ 3.11.8-r0     │ Path traversal    │
└─────────────┴────────────────┴──────────┴─────────────┴───────────────┴───────────────────┘

Python (python-pkg)
===================
Total: 3 (CRITICAL: 0, HIGH: 0, MEDIUM: 2, LOW: 1)

┌─────────────┬────────────────┬──────────┬─────────────┬───────────────┬───────────────────┐
│   Library   │ Vulnerability  │ Severity │  Installed  │ Fixed Version │      Title        │
├─────────────┼────────────────┼──────────┼─────────────┼───────────────┼───────────────────┤
│ fastapi     │ CVE-2024-9999  │ MEDIUM   │ 0.109.0     │ 0.110.0       │ XSS vulnerability │
│ jinja2      │ CVE-2023-1111  │ LOW      │ 3.1.3       │ 3.1.4         │ DoS via templates │
└─────────────┴────────────────┴──────────┴─────────────┴───────────────┴───────────────────┘
```

### Opción 3: Descargar Archivo SARIF

Los archivos SARIF se guardan como artifacts:

1. **Actions → Workflow → Summary**
2. **Scroll down → "Artifacts"**
3. **Descargar `trivy-results-alpine.sarif`**

**Formato SARIF (JSON):**
```json
{
  "version": "2.1.0",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "Trivy",
          "version": "0.48.0"
        }
      },
      "results": [
        {
          "ruleId": "CVE-2024-1234",
          "level": "error",
          "message": {
            "text": "Memory corruption in openssl"
          },
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": {
                  "uri": "Dockerfile.alpine"
                }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

---

## 🎯 ¿Por Qué es Importante?

### Beneficios del Escaneo Automático

1. **🔒 Seguridad Proactiva**
   - Detecta vulnerabilidades ANTES de desplegar
   - Evita brechas de seguridad conocidas
   - Cumple con estándares de compliance

2. **📊 Visibilidad Centralizada**
   - Dashboard en GitHub Security
   - Histórico de vulnerabilidades
   - Métricas de mejora

3. **⚡ Automatización**
   - Se ejecuta en CADA build
   - No requiere intervención manual
   - Notificaciones automáticas

4. **💰 Gratuito**
   - Trivy es open-source
   - GitHub Security es gratis para repos públicos
   - No costo adicional

---

## 🛠️ Interpretando los Resultados

### Niveles de Severidad

| Severidad | Score CVSS | Acción Recomendada |
|-----------|------------|-------------------|
| 🔴 **CRITICAL** | 9.0 - 10.0 | ⚠️ Arreglar INMEDIATAMENTE |
| 🟠 **HIGH** | 7.0 - 8.9 | ⏰ Arreglar en <7 días |
| 🟡 **MEDIUM** | 4.0 - 6.9 | 📅 Arreglar en siguiente sprint |
| 🟢 **LOW** | 0.1 - 3.9 | 📌 Arreglar cuando sea posible |

### Ejemplo de Decisiones

**Escenario 1: 0 Vulnerabilidades**
```
✅ TODO BIEN
→ Desplegar a producción sin problemas
```

**Escenario 2: 2 MEDIUM, 5 LOW**
```
⚠️ REVISAR
→ Revisar las MEDIUM
→ Si no hay exploit público conocido, desplegar
→ Programar fix para siguiente iteración
```

**Escenario 3: 1 CRITICAL**
```
🚨 BLOQUEAR DEPLOY
→ NO desplegar a producción
→ Actualizar imagen base o dependencia
→ Re-escanear hasta resolver
```

---

## 🔧 Cómo Arreglar Vulnerabilidades

### Opción 1: Actualizar Imagen Base

Si el problema está en Alpine/Debian:

```dockerfile
# Antes (vulnerable)
FROM python:3.11-alpine3.19

# Después (actualizado)
FROM python:3.11-alpine3.20  # Versión más reciente
```

### Opción 2: Actualizar Dependencias Python

Si el problema está en requirements.txt:

```txt
# Antes (vulnerable)
fastapi==0.109.0

# Después (patcheado)
fastapi>=0.110.0  # Versión sin CVE
```

### Opción 3: Rebuild de Imagen

A veces solo reconstruir soluciona:

```bash
# Pull la imagen base más reciente
docker pull python:3.11-alpine

# Rebuild sin cache
docker build --no-cache -f Dockerfile.alpine -t test .
```

---

## 📈 Monitoreo Continuo

### Dashboard de Seguridad

**GitHub te muestra:**

```
Security Overview
├── 📊 Total vulnerabilities: 15
├── 🔴 Critical: 0
├── 🟠 High: 2
├── 🟡 Medium: 8
├── 🟢 Low: 5
└── 📈 Trend: ↓ -3 vs last week
```

### Alertas Automáticas

Si hay vulnerabilidades **CRITICAL** o **HIGH**, GitHub puede:

1. ✅ Enviar email a los maintainers
2. ✅ Crear issues automáticas
3. ✅ Bloquear PRs (si está configurado)
4. ✅ Generar reportes PDF

---

## 🎓 Configuración Avanzada (Opcional)

### Personalizar Severidades que Bloquean

Edita el workflow para fallar en CRITICAL/HIGH:

```yaml
- name: Escanear vulnerabilidades con Trivy
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ secrets.DOCKERHUB_USERNAME }}/${{ env.DOCKER_IMAGE_NAME }}:alpine
    format: 'sarif'
    output: 'trivy-results-alpine.sarif'
    severity: 'CRITICAL,HIGH'  # ← Solo escanear estas
    exit-code: '1'              # ← Fallar si encuentra alguna
```

### Ignorar Vulnerabilidades Específicas

Crear archivo `.trivyignore`:

```
# Ignorar CVE conocido sin fix disponible
CVE-2024-1234

# Ignorar durante 30 días (con justificación)
CVE-2023-5678  # No hay fix, mitigado con firewall
```

### Escanear Solo Dependencias Python

```yaml
- name: Escanear solo Python packages
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: usuario/fastapi-web:alpine
    scanners: 'vuln'
    vuln-type: 'library'  # Solo librerías, no OS packages
```

---

## 📚 Recursos Adicionales

### Documentación Oficial
- **Trivy Docs:** https://aquasecurity.github.io/trivy/
- **GitHub Security:** https://docs.github.com/en/code-security
- **SARIF Format:** https://sarifweb.azurewebsites.net/

### Bases de Datos de CVEs
- **NVD (NIST):** https://nvd.nist.gov/
- **CVE.org:** https://cve.org/
- **Alpine Security:** https://security.alpinelinux.org/

### Herramientas Complementarias
- **Snyk:** Escáner comercial con features extras
- **Grype:** Alternativa open-source de Anchore
- **Clair:** Proyecto de CoreOS/Red Hat

---

## 🎯 Resumen Ejecutivo

### ¿Qué Hace Trivy en tu Pipeline?

```
Push a GitHub
    ↓
Build de imagen Docker
    ↓
Push a Docker Hub
    ↓
Trivy descarga la imagen ← AQUÍ
    ↓
Escanea paquetes y dependencias
    ↓
Genera reporte SARIF
    ↓
Sube a GitHub Security ← VER AQUÍ
    ↓
Dashboard actualizado ✅
```

### ¿Dónde Ver Resultados?

1. **🏆 GitHub Security Tab** (Mejor experiencia)
   - `github.com/TU-REPO/security/code-scanning`
   - Visualización interactiva
   - Filtros por severidad

2. **📝 Actions Logs** (Detalles técnicos)
   - `github.com/TU-REPO/actions`
   - Log completo del escaneo

3. **📄 Artifacts** (Datos crudos)
   - Archivos SARIF descargables
   - Para análisis offline

---

## ✅ Checklist de Seguridad

Después de cada deploy:

- [ ] Revisar Security tab
- [ ] Verificar que no hay CRITICAL/HIGH
- [ ] Investigar nuevas vulnerabilidades
- [ ] Actualizar dependencias si es necesario
- [ ] Re-escanear después de fix

---

**Creado:** 2025-01-22  
**Proyecto:** primeraWebFastAPI  
**Pipeline:** GitHub Actions + Trivy
