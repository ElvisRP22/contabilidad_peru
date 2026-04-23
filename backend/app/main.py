from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import create_tables
from app.config import settings
from app.auth.routes import router as auth_router
from app.core.routes import router as core_router
from app.contabilidad.routes import router as contabilidad_router
from app.facturacion.routes import router as facturacion_router
from app.inventario.routes import router as inventario_router
from app.nomina.routes import router as nomina_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="Contabilidad Perú API",
    description="Sistema Contable Peruano - FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(core_router, prefix="/api")
app.include_router(contabilidad_router, prefix="/api")
app.include_router(facturacion_router, prefix="/api")
app.include_router(inventario_router, prefix="/api")
app.include_router(nomina_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Contabilidad Perú API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}