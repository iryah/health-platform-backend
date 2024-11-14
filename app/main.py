from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
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

# Statik dosyalar ve templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Ana sayfa
@app.get("/")
@app.head("/")  # HEAD metodu için endpoint ekledik
def read_root():
   return {"message": "Health Platform API"}

# Health check endpoint'i
@app.get("/health")
async def health_check():
   return {"status": "healthy"}

# API router'ını dahil et
app.include_router(router, prefix="/api")

# Uygulama başlatma bilgisi için
if __name__ == "__main__":
   import uvicorn
   uvicorn.run(app, host="0.0.0.0", port=8000)
