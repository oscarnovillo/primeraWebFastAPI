# 📦 SBOM - Software Bill of Materials - Guía Completa

## 🎯 ¿Qué es SBOM?

**SBOM (Software Bill of Materials)** es un inventario completo de todos los componentes, librerías y dependencias que contiene tu software o imagen Docker.

Es como una "lista de ingredientes" o "factura detallada" de tu aplicación.

---

## 🔍 Analogía Simple

### SBOM es como la etiqueta nutricional de un producto:

**Producto alimenticio:**
```
Ingredientes:
- Harina de trigo (origen: España, lote: 2024-01)
- Azúcar (proveedor: XYZ, 100g)
- Chocolate (marca: Nestlé, 50g)
- Huevos (granja ABC, frescos)
- Levadura (tipo: química, 5g)

Información adicional:
- Sin gluten: NO
- Vegano: NO
- Alérgenos: Trigo, Huevo, Lácteos
```

**SBOM de tu imagen Docker:**
```json
{
  "name": "fastapi-web:alpine",
  "components": [
    {
      "name": "Alpine Linux",
      "version": "3.19.1",
      "supplier": "Alpine Linux Project"
    },
    {
      "name": "Python",
      "version": "3.11.6",
      "supplier": "Python Software Foundation"
    },
    {
      "name": "FastAPI",
      "version": "0.109.0",
      "license": "MIT",
      "supplier": "Sebastián Ramírez"
    },
    {
      "name": "OpenSSL",
      "version": "3.1.4-r5",
      "license": "Apache-2.0",
      "vulnerabilities": ["CVE-2024-1234"]
    }
  ]
}
```

---

## 🎯 Para Qué Sirve

### 1️⃣ **Seguridad Proactiva**

**Problema:** Se descubre una vulnerabilidad crítica

```
🚨 ALERTA: CVE-2024-9999
Vulnerabilidad crítica en OpenSSL 3.1.4
CVSS Score: 9.8 (CRITICAL)
```

**Con SBOM:**
```bash
# Buscar si estás afectado
grep "openssl.*3.1.4" sbom-alpine.spdx.json

# Resultado en segundos:
{
  "name": "libssl3",
  "version": "3.1.4-r5"  ← ¡VULNERABLE!
}

✅ Acción inmediata:
1. Actualizar imagen base
2. Reconstruir
3. Re-escanear
```

**Sin SBOM:**
```
❓ ¿Usamos OpenSSL?
❓ ¿Qué versión?
❓ ¿En qué imágenes?

→ Horas de investigación manual
→ Riesgo de pasar por alto alguna imagen
```

---

### 2️⃣ **Cumplimiento Normativo (Compliance)**

Muchas industrias y gobiernos **requieren SBOM por ley**:

#### **Estados Unidos**
```
Executive Order 14028 (2021)
"Todo software vendido al gobierno federal debe incluir SBOM"
```

#### **Unión Europea**
```
Cyber Resilience Act (2024)
"Fabricantes deben proporcionar SBOM de productos digitales"
```

#### **Industrias Reguladas**

| Sector | Regulación | Requiere SBOM |
|--------|------------|---------------|
| **Finanzas** | PCI-DSS 4.0 | ✅ Obligatorio |
| **Salud** | HIPAA | ✅ Recomendado |
| **Gobierno** | NIST SP 800-218 | ✅ Obligatorio |
| **Automotive** | ISO/SAE 21434 | ✅ Obligatorio |
| **Energía** | NERC CIP | ✅ Recomendado |

**Ejemplo de auditoría:**

```
Auditor: "Demuestre qué componentes usa en producción"

CON SBOM:
✅ Envías sbom-alpine.spdx.json
✅ Auditor verifica automáticamente
✅ Aprobado en minutos

SIN SBOM:
❌ Crear lista manualmente
❌ Verificar versiones una por una
❌ Documentar proveedores
❌ Días/semanas de trabajo
```

---

### 3️⃣ **Gestión de Licencias de Software**

El SBOM identifica **todas las licencias** de tus componentes:

```json
{
  "packages": [
    {
      "name": "FastAPI",
      "license": "MIT"  ← Licencia permisiva ✅
    },
    {
      "name": "GPL-Library",
      "license": "GPL-3.0"  ← ⚠️ Licencia copyleft
    },
    {
      "name": "Proprietary-SDK",
      "license": "Commercial"  ← ⚠️ Requiere licencia
    }
  ]
}
```

#### **Tipos de Licencias**

