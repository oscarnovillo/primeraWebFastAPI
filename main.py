from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
import uvicorn

# Crear la aplicación FastAPI
app = FastAPI(title="Mi Primera Web FastAPI", description="Ejemplo básico con Jinja2")

# Configurar las plantillas
templates = Jinja2Templates(directory="templates")

# Configurar archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Simulamos una base de datos simple en memoria
usuarios_db = []
productos_db = [
    {"id": 1, "nombre": "Portátil", "precio": 899.99, "categoria": "Tecnología"},
    {"id": 2, "nombre": "Mesa", "precio": 199.50, "categoria": "Muebles"},
    {"id": 3, "nombre": "Libro", "precio": 15.99, "categoria": "Educación"},
]

# RUTAS GET

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    """Página de inicio"""
    return templates.TemplateResponse("inicio.html", {
        "request": request, 
        "titulo": "Bienvenido a FastAPI",
        "mensaje": "Esta es tu primera aplicación web con FastAPI y Jinja2"
    })

@app.get("/navegacion", response_class=HTMLResponse)
async def navegacion(request: Request):
    """Página de navegación con enlaces"""
    return templates.TemplateResponse("navegacion.html", {"request": request})

@app.get("/productos", response_class=HTMLResponse)
async def listar_productos(request: Request, categoria: Optional[str] = None):
    """Página de productos con filtro opcional por categoría (parámetro GET)"""
    productos_filtrados = productos_db
    
    if categoria:
        productos_filtrados = [p for p in productos_db if p["categoria"].lower() == categoria.lower()]
    
    categorias = list(set([p["categoria"] for p in productos_db]))
    
    return templates.TemplateResponse("productos.html", {
        "request": request,
        "productos": productos_filtrados,
        "categorias": categorias,
        "categoria_seleccionada": categoria
    })

@app.get("/producto/{producto_id}", response_class=HTMLResponse)
async def ver_producto(request: Request, producto_id: int):
    """Ver un producto específico (parámetro en la URL)"""
    producto = next((p for p in productos_db if p["id"] == producto_id), None)
    
    if not producto:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": f"Producto con ID {producto_id} no encontrado"
        })
    
    return templates.TemplateResponse("producto_detalle.html", {
        "request": request,
        "producto": producto
    })

@app.get("/contacto", response_class=HTMLResponse)
async def formulario_contacto(request: Request):
    """Mostrar formulario de contacto"""
    return templates.TemplateResponse("contacto.html", {"request": request})

@app.get("/registro", response_class=HTMLResponse)
async def formulario_registro(request: Request):
    """Mostrar formulario de registro"""
    return templates.TemplateResponse("registro.html", {"request": request})

@app.get("/usuarios", response_class=HTMLResponse)
async def listar_usuarios(request: Request):
    """Listar usuarios registrados"""
    return templates.TemplateResponse("usuarios.html", {
        "request": request,
        "usuarios": usuarios_db
    })

# RUTAS POST

@app.post("/contacto", response_class=HTMLResponse)
async def procesar_contacto(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    mensaje: str = Form(...)
):
    """Procesar formulario de contacto (POST)"""
    # Aquí procesarías el mensaje (enviar email, guardar en BD, etc.)
    return templates.TemplateResponse("contacto_enviado.html", {
        "request": request,
        "nombre": nombre,
        "email": email,
        "mensaje": mensaje
    })

@app.post("/registro", response_class=HTMLResponse)
async def procesar_registro(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    edad: int = Form(...),
    ciudad: str = Form(...),
    intereses: list = Form(...)
):
    """Procesar formulario de registro (POST)"""
    nuevo_usuario = {
        "id": len(usuarios_db) + 1,
        "nombre": nombre,
        "email": email,
        "edad": edad,
        "ciudad": ciudad,
        "intereses": intereses if isinstance(intereses, list) else [intereses]
    }
    
    usuarios_db.append(nuevo_usuario)
    
    return templates.TemplateResponse("registro_exitoso.html", {
        "request": request,
        "usuario": nuevo_usuario
    })

@app.post("/buscar", response_class=HTMLResponse)
async def buscar_productos(
    request: Request,
    termino: str = Form(...),
    precio_min: Optional[float] = Form(None),
    precio_max: Optional[float] = Form(None)
):
    """Buscar productos (POST con múltiples parámetros)"""
    resultados = []
    
    for producto in productos_db:
        # Buscar por nombre
        if termino.lower() in producto["nombre"].lower():
            # Filtrar por precio si se especifica
            if precio_min is not None and producto["precio"] < precio_min:
                continue
            if precio_max is not None and producto["precio"] > precio_max:
                continue
            resultados.append(producto)
    
    return templates.TemplateResponse("buscar_resultados.html", {
        "request": request,
        "resultados": resultados,
        "termino": termino,
        "precio_min": precio_min,
        "precio_max": precio_max
    })

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
