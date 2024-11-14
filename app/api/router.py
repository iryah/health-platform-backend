from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
async def test_route():
    return {"message": "Router test endpoint çalışıyor"}
