#Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
import asyncio
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

# CONFIGURACIÓN JWT
SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 #30 minutos de expiración para el token

# OAUTH2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

# Usuario de prueba
fake_user = {
    "username": "ivanisay",
    "password": "123456"
}

#Modelo
class crear_usuario(BaseModel):
    id:int = Field(..., gt=0, description="Identificador de usuario")
    nombre:str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad:int = Field(..., ge=1,le=123, description="Edad del usuario va;ida entre 1 y 123")

# CREAR TOKEN
def crear_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# LOGIN (OBTENER TOKEN)
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["username"] or form_data.password != fake_user["password"]:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )
    
    access_token = crear_token({"sub": form_data.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ================= VALIDAR TOKEN =================
def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")
        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

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
async def actualizar(id: int, usuario_act: dict, user: str = Depends(validar_token)):
    for index, usuario in enumerate(usuarios):
        if usuario["id"] == id:
            usuarios[index] = usuario_act
            return {
                "mensaje": f"Usuario actualizado por {user}",
                "usuario": usuario_act
            }
    raise HTTPException(
        status_code=404, 
        detail="Usuario no encontrado"
        )

@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def eliminar(id: int, user: str = Depends(validar_token)):
    for index, usuario in enumerate(usuarios):
        if usuario["id"] == id:
            usuario_elim = usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por {user}",
                "usuario": usuario_elim
            }
    raise HTTPException(status_code=404, 
                        detail="Usuario no encontrado"
                        )