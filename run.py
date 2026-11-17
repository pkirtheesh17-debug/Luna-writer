import uvicorn
from backend.app.config import settings

if __name__ == "__main__":
    print(f"==================================================")
    print(f"  Starting Luna Writer Server...")
    print(f"  URL: http://{settings.HOST}:{settings.PORT}")
    print(f"  Swagger API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"==================================================")
    uvicorn.run(
        "backend.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
