from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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

# Statik dosyalar için klasör oluşturun ve mount edin
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates için Jinja2 kurulumu
templates = Jinja2Templates(directory="templates")

# Ana sayfa için HTML dönüş
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Health Platform API</title>
            <style>
                body { 
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    line-height: 1.6;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                }
                h1 { color: #333; }
                .api-link {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    background: #007bff;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Health Platform API</h1>
                <p>Hoş geldiniz! Bu API sağlık platformu için hizmet vermektedir.</p>
                <a href="/docs" class="api-link">API Dokümantasyonu</a>
            </div>
        </body>
    </html>
    """

# API router'ı ekleyin
@app.get("/api")
async def read_root():
    return {"message": "Health Platform API"}

# Diğer router'ları dahil edin
app.include_router(router, prefix="/api")
