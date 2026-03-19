#Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#Inicializaciones api
app = FastAPI(
    title="Mi Primer API",
    description="Roberto Carlos Rangel Rodriguez",
    version="1.0.0"
              )

# BD ficticia
usuarios=[
    {"id":1,"nombre":"Roberto","edad":"20"},
    {"id":2,"nombre":"Diego","edad":"19"},
    {"id":3,"nombre":"Julian","edad":"20"},
]
#Modelo
class crear_usuario(BaseModel):
    id:int = Field(..., gt=0, description="Identificador de usuario")
    nombre:str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad:int = Field(..., ge=1,le=123, description="Edad del usuario va;ida entre 1 y 123")

#Seguridad HTTP BASIC
seguridad = HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(seguridad)):
    userAuth = secrets.compare_digest(credenciales.username, "ivanisay")
    passAuth = secrets.compare_digest(credenciales.password, "123456")

    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas"
        )
    return credenciales.username


#Endpoint
@app.get("/", tags=["Inicio"])
async def holaMundo():
    return {"mensaje": "Hola mundo FASTAPI"}

@app.get("/v1/bienvenidos", tags=["Inicio"])
async def holaMundo():
    return {"mensaje": "Bienvenidos"}

@app.get("/v1/promedio", tags=["Calificaciones"])
async def promedio():
    await asyncio.sleep(3) #peticion, consultaBD..
    return {
        "Calificacion": "7.5",
        "estatus":"200"
        }

@app.get("/v1/parametroO/{id}", tags=["Parametros"])
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return {
        "Resuktado": "usuario encontrado",
        "Estatus":"200",
        }

@app.get("/v1/usuarios_op/", tags=["Parametro Opcional"])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return { "Usuario encontrado":id, "Datos":usuario}
        return {"Mensaje":"Usuario no encontrado"}
    else:
        return {"Aviso": "No se proporciono Id"}
    
@app.get("/v1/usuarios", tags=["CRUD HTTP"])
async def consultaT():
    return{
        "status":"200",
        "total":len(usuarios),
        "data": usuarios
    }

@app.post("/v1/usuarios", tags=["CRUD HTTP"])
async def crear_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario) 
    return{
        "mensaje": "usuario agregado correctamente",
        "status":"200",
        "usuario":usuario 
    }        

@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(id: str, usuario_act: dict):   
    for index, usuario in enumerate(usuarios):
        if usuario["id"] == id:           
            usuarios[index] = usuario_act           
            return {
                "mensaje": "Usuario actualizado correctamente",
                "status": "200",
                "usuario": usuario_act
            }
    raise HTTPException(
        status_code=404,
        detail="El usuario no fue econtrado"
    )

@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def eliminar_usuario(id: int, userAuth: str = Depends(verificar_peticion)):    
    for index, usuario in enumerate(usuarios):
        if usuario["id"] == id:           
            usuario_elim = usuarios.pop(index)           
            return {
                "mensaje": f"Usuario eliminado por {userAuth}",
                "status": "200",
                "usuario": usuario_elim
            }
    raise HTTPException(
        status_code=404,
        detail="El usuario no fue encontrado"
    )