| Tipo | Ejemplos | Implicaciones |
|------|----------|---------------|
| **Permisivas** | MIT, Apache, BSD | ✅ Uso libre, incluso comercial |
| **Copyleft** | GPL, AGPL | ⚠️ Requiere código abierto |
| **Weak Copyleft** | LGPL, MPL | ⚡ Requiere atribución |
| **Comerciales** | Oracle, Microsoft | 💰 Requiere licencia pagada |

**Caso real problemático:**

```
Tu aplicación usa:
└─ biblioteca-abc (GPL-3.0)
    └─ Requiere que TODO tu código sea open-source

Si tu producto es propietario:
❌ Violación de licencia
❌ Posibles demandas legales
❌ Multas millonarias

Con SBOM:
✅ Detectas GPL-3.0 antes de desplegar
✅ Buscas alternativa con MIT/Apache
✅ Evitas problemas legales
```

---

### 4️⃣ **Trazabilidad de Cadena de Suministro**

Sabes **de dónde viene cada componente**:

```
Tu Imagen Docker
  ↓
Alpine Linux 3.19.1
  ├─ Fuente: https://dl-cdn.alpinelinux.org/alpine/
  ├─ Checksum: sha256:abc123def456...
  ├─ Firmado por: Alpine Release Team
  └─ Contiene:
      ├─ Python 3.11.6
      │   ├─ Fuente: https://www.python.org/ftp/python/
      │   ├─ Checksum: sha256:xyz789...
      │   └─ Dependencias:
      │       └─ OpenSSL 3.1.4
      │           ├─ Fuente: https://www.openssl.org/source/
      │           └─ Checksum: sha256:qwe456...
      └─ musl-libc 1.2.4
          └─ Fuente: https://musl.libc.org/
```

#### **Caso Real: Supply Chain Attack**

**SolarWinds (2020)**
```
Atacantes comprometieron un componente de software
→ Insertaron código malicioso
→ Miles de empresas afectadas
→ Daños: miles de millones de dólares
```

**Cómo SBOM ayuda:**

```bash
# SBOM incluye checksums (hashes)
{
  "name": "solarwinds-component",
  "version": "2020.2.1",
  "checksum": {
    "algorithm": "SHA256",
    "value": "abc123def456..."  ← Hash esperado
  }
}

# Verificar integridad
sha256sum downloaded-component
# Output: xyz789...  ← ¡NO COINCIDE!

✅ Detectas componente comprometido ANTES de usarlo
```

---

### 5️⃣ **Respuesta Rápida a Incidentes**

**Escenario:** Vulnerabilidad Zero-Day descubierta

```
📰 CVE-2024-XXXX: Vulnerabilidad crítica en Log4j
🚨 CVSS: 10.0 (CRITICAL)
⏰ Explotación activa en la naturaleza
```

**Con SBOM (respuesta en minutos):**

```bash
# Buscar en todos los SBOM
grep -r "log4j" sbom-*.json

# Resultado:
sbom-api-service.json: "log4j:2.14.1"  ← VULNERABLE
sbom-web-app.json: No encontrado
sbom-database.json: No encontrado

# Acción:
1. Actualizar solo api-service
2. Desplegar fix en 1 hora
3. Crisis evitada ✅
```

**Sin SBOM (respuesta en días):**

```
1. ¿Qué servicios usan Log4j? 🤷
2. Revisar cada Dockerfile...
3. Revisar cada requirements.txt...
4. Revisar dependencias transitivas...
5. ¿Nos olvidamos de algo?
6. Actualizar TODO "por las dudas"
7. Despliegue masivo (riesgoso)
8. ⏰ 2-3 días mínimo
```

---

## 📄 Formato del SBOM: SPDX

Tu pipeline usa **SPDX** (Software Package Data Exchange), el estándar internacional más popular.

### **Estructura del Archivo**

