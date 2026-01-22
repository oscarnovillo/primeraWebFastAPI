# 📊 Cómo Ver los Reportes de Seguridad (Repos Privados)

> **Nota:** Esta guía es para repositorios **privados sin GitHub Advanced Security**. Si tu repo es público, los resultados aparecen automáticamente en la pestaña **Security** → **Code scanning**.

---

## 🎯 Acceder a los Reportes

### **Paso 1: Ve a la pestaña Actions**
1. En tu repositorio GitHub, click en **"Actions"** (arriba, junto a Pull Requests)
2. Verás la lista de todos los workflows ejecutados

### **Paso 2: Selecciona un workflow ejecutado**
3. Click en el último workflow exitoso (con ✅ verde)
4. Verás los jobs: `Build and Test`, `Docker Build and Push`, etc.

### **Paso 3: Descarga los Artifacts**
5. Scroll hasta el final de la página
6. En la sección **"Artifacts"** verás:
   - `security-reports-alpine` (reportes de la imagen Alpine)
   - `security-reports-optimized` (reportes de la imagen Debian optimizada)

7. **Click en el artifact** → Se descarga un archivo ZIP

---

## 📁 Contenido de los Artifacts

Cada ZIP contiene **3 archivos**:

### **1. `trivy-results-alpine.txt` (Tabla legible)**
```
┌─────────────────────┬────────────────┬──────────┬────────────────┬───────────────────┬───────────────┐
│       Library       │  Vulnerability │ Severity │ Installed Ver  │   Fixed Version   │     Title     │
├─────────────────────┼────────────────┼──────────┼────────────────┼───────────────────┼───────────────┤
│ openssl             │ CVE-2024-5678  │   HIGH   │ 1.1.1n         │ 1.1.1q            │ Buffer overflow│
└─────────────────────┴────────────────┴──────────┴────────────────┴───────────────────┴───────────────┘
```
👉 **Para qué:** Vista rápida de vulnerabilidades

### **2. `trivy-results-alpine.json` (Datos estructurados)**
```json
{
  "Results": [
    {
      "Target": "python:3.11-slim",
      "Vulnerabilities": [
        {
          "VulnerabilityID": "CVE-2024-5678",
          "Severity": "HIGH",
          "InstalledVersion": "1.1.1n",
          "FixedVersion": "1.1.1q"
        }
      ]
    }
  ]
}
```
👉 **Para qué:** Procesamiento automatizado, CI/CD, dashboards

### **3. `sbom-alpine.spdx.json` (Software Bill of Materials)**
```json
{
  "name": "fastapi-web",
  "packages": [
    {
      "name": "fastapi",
      "versionInfo": "0.104.1",
      "licenseConcluded": "MIT"
    }
  ]
}
```
👉 **Para qué:** Auditorías de seguridad, compliance, rastreo de dependencias

---

## 🔍 Cómo Interpretar los Resultados

### **Severidades de Trivy:**

| Severidad | Color | Acción Recomendada |
|-----------|-------|-------------------|
| 🔴 **CRITICAL** | Rojo | ⚠️ **URGENTE** - Actualizar inmediatamente |
| 🟠 **HIGH** | Naranja | ⚡ Actualizar pronto (1-2 semanas) |
| 🟡 **MEDIUM** | Amarillo | 📅 Planificar actualización (1 mes) |
| 🔵 **LOW** | Azul | ℹ️ Informativo - Revisar en próximo sprint |

### **Ejemplo de lectura:**
```
Library: openssl
Vulnerability: CVE-2024-5678
Severity: HIGH
Installed: 1.1.1n
Fixed in: 1.1.1q
Title: Buffer overflow in SSL handshake
```

**Interpretación:**
- Tu imagen usa OpenSSL 1.1.1n (vulnerable)
- Existe una vulnerabilidad ALTA (buffer overflow)
- Se soluciona actualizando a 1.1.1q
- **Acción:** Actualizar base image de Python que incluye OpenSSL nuevo

---

## 🛠️ Qué Hacer con las Vulnerabilidades

