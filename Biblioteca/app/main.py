# Importaciones
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# Inicialización API
app = FastAPI(
    title="Biblioteca Digital",
    description="Roberto Carlos Rangel Rodriguez",
    version="v1.0.0"
)

# MODELOS
class Usuario(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    correo: EmailStr


class Libro(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    autor: str = Field(min_length=2, max_length=100)
    año: int = Field(gt=1450, le=datetime.now().year)
    paginas: int = Field(gt=1)
    estado: str = Field(default="disponible", pattern="^(disponible|prestado)$")


class Prestamo(BaseModel):
    usuario: Usuario
    nombre_libro: str

# BASE DE DATOS TEMPORAL
lista_libros = []
lista_prestamos = []

# ENDPOINTS

# Registrar libro
@app.post("/v1/libros", status_code=201, tags=["Libros"])
async def agregar_libro(libro: Libro):

    for libro_guardado in lista_libros:
        if libro_guardado.nombre.lower() == libro.nombre.lower():
            raise HTTPException(
                status_code=400,
                detail="Ese libro ya está registrado"
            )

    lista_libros.append(libro)
    return {"mensaje": "Libro agregado correctamente", "libro": libro}


# Listar libros
@app.get("/v1/libros", tags=["Libros"])
async def ver_libros():
    return {
        "total_libros": len(lista_libros),
        "libros": lista_libros
    }


# Buscar libro por nombre
@app.get("/v1/libros/{nombre}", tags=["Libros"])
async def buscar_libro(nombre: str):

    for libro in lista_libros:
        if libro.nombre.lower() == nombre.lower():
            return libro

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


# Registrar préstamo
@app.post("/v1/prestamos", tags=["Prestamos"])
async def hacer_prestamo(datos: Prestamo):

    for libro in lista_libros:
        if libro.nombre.lower() == datos.nombre_libro.lower():

            if libro.estado == "prestado":
                raise HTTPException(
                    status_code=409,
                    detail="El libro ya está prestado"
                )

            libro.estado = "prestado"
            lista_prestamos.append(datos)

            return {"mensaje": "Préstamo realizado correctamente"}

    raise HTTPException(
        status_code=404,
        detail="El libro no existe"
    )


# Devolver libro
@app.put("/v1/prestamos/devolver/{nombre_libro}", tags=["Prestamos"])
async def devolver_libro(nombre_libro: str):

    for libro in lista_libros:
        if libro.nombre.lower() == nombre_libro.lower():

            if libro.estado == "disponible":
                raise HTTPException(
                    status_code=409,
                    detail="El libro ya estaba disponible"
                )

            libro.estado = "disponible"
            return {"mensaje": "Libro devuelto correctamente"}

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


# Eliminar préstamo
@app.delete("/v1/prestamos/{nombre_libro}", tags=["Prestamos"])
async def borrar_prestamo(nombre_libro: str):

    for i, prestamo in enumerate(lista_prestamos):
        if prestamo.nombre_libro.lower() == nombre_libro.lower():

            lista_prestamos.pop(i)
            return {"mensaje": "Registro de préstamo eliminado"}

    raise HTTPException(
        status_code=409,
        detail="El préstamo ya no existe"
    )