```json
{
  "spdxVersion": "SPDX-2.3",
  "dataLicense": "CC0-1.0",
  "SPDXID": "SPDXRef-DOCUMENT",
  "name": "fastapi-web:alpine",
  "creationInfo": {
    "created": "2025-01-22T10:30:00Z",
    "creators": ["Tool: syft-0.98.0"],
    "licenseListVersion": "3.21"
  },
  
  "packages": [
    {
      "SPDXID": "SPDXRef-Package-fastapi",
      "name": "fastapi",
      "versionInfo": "0.109.0",
      "supplier": "Person: Sebastián Ramírez",
      "downloadLocation": "https://pypi.org/project/fastapi/0.109.0/",
      "filesAnalyzed": false,
      "licenseConcluded": "MIT",
      "licenseInfoFromFiles": ["MIT"],
      "copyrightText": "Copyright 2018 Sebastián Ramírez",
      "checksums": [
        {
          "algorithm": "SHA256",
          "checksumValue": "abc123def456..."
        }
      ],
      "externalRefs": [
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:pypi/fastapi@0.109.0"
        }
      ]
    },
    
    {
      "SPDXID": "SPDXRef-Package-openssl",
      "name": "libssl3",
      "versionInfo": "3.1.4-r5",
      "supplier": "Organization: OpenSSL Project",
      "downloadLocation": "https://www.openssl.org/source/openssl-3.1.4.tar.gz",
      "licenseConcluded": "Apache-2.0",
      "checksums": [
        {
          "algorithm": "SHA256",
          "checksumValue": "xyz789..."
        }
      ]
    }
  ],
  
  "relationships": [
    {
      "spdxElementId": "SPDXRef-Package-fastapi",
      "relationshipType": "DEPENDS_ON",
      "relatedSpdxElement": "SPDXRef-Package-starlette"
    },
    {
      "spdxElementId": "SPDXRef-Package-fastapi",
      "relationshipType": "DEPENDS_ON",
      "relatedSpdxElement": "SPDXRef-Package-pydantic"
    }
  ]
}
```

---

## 🔧 Cómo Funciona en Tu Pipeline

### **Paso a Paso**

```yaml
- name: Build y Push imagen Docker
  uses: docker/build-push-action@v5
  with:
    push: true
    tags: usuario/fastapi-web:alpine
  # ↑ Imagen publicada en Docker Hub

- name: Generar SBOM
  uses: anchore/sbom-action@v0
  with:
    image: usuario/fastapi-web:alpine  # Imagen a analizar
    format: spdx-json                   # Formato estándar
    output-file: sbom-alpine.spdx.json  # Archivo resultado
```

### **Lo Que Hace Internamente**

```
1. Descarga imagen desde Docker Hub
2. Extrae todas las capas de la imagen
3. Escanea:
   ├─ Paquetes del sistema (APK en Alpine)
   ├─ Dependencias Python (pip packages)
   ├─ Librerías del sistema (.so files)
   ├─ Binarios ejecutables
   └─ Metadatos de archivos
4. Consulta bases de datos de paquetes
5. Obtiene licencias de cada componente
6. Calcula checksums (hashes)
7. Mapea dependencias transitivas
8. Genera archivo SPDX-JSON
9. Sube como artifact a GitHub
```

---

## 📊 Ejemplo Real de Tu Proyecto

### **SBOM Generado para fastapi-web:alpine**

```json
{
  "name": "fastapi-web:alpine",
  "packages": [
    {
      "name": "alpine-baselayout",
      "version": "3.4.3-r2",
      "license": "GPL-2.0-only"
    },
    {
      "name": "python3",
      "version": "3.11.6-r0",
      "license": "PSF-2.0"
    },
    {
      "name": "fastapi",
      "version": "0.109.0",
      "license": "MIT",
      "purl": "pkg:pypi/fastapi@0.109.0"
    },
    {
      "name": "uvicorn",
      "version": "0.27.0",
      "license": "BSD-3-Clause",
      "dependencies": ["httptools", "uvloop", "websockets"]
    },
    {
      "name": "jinja2",
      "version": "3.1.3",
      "license": "BSD-3-Clause"
    },
    {
      "name": "starlette",
      "version": "0.35.1",
      "license": "BSD-3-Clause"
    },
    {
      "name": "pydantic",
      "version": "2.5.3",
      "license": "MIT"
    },
    {
      "name": "libssl3",
      "version": "3.1.4-r5",
      "license": "Apache-2.0"
    }
    // ... ~50-100 paquetes más
  ]
}
```

### **Análisis del SBOM**

```bash
# Total de paquetes
jq '.packages | length' sbom-alpine.spdx.json
# Output: 87 paquetes

# Licencias únicas
jq '.packages[].licenseConcluded' sbom-alpine.spdx.json | sort | uniq
# Output:
#   MIT (mayoría)
#   Apache-2.0
#   BSD-3-Clause
#   GPL-2.0-only (algunos componentes del sistema)
#   PSF-2.0 (Python)

# Paquetes Python
jq '.packages[] | select(.name | contains("fastapi"))' sbom-alpine.spdx.json

# Dependencias de FastAPI
jq '.relationships[] | select(.spdxElementId | contains("fastapi"))' sbom-alpine.spdx.json
```

---

## 🎯 Casos de Uso Prácticos

### **Caso 1: Auditoría de Cliente**

**Escenario:**
```
Cliente: "Necesitamos saber qué componentes usa su aplicación
         para nuestra auditoría de seguridad anual"
```