### **1. Vulnerabilidades en Base Image (Python, Alpine, etc.)**
```dockerfile
# ANTES (vulnerable)
FROM python:3.11-slim

# DESPUÉS (actualizado)
FROM python:3.11-slim
# Agregar actualización de paquetes del sistema
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
```

### **2. Vulnerabilidades en Dependencias Python**
```bash
# Ver versión vulnerable
pip show paquete-vulnerable

# Actualizar a versión segura
pip install --upgrade paquete-vulnerable==VERSION_SEGURA

# Actualizar requirements.txt
echo "paquete-vulnerable==VERSION_SEGURA" >> requirements.txt
```

### **3. Vulnerabilidades sin Fix Disponible**
- **Opción 1:** Aceptar el riesgo (documentar en README)
- **Opción 2:** Buscar librería alternativa
- **Opción 3:** Aplicar mitigaciones (WAF, rate limiting, etc.)

---

## 📊 Comparar Reportes Entre Imágenes

### **Descargar ambos artifacts:**
1. `security-reports-alpine.zip`
2. `security-reports-optimized.zip`

### **Comparar tamaños de imágenes vs seguridad:**

| Imagen | Tamaño | Vulns CRITICAL | Vulns HIGH | Recomendación |
|--------|--------|----------------|------------|---------------|
| Alpine | 109 MB | 0 | 2 | ✅ Mejor para producción |
| Optimized | 201 MB | 1 | 5 | ⚠️ Actualizar base image |

---

## 🔄 Automatización: Integrar con Slack/Discord

Si quieres **notificaciones automáticas** cuando hay vulnerabilidades críticas:

```yaml
# Agregar al workflow (después de Trivy scan)
- name: Notificar vulnerabilidades críticas
  if: always()
  run: |
    CRITICAL_COUNT=$(cat trivy-results-alpine.json | jq '[.Results[].Vulnerabilities[] | select(.Severity=="CRITICAL")] | length')
    if [ "$CRITICAL_COUNT" -gt 0 ]; then
      echo "⚠️ ALERTA: $CRITICAL_COUNT vulnerabilidades CRÍTICAS encontradas"
      # Aquí puedes agregar webhook a Slack/Discord
    fi
```

---

## 📈 Historial de Seguridad

Los artifacts se guardan **90 días** (configurable en `retention-days`).

**Para comparar evolución:**
1. Descarga artifact de hace 1 mes
2. Descarga artifact actual
3. Compara archivos JSON con herramientas como `jq` o `diff`

```bash
# Comparar vulnerabilidades entre versiones
diff <(jq '.Results[].Vulnerabilities[].VulnerabilityID' trivy-old.json | sort) \
     <(jq '.Results[].Vulnerabilities[].VulnerabilityID' trivy-new.json | sort)
```

---

## 🎓 Recursos Adicionales

- **Trivy Database:** https://avd.aquasec.com/
- **CVE Search:** https://cve.mitre.org/cve/search_cve_list.html
- **National Vulnerability Database:** https://nvd.nist.gov/

---

## ❓ FAQ

**P: ¿Por qué no aparecen en la pestaña Security?**
R: GitHub Code Scanning solo funciona en repos públicos o con GitHub Advanced Security (pago).

**P: ¿Puedo automatizar la descarga de artifacts?**
R: Sí, usa la GitHub CLI: `gh run download <run-id> -n security-reports-alpine`

**P: ¿Qué hago si hay 100+ vulnerabilidades?**
R: Prioriza CRITICAL/HIGH, actualiza base image, y considera cambiar a Alpine (menos superficie de ataque).

**P: ¿Los artifacts ocupan espacio del repo?**
R: No, se almacenan separadamente y se borran automáticamente después de 90 días.

---

## 🚀 Siguiente Paso

Si tu proyecto es **open source o puede ser público**, considera hacer el repositorio público para obtener:
- ✅ Code Scanning gratis en pestaña Security
- ✅ Dependabot alerts automáticos
- ✅ Gráficos de tendencias de vulnerabilidades
- ✅ Mayor visibilidad y contribuciones

**Cómo hacerlo:** Settings → Danger Zone → Change visibility → Make public
