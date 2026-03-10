#Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from datetime import datetime

#Inicializar API
app = FastAPI(
    title="API de sistema de Reservas Hospedaje",
    version = "1.0.0"
)

#BD ficticia
reservas = {
    1: {"id": 1, "huesped": "Roberto", "fecha de entrada": "2024-06-01","fecha de salida": "2024-06-02" ,"habitacion": "101", "tipo de habitacion": "sencilla", "estancia": "6 dias"},
    2: {"id": 2, "huesped": "Diego", "fecha de entrada": "2024-06-02", "fecha de salida": "2024-06-03", "habitacion": "102", "tipo de habitacion": "doble", "estancia": "4 dias"},
    3: {"id": 3, "huesped": "Julian", "fecha de entrada": "2024-06-03", "fecha de salida": "2024-06-04", "habitacion": "103", "tipo de habitacion": "suite", "estancia": "7 dias"},
}

#Modelos
class crear_reserva(BaseModel):
    id:int = Field(..., gt=0, description="Identificador de usuario")
    fecha_de_entrada: str = Field(..., gt=datetime.now().strftime("%Y-%m-%d"), description="Fecha de entrada en formato YYYY-MM-DD")
    fecha_de_salida: str = Field(..., gt=fecha_de_entrada, description="Fecha de salida en formato YYYY-MM-DD")
    huesped:str = Field(..., min_length=5, max_length=50, example="Ricardo")
    estancia:int = Field(..., ge=1,le=7, description="Estancia en dias")

#Seguridad HTTP BASIC
seguridad = HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(seguridad)):
    userAuth = secrets.compare_digest(credenciales.username, "hotel")
    passAuth = secrets.compare_digest(credenciales.password, "r2026")

    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas"
        )
    return credenciales.username

#Endpoints

@app.post("/v1/reservas", tags=["Reservas"])
async def crear_reserva(reserva: crear_reserva, username: str = Depends(verificar_peticion)):
    if reserva.id in reservas:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reserva con este ID ya existe")
    reservas[reserva.id] = reserva.dict()
    return {
        "status":"201",
        "reserva": reservas[reserva.id]
    }

@app.get("/v1/listar_reservas", tags=["Reservas"])
async def listar_reservas():
    return {
        "status":"200",
        "total":len(reservas),
        "data": reservas
    }

@app.get("/v1/reservas/{id}", tags=["Reservas"])
async def reserva_por_id(id:int):
    if id in reservas:
        return {
            "status":"200",
            "reserva": reservas[id]
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
    
#Confirmar reserva
@app.get("/v1/reservas/{id}/confirmar", tags=["Reservas"])
async def confirmar_reserva(id:int):
    if id in reservas:
        reserva = reservas[id]
        return {
            "status":"200",
            "mensaje": f"Reserva confirmada para {reserva['huesped']} del {reserva['fecha_de_entrada']} al {reserva['fecha_de_salida']} en la habitacion {reserva['habitacion']} ({reserva['tipo de habitacion']})"
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
    
#Cancelar reserva
@app.delete("/v1/reservas/{id}", tags=["Reservas"])
async def cancelar_reserva(id:int):
    if id in reservas:
        del reservas[id]
        return {
            "status":"200",
            "mensaje": f"Reserva con ID {id} cancelada exitosamente"
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")