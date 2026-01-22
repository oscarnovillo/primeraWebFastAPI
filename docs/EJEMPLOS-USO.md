# 🚀 Ejemplos de Uso - FastAPI Docker Images

Guía práctica con ejemplos reales de cómo usar las imágenes Docker publicadas en diferentes escenarios.

---

## 📋 Prerequisitos

```bash
# Verificar que Docker está instalado
docker --version

# Login a Docker Hub (opcional, solo para imágenes privadas)
docker login
```

---

## 🏃 Inicio Rápido (30 segundos)

### Ejecutar la aplicación

```bash
# Descargar y ejecutar imagen Alpine (recomendada, 109 MB)
docker run -d \
  --name fastapi-app \
  -p 8000:8000 \
  TU-USUARIO/fastapi-web:alpine

# Verificar que funciona
curl http://localhost:8000

# Ver logs
docker logs fastapi-app

# Detener
docker stop fastapi-app

# Eliminar
docker rm fastapi-app
```

### Ejecutar versión optimizada

```bash
# Usar imagen Debian-based (201 MB)
docker run -d \
  --name fastapi-app \
  -p 8000:8000 \
  TU-USUARIO/fastapi-web:optimized
```

---

## 🛠️ Escenarios de Uso

### 1. Desarrollo Local con Hot-Reload

```bash
# Montar código local para desarrollo
docker run -d \
  --name fastapi-dev \
  -p 8000:8000 \
  -v $(pwd):/app \
  -e RELOAD=true \
  TU-USUARIO/fastapi-web:alpine \
  uvicorn main:app --host 0.0.0.0 --reload

# En Windows PowerShell
docker run -d `
  --name fastapi-dev `
  -p 8000:8000 `
  -v ${PWD}:/app `
  -e RELOAD=true `
  TU-USUARIO/fastapi-web:alpine `
  uvicorn main:app --host 0.0.0.0 --reload
```

### 2. Producción con Docker Compose

**Archivo:** `docker-compose.prod.yml`

```yaml
version: '3.8'

services:
  web:
    image: TU-USUARIO/fastapi-web:alpine
    container_name: fastapi-prod
    restart: unless-stopped
    ports:
      - "80:8000"
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=info
    healthcheck:
      test: ["CMD", "python", "-c", "import socket; s=socket.socket(); s.connect(('localhost', 8000)); s.close()"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - app-network

  # Opcional: Nginx como reverse proxy
  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    restart: unless-stopped
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

**Uso:**

```bash
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml down
```

### 3. Scaling con Docker Compose

```yaml
version: '3.8'

services:
  web:
    image: TU-USUARIO/fastapi-web:alpine
    restart: unless-stopped
    environment:
      - ENVIRONMENT=production
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx-load-balancer.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
    networks:
      - app-network

networks:
  app-network:
```

**Escalar a 5 instancias:**

```bash
docker-compose up -d --scale web=5
```

### 4. Kubernetes Deployment

**Archivo:** `k8s-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-deployment
  labels:
    app: fastapi
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
      - name: fastapi
        image: TU-USUARIO/fastapi-web:alpine
        ports:
        - containerPort: 8000
        resources:
          limits:
            memory: "256Mi"
            cpu: "500m"
          requests:
            memory: "128Mi"
            cpu: "250m"
        livenessProbe:
          exec:
            command:
            - python
            - -c
            - "import socket; s=socket.socket(); s.connect(('localhost', 8000)); s.close()"
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - python
            - -c
            - "import socket; s=socket.socket(); s.connect(('localhost', 8000)); s.close()"
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  selector:
    app: fastapi
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

**Desplegar en Kubernetes:**

```bash
# Aplicar deployment
kubectl apply -f k8s-deployment.yaml

# Verificar pods
kubectl get pods

# Ver logs
kubectl logs -l app=fastapi

# Escalar
kubectl scale deployment fastapi-deployment --replicas=5

# Obtener URL del servicio
kubectl get service fastapi-service
```

### 5. AWS ECS (Elastic Container Service)

**Task Definition (JSON):**

```json
{
  "family": "fastapi-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "fastapi-container",
      "image": "TU-USUARIO/fastapi-web:alpine",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "healthCheck": {
        "command": [
          "CMD-SHELL",
          "python -c 'import socket; s=socket.socket(); s.connect((\"localhost\", 8000)); s.close()'"
        ],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      },
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/fastapi",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**Comandos AWS CLI:**

```bash
# Registrar task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Crear servicio
aws ecs create-service \
  --cluster fastapi-cluster \
  --service-name fastapi-service \
  --task-definition fastapi-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### 6. Azure Container Instances

