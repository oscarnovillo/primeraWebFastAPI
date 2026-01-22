# ✅ Checklist Pre-Push: GitHub CI/CD

Usa este checklist antes de hacer push para asegurar que el pipeline de CI/CD funcionará correctamente.

---

## 🔐 1. Docker Hub - Configuración

### Access Token
- [ ] Token generado en Docker Hub
- [ ] Permisos configurados: `Read, Write, Delete`
- [ ] Token copiado y guardado de forma segura
- [ ] Nombre sugerido: `GitHub Actions - primeraWebFastAPI`

### Repositorio (Opcional)
- [ ] Repositorio creado en Docker Hub con nombre `fastapi-web`
- [ ] Visibilidad configurada (Public/Private)
- [ ] O: Permitir auto-creación en primer push

**URL de verificación:** https://hub.docker.com/

---

## 🔑 2. GitHub - Secrets

### Secrets Configurados
- [ ] `DOCKERHUB_USERNAME` - Nombre de usuario de Docker Hub
- [ ] `DOCKERHUB_TOKEN` - Access Token (NO contraseña)

### Verificar en GitHub
1. [ ] Ir a: `Settings` → `Secrets and variables` → `Actions`
2. [ ] Verificar que ambos secrets existen
3. [ ] Verificar nombres exactos (case-sensitive)

**Path:** `tu-repo/settings/secrets/actions`

---

## 📁 3. Archivos del Proyecto

### Dockerfiles
- [ ] `Dockerfile` presente
- [ ] `Dockerfile.alpine` presente
- [ ] `Dockerfile.simple` presente (opcional)
- [ ] `.dockerignore` configurado

### CI/CD
- [ ] `.github/workflows/docker-ci-cd.yml` presente
- [ ] Workflow sintácticamente correcto (YAML válido)

### Documentación
- [ ] `README.md` actualizado
- [ ] `README-DOCKER.md` presente
- [ ] `INICIO-RAPIDO-CICD.md` presente
- [ ] Otros docs presentes

### Aplicación
- [ ] `requirements.txt` actualizado
- [ ] `main.py` funcional
- [ ] Templates en `/templates` presentes
- [ ] Static files en `/static` presentes

---

## 🔀 4. Git - Configuración

### Repositorio
- [ ] Remote `origin` configurado
  ```powershell
  git remote -v
  ```
- [ ] URL correcta apuntando a GitHub
- [ ] Credenciales de GitHub configuradas

### Rama
- [ ] Rama actual es `main` o `master`
  ```powershell
  git branch --show-current
  ```
- [ ] Workflow configurado para ejecutarse en esta rama

### Estado
- [ ] Todos los archivos añadidos
  ```powershell
  git status
  ```
- [ ] Sin archivos importantes sin rastrear
- [ ] `.gitignore` configurado correctamente

---

## 🧪 5. Validación Local (Opcional)

### Docker Local
- [ ] `docker build -f Dockerfile -t test:optimized .` funciona
- [ ] `docker build -f Dockerfile.alpine -t test:alpine .` funciona
- [ ] `docker run -p 8000:8000 test:alpine` funciona
- [ ] App accesible en http://localhost:8000

### Python Local
- [ ] `python main.py` ejecuta sin errores
- [ ] Dependencias instaladas correctamente
- [ ] App funciona en http://127.0.0.1:8000

---

## 📝 6. Workflow - Configuración

### Variables de Entorno
- [ ] `DOCKER_IMAGE_NAME` configurado en workflow
- [ ] Valor por defecto: `fastapi-web`
- [ ] Cambiado si deseas otro nombre

### Matrix Strategy
- [ ] `Dockerfile` incluido en matriz
- [ ] `Dockerfile.alpine` incluido en matriz
- [ ] Tags configurados: `optimized` y `alpine`

### Triggers
- [ ] Configurado para rama `main`
- [ ] (Opcional) Configurado para tags `v*.*.*`
- [ ] (Opcional) Configurado para PRs

---

## 🎯 7. Checklist de Commits

### Mensajes de Commit
- [ ] Mensaje descriptivo y claro
- [ ] Prefijo semántico (opcional):
  - `feat:` para nuevas características
  - `fix:` para correcciones
  - `docs:` para documentación
  - `chore:` para tareas de mantenimiento

### Ejemplo Recomendado
```powershell
git commit -m "feat: activar CI/CD con GitHub Actions para Docker Hub"
```

---

## 🚀 8. Pre-Push Validation

### Ejecutar Script de Validación
```powershell
.\validate-cicd.ps1
```