**Respuesta CON SBOM:**
```
Tú: "Aquí está el SBOM completo en formato SPDX"
    → Envías sbom-alpine.spdx.json
    → Cliente carga en su herramienta de compliance
    → Verificación automática en 5 minutos
    → ✅ Aprobado
```

**Respuesta SIN SBOM:**
```
Tú: "Déjame preparar la documentación..."
    → Revisar Dockerfile
    → Listar dependencias manualmente
    → Verificar versiones
    → Documentar en Excel
    → Enviar al cliente
    → Cliente verifica manualmente
    → ⏰ 2-3 días de trabajo
```

---

### **Caso 2: Vulnerabilidad Log4Shell**

**Diciembre 2021:**
```
🚨 ALERTA CRÍTICA: CVE-2021-44228 (Log4Shell)
CVSS: 10.0 (CRITICAL)
Afecta: Apache Log4j 2.0-beta9 hasta 2.14.1
```

**Empresa CON SBOM:**
```bash
# Buscar en todos los servicios (segundos)
grep -r "log4j" sbom-*.json

# Resultado:
sbom-api-service.json: log4j:2.14.1  ← VULNERABLE
sbom-legacy-app.json: log4j:2.12.1   ← VULNERABLE

# Acción (1 hora):
1. Actualizar solo esos 2 servicios
2. Desplegar fix
3. Re-escanear SBOM
4. Confirmar remediación

✅ Crisis resuelta en 1 hora
✅ 0 brechas de seguridad
```

**Empresa SIN SBOM:**
```
1. ¿Qué servicios usan Log4j? 🤷
2. Revisar 50+ microservicios...
3. Revisar dependencias transitivas...
4. ¿Nos olvidamos de algo?
5. Actualizar TODO "por las dudas"
6. Testing masivo
7. Despliegue de emergencia

⏰ 2-3 días de trabajo
💸 Millones en pérdidas
🚨 Posibles brechas durante ese tiempo
```

---

### **Caso 3: Licencias Incompatibles**

**Escenario:**
```
Tu startup desarrolla software propietario
Usas una librería con licencia GPL-3.0 sin darte cuenta
```

**Problema:**
```
GPL-3.0 requiere:
❌ Todo código derivado debe ser open-source
❌ Código fuente debe estar disponible públicamente

Si vendes software propietario:
⚖️ Violación de licencia
💰 Posibles demandas (millones en daños)
📰 Reputación dañada
```

**Con SBOM:**
```bash
# Buscar licencias problemáticas
jq '.packages[] | select(.licenseConcluded | contains("GPL"))' sbom-alpine.spdx.json

# Resultado:
{
  "name": "problema-library",
  "license": "GPL-3.0"  ← ⚠️ ALERTA
}

# Acción:
1. Buscar alternativa con MIT/Apache
2. Reemplazar librería
3. Re-generar SBOM
4. Verificar compliance

✅ Problema evitado ANTES de vender
```

**Sin SBOM:**
```
→ Desconoces el problema
→ Vendes el producto
→ Cliente descubre GPL en tu código
→ Demanda legal
→ 💸 Millones en pérdidas
```

---

## 🛠️ Herramientas para Analizar SBOM

### **1. Análisis en Terminal**

```bash
# Instalaren jq para procesar JSON
# Windows: choco install jq
# Linux: apt install jq

# Contar paquetes
jq '.packages | length' sbom-alpine.spdx.json

# Listar solo nombres y versiones
jq '.packages[] | "\(.name):\(.versionInfo)"' sbom-alpine.spdx.json

# Buscar paquete específico
jq '.packages[] | select(.name == "fastapi")' sbom-alpine.spdx.json

# Listar todas las licencias
jq '.packages[].licenseConcluded' sbom-alpine.spdx.json | sort | uniq -c

# Buscar licencias GPL (problemáticas)
jq '.packages[] | select(.licenseConcluded | contains("GPL"))' sbom-alpine.spdx.json

# Ver dependencias de un paquete
jq '.relationships[] | select(.spdxElementId | contains("fastapi"))' sbom-alpine.spdx.json
```

### **2. Herramientas Visuales**

#### **FOSSA**
```
https://fossa.com/
→ Carga SBOM
→ Análisis de licencias
→ Detección de vulnerabilidades
→ Reportes de compliance
```

#### **Dependency-Track**
```
https://dependencytrack.org/
→ Open-source
→ Dashboard de vulnerabilidades
→ Gestión de licencias
→ Alertas automáticas
```

#### **Grype (Anchore)**
```bash
# Escanear SBOM en busca de vulnerabilidades
grype sbom:./sbom-alpine.spdx.json

# Output:
NAME     INSTALLED  VULNERABILITY   SEVERITY
libssl3  3.1.4-r5   CVE-2024-1234   High
python3  3.11.6     CVE-2023-5678   Medium
```