```bash
# Crear grupo de recursos
az group create --name fastapi-rg --location eastus

# Desplegar contenedor
az container create \
  --resource-group fastapi-rg \
  --name fastapi-container \
  --image TU-USUARIO/fastapi-web:alpine \
  --cpu 1 \
  --memory 1 \
  --ports 8000 \
  --dns-name-label fastapi-app-unique \
  --environment-variables ENVIRONMENT=production

# Obtener URL
az container show \
  --resource-group fastapi-rg \
  --name fastapi-container \
  --query ipAddress.fqdn \
  --output tsv
```

### 7. Google Cloud Run

```bash
# Desplegar en Cloud Run
gcloud run deploy fastapi-service \
  --image TU-USUARIO/fastapi-web:alpine \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --port 8000

# Obtener URL
gcloud run services describe fastapi-service \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

### 8. DigitalOcean App Platform

**Archivo:** `.do/app.yaml`

```yaml
name: fastapi-app
services:
  - name: web
    image:
      registry_type: DOCKER_HUB
      registry: TU-USUARIO
      repository: fastapi-web
      tag: alpine
    instance_count: 2
    instance_size_slug: basic-xs
    http_port: 8000
    health_check:
      http_path: /
    routes:
      - path: /
```

**Desplegar:**

```bash
# Usando doctl CLI
doctl apps create --spec .do/app.yaml

# O usar la interfaz web de DigitalOcean
```

---

## 🔧 Configuración Avanzada

### Variables de Entorno Comunes

```bash
docker run -d \
  --name fastapi-app \
  -p 8000:8000 \
  -e ENVIRONMENT=production \
  -e LOG_LEVEL=info \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e SECRET_KEY=your-secret-key \
  -e ALLOWED_HOSTS=* \
  TU-USUARIO/fastapi-web:alpine
```

### Persistencia de Datos

```bash
# Crear volumen
docker volume create fastapi-data

# Ejecutar con volumen
docker run -d \
  --name fastapi-app \
  -p 8000:8000 \
  -v fastapi-data:/app/data \
  TU-USUARIO/fastapi-web:alpine
```

### Networking Personalizado

```bash
# Crear red
docker network create fastapi-network

# Ejecutar base de datos
docker run -d \
  --name postgres \
  --network fastapi-network \
  -e POSTGRES_PASSWORD=secret \
  postgres:15-alpine

# Ejecutar app
docker run -d \
  --name fastapi-app \
  --network fastapi-network \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:secret@postgres:5432/mydb \
  TU-USUARIO/fastapi-web:alpine
```

---

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real

```bash
# Logs en tiempo real
docker logs -f fastapi-app

# Últimas 100 líneas
docker logs --tail 100 fastapi-app

# Con timestamps
docker logs -t fastapi-app
```

### Inspeccionar Contenedor

```bash
# Stats de recursos
docker stats fastapi-app

# Información completa
docker inspect fastapi-app

# Procesos en ejecución
docker top fastapi-app
```

### Ejecutar Comandos Dentro del Contenedor

```bash
# Shell interactivo
docker exec -it fastapi-app sh

# Ejecutar comando único
docker exec fastapi-app python --version

# Ver variables de entorno
docker exec fastapi-app env
```

---

## 🔒 Seguridad

### Escanear Vulnerabilidades

```bash
# Usando Trivy (recomendado)
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image TU-USUARIO/fastapi-web:alpine

# Usando Docker Scout
docker scout cves TU-USUARIO/fastapi-web:alpine
```

### Usuario No-Root

```bash
# Verificar que corre como usuario no-root
docker exec fastapi-app whoami
# Output: fastapi

docker exec fastapi-app id
# Output: uid=1000(fastapi) gid=1000(fastapi) groups=1000(fastapi)
```

---

## 🎯 Selección de Imagen

### ¿Cuál imagen usar?

| Escenario | Imagen Recomendada | Razón |
|-----------|-------------------|-------|
| **Producción** | `alpine` | Menor tamaño (109 MB), más segura |
| **Desarrollo** | `optimized` | Más herramientas debug |
| **Testing** | `alpine` | Builds más rápidos |
| **CI/CD** | `alpine` | Deploy más rápido |
| **ARM64 (M1/M2)** | `alpine` o `optimized` | Multi-arquitectura |
| **Raspberry Pi** | `alpine` | Menor consumo de recursos |

### Tags Disponibles

```bash
# Latest de cada variante
TU-USUARIO/fastapi-web:alpine
TU-USUARIO/fastapi-web:optimized

