#Importaciones
from fastapi import FastAPI
from app.routers import usuarios, varios

#Inicializaciones api
app = FastAPI(
    title="Mi Primer API",
    description="Roberto Carlos Rangel Rodriguez",
    version="1.0.0"
              )
app.include_router(usuarios.routerU)
app.include_router(varios.routerV)