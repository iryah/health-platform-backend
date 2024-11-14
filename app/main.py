from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api import router

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
   allow_headers=["*"],
)

# Statik dosyalar ve templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Ana sayfa
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
   return templates.TemplateResponse("index.html", {"request": request})

# API root endpoint
@app.get("/api")
async def read_root():
   return {"message": "Health Platform API"}

# Sağlık kontrolü endpoint'i
@app.get("/health")
async def health_check():
   return {"status": "healthy"}

# 404 hata yakalayıcı
@app.exception_handler(404)
async def not_found_error(request: Request, exc):
   return templates.TemplateResponse(
       "error.html",
       {
           "request": request,
           "error_code": "404",
           "error_message": "Sayfa bulunamadı."
       },
       status_code=404
   )

# API router'ını dahil et
app.include_router(router, prefix="/api")

# Uygulama başlatma bilgisi için
if __name__ == "__main__":
   import uvicorn
   uvicorn.run(app, host="0.0.0.0", port=8000)
