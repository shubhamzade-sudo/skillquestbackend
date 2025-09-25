# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings

# ✅ updated imports (no more topevaluation)
from app.routers import jd_matching_score, jd_master, employee, snow_employee

app = FastAPI(title=settings.app_name)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://dentsu-skillquest.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ new router names
app.include_router(jd_matching_score.router)
app.include_router(jd_master.router)
app.include_router(employee.router)
app.include_router(snow_employee.router)

@app.get("/health")
def health():
    return {"status": "ok"}
