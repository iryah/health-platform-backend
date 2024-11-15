from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .api import router

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
   title="Health Platform API",
   description="Sağlık Değerlendirme ve Yönlendirme Platformu",
   version="1.0.0"
)

# CORS ayarları 
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"]
)

# Ana sayfa
@app.get("/")
def read_root():
   return {"message": "Health Platform API"}

# Health check endpoint'i
@app.get("/health")
async def health_check():
   return {"status": "healthy"}

# API router'ını dahil et
app.include_router(router, prefix="/api")
