# run.py
import uvicorn
from app.core.settings import settings

def main():
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.reload)

if __name__ == "__main__":
    main()
