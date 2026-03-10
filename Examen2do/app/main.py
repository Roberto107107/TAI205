#Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel, Field, validator
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
    1: {"id": 1, "huesped": "Roberto", "fecha_de_entrada": "2026-03-13","fecha_de_salida": "2026-03-15" ,"habitacion": "101", "tipo_de_habitacion": "sencilla", "estancia": 6},
    2: {"id": 2, "huesped": "Diego", "fecha_de_entrada": "2026-03-10", "fecha_de_salida": "2026-03-14", "habitacion": "102", "tipo_de_habitacion": "doble", "estancia": 4},
    3: {"id": 3, "huesped": "Julian", "fecha_de_entrada": "2026-06-03", "fecha_de_salida": "2026-06-04", "habitacion": "103", "tipo_de_habitacion": "suite", "estancia": 7},
}


#Modelos de datos 
class crear_reserva(BaseModel):
    id:int = Field(..., gt=0, description="Identificador de usuario")
    fecha_de_entrada: str = Field(..., gt=datetime.now().strftime("%Y-%m-%d"), description="Fecha de entrada en formato YYYY-MM-DD")
    fecha_de_salida: str = Field(..., description="Fecha de salida en formato YYYY-MM-DD")
    huesped:str = Field(..., min_length=5, max_length=50, example="Ricardo")
    habitacion: str = Field(..., description="Numero de habitacion")
    tipo_de_habitacion: str = Field(..., description="Tipo de habitacion")
    estancia:int = Field(..., ge=1,le=7, description="Estancia en dias")

    @validator('fecha_de_salida')
    def validate_fecha_salida(cls, v, values):
        entrada = values.get('fecha_de_entrada')
        if entrada and v <= entrada:
            raise ValueError('Fecha de salida debe ser posterior a fecha de entrada')
        return v

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
#Crear reserva con autenticacion
@app.post("/v1/reservas", tags=["Reservas"])
async def crear_reserv(reserva:crear_reserva, UserAuth: str = Depends(verificar_peticion)):
    if reserva.id in reservas:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reserva con este ID ya existe")
    
    reservas[reserva.id] = {
        "id": reserva.id,
        "huesped": reserva.huesped,
        "fecha_de_entrada": reserva.fecha_de_entrada,
        "fecha_de_salida": reserva.fecha_de_salida,
        "habitacion": reserva.habitacion,
        "tipo_de_habitacion": reserva.tipo_de_habitacion,
        "estancia": reserva.estancia
    }
    return {
        "status":"201",
        "mensaje": f"Reserva creada por {UserAuth} exitosamente para {reserva.huesped} del {reserva.fecha_de_entrada} al {reserva.fecha_de_salida} ({reserva.estancia} dias)"
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
            "mensaje": f"Reserva confirmada para {reserva['huesped']} del {reserva['fecha_de_entrada']} al {reserva['fecha_de_salida']} en la habitacion {reserva['habitacion']} ({reserva['tipo_de_habitacion']})"
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
    
#Cancelar reserva con autentificacion
@app.delete("/v1/reservas/{id}", tags=["Reservas"])
async def cancelar_reserva(id:int, UserAuth: str = Depends(verificar_peticion)):
    if id in reservas:
        del reservas[id]
        return {
            "status":"200",
            "mensaje": f"Reserva cancelada por {UserAuth} cancelada exitosamente"
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")