# Por commit SHA
TU-USUARIO/fastapi-web:alpine-abc1234
TU-USUARIO/fastapi-web:optimized-abc1234

# Por fecha
TU-USUARIO/fastapi-web:alpine-20250122
TU-USUARIO/fastapi-web:optimized-20250122

# Por versión (si usaste tags git)
TU-USUARIO/fastapi-web:v1.0.0-alpine
TU-USUARIO/fastapi-web:v1.0.0-optimized
```

---

## 🧪 Testing y Validación

### Health Check Manual

```bash
# Usando curl
curl -f http://localhost:8000 || exit 1

# Usando Python socket
docker exec fastapi-app python -c \
  "import socket; s=socket.socket(); s.connect(('localhost', 8000)); s.close()"
```

### Load Testing con Apache Bench

```bash
# Instalar Apache Bench
apt-get install apache2-utils  # Debian/Ubuntu
brew install httpd              # macOS

# Test de carga
ab -n 1000 -c 10 http://localhost:8000/
```

### Load Testing con wrk

```bash
# Test durante 30 segundos con 10 conexiones
wrk -t4 -c10 -d30s http://localhost:8000/
```

---

## 🔄 Actualización y Rollback

### Actualizar a Nueva Versión

```bash
# Pull nueva versión
docker pull TU-USUARIO/fastapi-web:alpine

# Detener contenedor actual
docker stop fastapi-app
docker rm fastapi-app

# Ejecutar nueva versión
docker run -d \
  --name fastapi-app \
  -p 8000:8000 \
  TU-USUARIO/fastapi-web:alpine
```

### Rollback a Versión Anterior

```bash
# Usar tag SHA específico
docker pull TU-USUARIO/fastapi-web:alpine-abc1234

docker run -d \
  --name fastapi-app \
  -p 8000:8000 \
  TU-USUARIO/fastapi-web:alpine-abc1234
```

### Blue-Green Deployment

```bash
# Green (nueva versión)
docker run -d \
  --name fastapi-green \
  -p 8001:8000 \
  TU-USUARIO/fastapi-web:alpine

# Test en puerto 8001
curl http://localhost:8001

# Si funciona, cambiar a puerto principal
docker stop fastapi-app
docker rm fastapi-app
docker run -d \
  --name fastapi-app \
  -p 8000:8000 \
  TU-USUARIO/fastapi-web:alpine

# Eliminar green
docker stop fastapi-green
docker rm fastapi-green
```

---

## 🎓 Mejores Prácticas

### ✅ DO (Hacer)

1. **Usar tags específicos** en producción (no `latest`)
2. **Implementar health checks** en todos los despliegues
3. **Limitar recursos** (CPU/memoria) en Kubernetes/ECS
4. **Usar multi-stage builds** (ya implementado)
5. **Escanear vulnerabilidades** regularmente
6. **Mantener logs** con rotación
7. **Usar secrets** para contraseñas, NO variables de entorno
8. **Implementar graceful shutdown**

### ❌ DON'T (No hacer)

1. **NO usar `latest`** en producción
2. **NO ejecutar como root** (ya configurado usuario `fastapi`)
3. **NO hardcodear secrets** en la imagen
4. **NO exponer puertos innecesarios**
5. **NO ignorar actualizaciones** de seguridad
6. **NO usar imágenes sin escaneo** de vulnerabilidades

---

## 📚 Recursos Adicionales

- **Docker Documentation**: https://docs.docker.com/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Kubernetes Docs**: https://kubernetes.io/docs/
- **AWS ECS Guide**: https://docs.aws.amazon.com/ecs/
- **Trivy Security**: https://aquasecurity.github.io/trivy/

---

## 🆘 Troubleshooting

### Contenedor no inicia

```bash
# Ver logs de error
docker logs fastapi-app

# Verificar que el puerto no está en uso
netstat -an | grep 8000  # Linux/Mac
netstat -an | findstr 8000  # Windows

# Ejecutar en modo interactivo para debug
docker run -it --rm -p 8000:8000 TU-USUARIO/fastapi-web:alpine sh
```

### Puerto ya en uso

```bash
# Usar otro puerto host
docker run -d -p 8080:8000 TU-USUARIO/fastapi-web:alpine

# O detener el proceso que usa el puerto
# Linux/Mac
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Imagen no encontrada

```bash
# Verificar que el nombre es correcto
docker images | grep fastapi-web

# Pull explícito
docker pull TU-USUARIO/fastapi-web:alpine
```

---

**¡Disfruta de tu aplicación FastAPI Dockerizada! 🚀**