### Verificar Output
- [ ] ✅ Sin errores críticos
- [ ] ⚠️ Advertencias revisadas (si las hay)
- [ ] 📊 Tamaños de contexto razonables

---

## 📤 9. Push Final

### Comandos
```powershell
# Verificar estado
git status

# Añadir archivos (si no están añadidos)
git add .

# Commit
git commit -m "feat: activar CI/CD con GitHub Actions"

# Push
git push origin main
```

### Después del Push
- [ ] Ir a pestaña `Actions` en GitHub
- [ ] Verificar que el workflow se ejecuta
- [ ] Monitorear progreso (tarda ~3-5 minutos)

---

## 🔍 10. Verificación Post-Deploy

### GitHub Actions
- [ ] Pipeline completado exitosamente (✅ verde)
- [ ] Job 1: Build and Test - Pasado
- [ ] Job 2: Docker Build and Push - Pasado
- [ ] Job 3: Security Scan - Pasado
- [ ] Sin errores en logs

### Docker Hub
- [ ] Imágenes visibles en Docker Hub
- [ ] Tags correctos:
  - `optimized`, `optimized-<sha>`, `optimized-YYYYMMDD`
  - `alpine`, `alpine-<sha>`, `alpine-YYYYMMDD`
- [ ] Tamaños correctos (~201 MB optimized, ~109 MB alpine)
- [ ] Arquitecturas: AMD64 y ARM64

### GitHub Security
- [ ] Ir a pestaña `Security`
- [ ] Verificar escaneo de Trivy completado
- [ ] Revisar vulnerabilidades (si las hay)

---

## ✨ 11. Prueba Final

### Descargar Imagen
```powershell
docker pull TU-USUARIO/fastapi-web:alpine
```

### Ejecutar Contenedor
```powershell
docker run -d -p 8000:8000 --name test-cicd TU-USUARIO/fastapi-web:alpine
```

### Verificar
```powershell
# Verificar que responde
curl http://localhost:8000

# O abrir en navegador
start http://localhost:8000
```

### Limpiar
```powershell
docker stop test-cicd
docker rm test-cicd
```

---

## 🎊 Checklist Completo

**Si todos los items están marcados:**

✅ ¡Estás listo para hacer push y activar el CI/CD!

**Si falta alguno:**

⚠️ Revisa la sección correspondiente antes de continuar

---

## 📚 Recursos de Ayuda

| Problema | Solución |
|----------|----------|
| Secrets no configurados | Ver `.github/GITHUB-ACTIONS-SETUP.md` sección 2 |
| Workflow con errores | Verificar sintaxis YAML en línea |
| Docker build falla localmente | Revisar `README-DOCKER.md` |
| Git remote no configurado | `git remote add origin URL` |
| Pipeline falla en GitHub | Revisar logs en tab Actions |

---

## 🆘 Troubleshooting Rápido

### Error: "Invalid username or password"
**Causa:** Secret `DOCKERHUB_TOKEN` incorrecto  
**Solución:** Regenerar Access Token en Docker Hub

### Error: "Repository not found"
**Causa:** Repo no existe en Docker Hub  
**Solución:** Crear manualmente o permitir auto-creación

### Error: "Permission denied"
**Causa:** Token sin permisos Write  
**Solución:** Regenerar con permisos completos

### Pipeline no se ejecuta
**Causa:** Rama incorrecta o workflow deshabilitado  
**Solución:** Verificar rama y habilitar Actions en GitHub

---

## 📝 Notas Finales

- **Primera ejecución:** Tardará ~5 minutos (descarga imágenes base)
- **Siguientes:** ~1-2 minutos (usa caché)
- **Tags SHA:** Útiles para rollbacks precisos
- **Multi-arch:** Funciona en Mac M1/M2 y Raspberry Pi

---

## ✅ Estado Final

Una vez que todo esté verificado:

```
┌─────────────────────────────────────┐
│  ✅ Docker Hub configurado          │
│  ✅ GitHub Secrets configurados     │
│  ✅ Archivos del proyecto listos    │
│  ✅ Git configurado correctamente   │
│  ✅ Validación local exitosa        │
│  ✅ Workflow verificado             │
│  ✅ Listo para PUSH                 │
└─────────────────────────────────────┘
```

**Comando final:**

```powershell
git push origin main
```

**🎉 ¡El pipeline se ejecutará automáticamente!**

---

**Creado:** 2025-01-22  
**Versión:** 1.0.0  
**Proyecto:** primeraWebFastAPI
