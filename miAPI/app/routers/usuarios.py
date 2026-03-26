#Importaciones
from fastapi import status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session 
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB

routerU= APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD HTTP']
)

#Endpoint    
@routerU.get("/")
async def consultaT(db: Session=Depends(get_db)):
    queryUsuarios = db.query(usuarioDB).all()
    return{
        "status":"200",
        "total":len(queryUsuarios),
        "data": queryUsuarios
    }

@routerU.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuarioP:crear_usuario, db: Session=Depends(get_db)):

    usuarioNuevo = usuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)
    
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)
    return{
        "mensaje": "usuario agregado correctamente",
        "status":"200",
        "usuario":usuarioP
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