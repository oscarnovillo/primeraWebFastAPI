# 🔄 Auto-Updates de Imágenes Docker - Guía Completa

> **Problema:** ¿Cómo actualizar automáticamente contenedores cuando se publica una nueva imagen en Docker Hub?
> 
> **Solución:** Usar tags "flotantes" + herramientas de auto-update (Watchtower, Kubernetes, etc.)

---

## 📋 Tabla de Contenidos
1. [Sistema de tags explicado](#sistema-de-tags-explicado)
2. [Watchtower (Docker Compose)](#watchtower-docker-compose)
3. [Kubernetes con ImagePullPolicy](#kubernetes-auto-updates)
4. [Flux CD (GitOps)](#flux-cd-gitops)
5. [Renovate Bot (automatización total)](#renovate-bot)
6. [Comparativa de estrategias](#comparativa)

---

## 🏷️ Sistema de Tags Explicado

### **Tags actuales del proyecto:**

```yaml
# 1. Tags FLOTANTES (se sobrescriben en cada build)
alpine              # ← Siempre apunta a la última build Alpine
alpine-latest       # ← Alias explícito de "última versión"
optimized           # ← Siempre apunta a la última build Debian

# 2. Tags INMUTABLES (nunca cambian)
alpine-a1b2c3d      # ← Hash del commit específico
alpine-20260122     # ← Build de fecha específica

# 3. Tags SEMVER (solo en releases con git tag)
1.5.2-alpine        # ← Versión exacta
1.5-alpine          # ← Última versión 1.5.x (parches)
1-alpine            # ← Última versión 1.x.x (minor updates)
```

### **¿Cuál usar para auto-updates?**

| Tag | Auto-Update | Estabilidad | Uso Recomendado |
|-----|-------------|-------------|-----------------|
| `alpine` | ✅ Sí | ⚠️ Puede romper | Desarrollo/Testing |
| `alpine-latest` | ✅ Sí | ⚠️ Puede romper | Staging |
| `1-alpine` | ✅ Sí | ✅ Estable | **Producción (Major)** ⭐ |
| `1.5-alpine` | ✅ Sí | ✅✅ Muy estable | **Producción (Minor)** ⭐⭐ |
| `1.5.2-alpine` | ❌ No | ✅✅✅ Inmutable | Auditorías |
| `alpine-a1b2c3d` | ❌ No | ✅✅✅ Inmutable | Debugging |

---

## 🐳 Watchtower (Docker Compose)

### **¿Qué es Watchtower?**
Herramienta que monitorea Docker Hub y **actualiza automáticamente** contenedores cuando detecta nuevas imágenes.

### **Instalación:**

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Tu aplicación FastAPI
  fastapi-web:
    image: usuario/fastapi-web:alpine  # ← Tag flotante
    container_name: fastapi-web
    ports:
      - "8000:8000"
    restart: unless-stopped
    labels:
      - "com.centurylinklabs.watchtower.enable=true"  # Habilitar auto-update

  # Watchtower (auto-updater)
  watchtower:
    image: containrrr/watchtower:latest
    container_name: watchtower
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      # Chequear cada 5 minutos (300 segundos)
      - WATCHTOWER_POLL_INTERVAL=300
      
      # Solo actualizar contenedores con label "enable=true"
      - WATCHTOWER_LABEL_ENABLE=true
      
      # Limpiar imágenes viejas después de actualizar
      - WATCHTOWER_CLEANUP=true
      
      # Notificaciones (opcional)
      - WATCHTOWER_NOTIFICATIONS=email
      - WATCHTOWER_NOTIFICATION_EMAIL_FROM=watchtower@example.com
      - WATCHTOWER_NOTIFICATION_EMAIL_TO=admin@example.com
```

### **Uso:**

```bash
# 1. Levantar servicios
docker-compose up -d

# 2. Watchtower monitoreará alpine tag cada 5 minutos
# 3. Cuando detecte nueva imagen, hará:
#    - docker pull usuario/fastapi-web:alpine
#    - docker stop fastapi-web
#    - docker rm fastapi-web
#    - docker run (nueva versión)
#    - docker image prune (limpiar)

# 4. Ver logs de Watchtower
docker logs -f watchtower
```

### **Estrategias de actualización:**

```yaml
# Estrategia 1: AGRESIVA (cada push a main)
services:
  app:
    image: usuario/fastapi-web:alpine  # Se actualiza en cada commit

# Estrategia 2: MODERADA (solo releases minor)
services:
  app:
    image: usuario/fastapi-web:1-alpine  # Solo actualiza 1.x.x → 1.y.y

# Estrategia 3: CONSERVADORA (solo patches)
services:
  app:
    image: usuario/fastapi-web:1.5-alpine  # Solo actualiza 1.5.x → 1.5.y
```

---

## ☸️ Kubernetes Auto-Updates

### **Método 1: ImagePullPolicy Always**

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi-web
  template:
    metadata:
      labels:
        app: fastapi-web
    spec:
      containers:
      - name: fastapi-web
        image: usuario/fastapi-web:1.5-alpine  # Tag flotante (minor version)
        imagePullPolicy: Always  # ← Siempre chequear por nueva imagen
        ports:
        - containerPort: 8000
```

**Cómo funciona:**
- Cada vez que Kubernetes crea un nuevo pod, hace `docker pull`
- Si hay nueva imagen con el mismo tag, la descarga
- **Limitación:** Solo actualiza al crear nuevos pods (scaling, restart, etc.)

### **Método 2: CronJob que fuerza rollout**

```yaml
# auto-update-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: fastapi-web-auto-update
spec:
  schedule: "*/30 * * * *"  # Cada 30 minutos
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: deployment-updater
          containers:
          - name: kubectl
            image: bitnami/kubectl:latest
            command:
            - /bin/sh
            - -c
            - |
              # Forzar rollout restart (recrea pods con nueva imagen)
              kubectl rollout restart deployment/fastapi-web -n default
          restartPolicy: OnFailure
---
# ServiceAccount con permisos
apiVersion: v1
kind: ServiceAccount
metadata:
  name: deployment-updater
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployment-updater
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: deployment-updater
subjects:
- kind: ServiceAccount
  name: deployment-updater
roleRef:
  kind: Role
  name: deployment-updater
  apiGroup: rbac.authorization.k8s.io
```

**Cómo funciona:**
- CronJob ejecuta cada 30 minutos
- Fuerza un `rollout restart` del deployment
- Kubernetes recrea pods con nueva imagen (si existe)

### **Método 3: Keel (Kubernetes Auto-Update Tool)**

```yaml
# deployment.yaml con annotations de Keel
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-web
  annotations:
    keel.sh/policy: minor        # Actualizar versiones minor (1.5.x)
    keel.sh/trigger: poll        # Chequear Docker Hub periódicamente
    keel.sh/pollSchedule: "@every 5m"  # Cada 5 minutos
spec:
  template:
    spec:
      containers:
      - name: fastapi-web
        image: usuario/fastapi-web:1.5-alpine
```

**Instalación de Keel:**
```bash
# Usando Helm
helm repo add keel https://charts.keel.sh
helm install keel keel/keel --set helmProvider.enabled=true

# Keel monitoreará deployments con annotations
```

---

## 🚀 Flux CD (GitOps)

### **¿Qué es Flux?**
Sistema GitOps que sincroniza tu cluster Kubernetes con un repositorio Git.

### **Configuración:**

```yaml
# k8s/deployment.yaml (en tu repo Git)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-web
spec:
  template:
    spec:
      containers:
      - name: fastapi-web
        image: usuario/fastapi-web:1.5-alpine  # ← Flux actualizará esto
```

```yaml
# flux/image-policy.yaml
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImagePolicy
metadata:
  name: fastapi-web-policy
spec:
  imageRepositoryRef:
    name: fastapi-web-repo
  policy:
    semver:
      range: 1.5.x  # ← Solo actualizar parches 1.5.0 → 1.5.9
```

```yaml
# flux/image-repository.yaml
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImageRepository
metadata:
  name: fastapi-web-repo
spec:
  image: usuario/fastapi-web
  interval: 5m  # Chequear cada 5 minutos
```

**Cómo funciona:**
1. Flux escanea Docker Hub cada 5 minutos
2. Detecta nueva imagen `1.5.3-alpine` (cumple con range `1.5.x`)
3. **Actualiza automáticamente el archivo YAML en Git**
4. Hace commit y push al repo
5. Flux aplica el cambio al cluster

**Ventajas:**
- ✅ Auditoría completa (todo en Git)
- ✅ Rollback fácil (git revert)
- ✅ Aprobaciones (Pull Requests)

---

## 🤖 Renovate Bot (Automatización Total)

### **¿Qué es Renovate?**
Bot que **crea Pull Requests automáticos** cuando detecta nuevas versiones.

### **Configuración:**

```json
// renovate.json (en la raíz del repo)
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:base"],
  "docker": {
    "enabled": true,
    "pinDigests": true
  },
  "packageRules": [
    {
      "matchDatasources": ["docker"],
      "matchPackageNames": ["usuario/fastapi-web"],
      "versioning": "semver",
      "separateMajorMinor": true,
      "automerge": true,
      "automergeType": "pr",
      "matchUpdateTypes": ["patch"],  // Auto-merge solo parches
      "schedule": ["every weekend"]
    }
  ]
}
```

**Cómo funciona:**
1. Renovate chequea Docker Hub diariamente
2. Detecta nueva versión `1.5.3-alpine`
3. **Crea Pull Request** actualizando `docker-compose.yml`
4. Si es un patch (1.5.2 → 1.5.3), auto-merge
5. Si es minor/major, espera aprobación manual

---

## 📊 Comparativa de Estrategias

| Herramienta | Complejidad | Auto-Merge | GitOps | Mejor Para |
|-------------|-------------|------------|--------|------------|
| **Watchtower** | ⭐ Muy fácil | ✅ Sí | ❌ No | Docker Compose, VPS, homelab |
| **K8s ImagePullPolicy** | ⭐⭐ Fácil | ✅ Sí | ❌ No | Kubernetes simple |
| **Keel** | ⭐⭐ Fácil | ✅ Sí | ❌ No | Kubernetes con políticas |
| **Flux CD** | ⭐⭐⭐ Medio | ✅ Sí | ✅ Sí | Producción enterprise |
| **Renovate Bot** | ⭐⭐ Fácil | ⚠️ Configurable | ✅ Sí | Teams con code review |

---

## 🎯 Recomendaciones por Escenario

### **Escenario 1: Desarrollo/Testing**
```yaml
# docker-compose.yml
services:
  app:
    image: usuario/fastapi-web:alpine  # Última versión siempre
  
  watchtower:
    image: containrrr/watchtower
    environment:
      - WATCHTOWER_POLL_INTERVAL=60  # Chequear cada minuto
```
✅ **Por qué:** Quieres las últimas features inmediatamente

---

### **Escenario 2: Staging/Pre-producción**
```yaml
# deployment.yaml
spec:
  containers:
  - name: app
    image: usuario/fastapi-web:1-alpine  # Solo major version
    imagePullPolicy: Always

# + CronJob que fuerza rollout cada 6 horas
```
✅ **Por qué:** Balance entre actualizaciones y estabilidad

---

### **Escenario 3: Producción con Flux CD**
```yaml
# image-policy.yaml
spec:
  policy:
    semver:
      range: 1.5.x  # Solo parches
```
✅ **Por qué:** 
- Control total via Git
- Rollback fácil
- Auditoría completa
- Aprobaciones automáticas solo para parches

---

### **Escenario 4: Producción ultra-conservadora**
```yaml
# deployment.yaml
spec:
  containers:
  - name: app
    image: usuario/fastapi-web:1.5.2-alpine@sha256:abc123...  # Pinned digest
    imagePullPolicy: IfNotPresent
```
✅ **Por qué:** 
- Cero sorpresas
- Actualizaciones manuales con testing exhaustivo
- Usar Renovate para **notificaciones**, no auto-merge

---

## 🛠️ Ejemplo Completo: Watchtower + Notificaciones

```yaml
# docker-compose.production.yml
version: '3.8'

services:
  # Aplicación FastAPI
  fastapi-web:
    image: usuario/fastapi-web:1.5-alpine  # Tag flotante (minor version)
    container_name: fastapi-web
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - ENV=production
    labels:
      - "com.centurylinklabs.watchtower.enable=true"
      - "com.centurylinklabs.watchtower.monitor-only=false"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  # Watchtower con notificaciones Slack
  watchtower:
    image: containrrr/watchtower:latest
    container_name: watchtower
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      # Chequear cada hora
      - WATCHTOWER_POLL_INTERVAL=3600
      
      # Solo contenedores con label enable=true
      - WATCHTOWER_LABEL_ENABLE=true
      
      # Limpiar imágenes viejas
      - WATCHTOWER_CLEANUP=true
      
      # Incluir stopped containers
      - WATCHTOWER_INCLUDE_STOPPED=true
      
      # Notificaciones Slack
      - WATCHTOWER_NOTIFICATIONS=slack
      - WATCHTOWER_NOTIFICATION_SLACK_HOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ
      - WATCHTOWER_NOTIFICATION_SLACK_IDENTIFIER=watchtower-production
      
      # Logging
      - WATCHTOWER_DEBUG=false
      - WATCHTOWER_TRACE=false
```

**Deploy:**
```bash
# 1. Configurar secrets
export SLACK_WEBHOOK="https://hooks.slack.com/..."

# 2. Levantar stack
docker-compose -f docker-compose.production.yml up -d

# 3. Ver logs
docker logs -f watchtower

# 4. Forzar chequeo manual (sin esperar intervalo)
docker exec watchtower /watchtower --run-once
```

---

## 🔐 Seguridad: Validar Updates Antes de Aplicar

```yaml
# watchtower-safe.yml
services:
  watchtower:
    image: containrrr/watchtower
    environment:
      # IMPORTANTE: Solo monitorear, NO actualizar automáticamente
      - WATCHTOWER_MONITOR_ONLY=true
      - WATCHTOWER_NOTIFICATIONS=slack
    # Recibirás notificación en Slack cuando haya update disponible
    # Luego actualizas manualmente después de testing:
    # docker-compose pull && docker-compose up -d
```

---

## 📈 Monitoring de Updates

```bash
# Logs de Watchtower (ver qué se actualizó)
docker logs watchtower --since 24h

# Ver qué tag/digest tiene tu contenedor actualmente
docker inspect fastapi-web | jq '.[0].Config.Image'
docker inspect fastapi-web | jq '.[0].Image'  # SHA256 digest

# Comparar con Docker Hub
docker pull usuario/fastapi-web:1.5-alpine
docker images --digests | grep fastapi-web
```

---

## ✅ Checklist de Implementación

### Para Watchtower (Docker Compose):
- [ ] Usar tag flotante (`alpine`, `1-alpine`, `1.5-alpine`)
- [ ] Agregar servicio Watchtower al `docker-compose.yml`
- [ ] Configurar `WATCHTOWER_POLL_INTERVAL` (recomendado: 3600 = 1 hora)
- [ ] Habilitar `WATCHTOWER_CLEANUP=true`
- [ ] Configurar notificaciones (Slack, Email, etc.)
- [ ] Agregar healthcheck a tu app
- [ ] Testing: `docker exec watchtower /watchtower --run-once`

### Para Kubernetes:
- [ ] Usar tag SemVer flotante (`1.5-alpine`)
- [ ] Configurar `imagePullPolicy: Always`
- [ ] Opción A: Instalar Keel con annotations
- [ ] Opción B: Crear CronJob para `rollout restart`
- [ ] Opción C: Implementar Flux CD con ImagePolicy
- [ ] Configurar monitoring (Prometheus alerts en updates)

---

## 🚀 Próximos Pasos

1. **Decide tu estrategia:**
   - Desarrollo: `alpine` + Watchtower cada 5 min
   - Staging: `1-alpine` + Keel cada hora
   - Producción: `1.5-alpine` + Flux CD con aprobación

2. **Implementa:**
   ```bash
   # Copia uno de los ejemplos de arriba
   # Personaliza variables (SLACK_WEBHOOK, etc.)
   # Deploy
   ```

3. **Monitorea:**
   ```bash
   # Verifica que updates funcionen
   # Revisa logs de Watchtower/Keel/Flux
   # Confirma que rollbacks funcionen
   ```

---

## 📚 Referencias

- [Watchtower Docs](https://containrrr.dev/watchtower/)
- [Keel Documentation](https://keel.sh/)
- [Flux CD Image Automation](https://fluxcd.io/docs/guides/image-update/)
- [Renovate Bot](https://docs.renovatebot.com/)
- [Kubernetes Image Pull Policy](https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy)

---

**Actualizado:** 22 de enero de 2026  
**Proyecto:** primeraWebFastAPI  
**Relacionado:** `DOCKER-TAGS-EXPLICACION.md`