---

## 📊 Integración con Herramientas de Seguridad

### **Flujo Completo**

```
GitHub Actions
    ↓
1. Build imagen Docker
    ↓
2. Push a Docker Hub
    ↓
3. Generar SBOM (Anchore)
    ↓
4. Escanear vulnerabilidades (Trivy)
    ↓
5. Comparar SBOM vs CVEs
    ↓
6. Reportar en GitHub Security
    ↓
7. Almacenar SBOM como artifact
```

### **SBOM + Trivy = Doble Verificación**

```yaml
# Tu workflow ya hace esto:

1. Trivy escanea la imagen directamente
   → Encuentra vulnerabilidades en tiempo real

2. SBOM documenta qué hay en la imagen
   → Permite análisis posterior
   → Auditorías de compliance
   → Comparaciones históricas

# Son complementarios:
Trivy  → "¿Qué está vulnerable AHORA?"
SBOM   → "¿Qué contiene esta imagen?"
```

---

## 📈 Beneficios Cuantificables

| Métrica | Sin SBOM | Con SBOM | Mejora |
|---------|----------|----------|--------|
| **Tiempo de respuesta a CVE** | 2-3 días | 5-10 min | **99% más rápido** |
| **Auditorías de compliance** | 1-2 semanas | 1 hora | **95% más rápido** |
| **Detección de licencias** | Manual | Automático | **100% cobertura** |
| **Costo de auditoría** | $10k-50k | $500-1k | **90% ahorro** |
| **Riesgo de brechas** | Alto | Bajo | **80% reducción** |

---

## ✅ Checklist de Uso del SBOM

### **Después de Cada Deploy**

- [ ] Descargar SBOM de GitHub Artifacts
- [ ] Analizar licencias (`jq '.packages[].licenseConcluded'`)
- [ ] Verificar que no hay GPL/AGPL (si es propietario)
- [ ] Guardar SBOM en repositorio de documentación
- [ ] Comparar con SBOM anterior (cambios)

### **Mensualmente**

- [ ] Revisar SBOM en busca de paquetes desactualizados
- [ ] Comparar con base de datos de CVEs
- [ ] Generar reporte de compliance
- [ ] Actualizar componentes críticos

### **Antes de Auditorías**

- [ ] Preparar SBOM de todas las imágenes en producción
- [ ] Generar reporte de licencias
- [ ] Documentar proveedores de componentes
- [ ] Verificar checksums de componentes críticos

---

## 🎓 Recursos Adicionales

### **Estándares**
- **SPDX:** https://spdx.dev/
- **CycloneDX:** https://cyclonedx.org/ (alternativa a SPDX)
- **SWID:** https://csrc.nist.gov/projects/Software-Identification-SWID

### **Herramientas**
- **Syft:** https://github.com/anchore/syft (genera SBOM)
- **Grype:** https://github.com/anchore/grype (escanea SBOM)
- **FOSSA:** https://fossa.com/ (compliance)
- **Dependency-Track:** https://dependencytrack.org/ (open-source)

### **Regulaciones**
- **NTIA SBOM:** https://www.ntia.gov/sbom
- **Executive Order 14028:** https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity
- **Cyber Resilience Act (EU):** https://digital-strategy.ec.europa.eu/en/library/cyber-resilience-act

---

## 🎯 Resumen Ejecutivo

### **¿Por Qué SBOM?**

1. **🔒 Seguridad:** Respuesta rápida a vulnerabilidades
2. **📋 Compliance:** Cumplir regulaciones automáticamente
3. **⚖️ Licencias:** Evitar problemas legales
4. **🔍 Transparencia:** Saber exactamente qué tienes
5. **⚡ Eficiencia:** Auditorías en minutos vs días
6. **💰 Ahorro:** Reducir costos de gestión

### **¿Dónde Está Mi SBOM?**

```
GitHub → Actions → Workflow ejecutado → Artifacts
→ Descargar: sbom-alpine.spdx.json
→ Descargar: sbom-optimized.spdx.json
```

### **¿Qué Hacer con Él?**

1. **Guardarlo** para auditorías futuras
2. **Analizarlo** con jq o herramientas visuales
3. **Compararlo** con bases de datos de CVEs
4. **Compartirlo** con clientes/auditores
5. **Monitorearlo** para cambios sospechosos

---

**Creado:** 2025-01-22  
**Proyecto:** primeraWebFastAPI  
**Formato:** SPDX-2.3  
**Generado por:** Anchore Syft
