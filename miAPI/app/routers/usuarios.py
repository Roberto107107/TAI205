#Importaciones
from fastapi import status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

routerU= APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD HTTP']
)

#Endpoint    
@routerU.get("/")
async def consultaT():
    return{
        "status":"200",
        "total":len(usuarios),
        "data": usuarios
    }

@routerU.post("/", status_code=status.HTTP_201_CREATED)
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

@routerU.put("/{id}", status_code=status.HTTP_201_CREATED)
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

@routerU.delete("/{id}", status_code=status.HTTP_200_OK)
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