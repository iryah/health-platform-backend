from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .router import router

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
   title="Health Platform API",
   description="Sağlık Değerlendirme ve Yönlendirme Platformu",
   version="1.0.0"
)

# CORS ayarları - güncellenmiş hali
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Router'ı ekle
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
   return {"message": "Health Platform API"}

@app.get("/health")
def health_check():
   return {"status": "healthy"}
