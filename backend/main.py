from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.check_ins import router as check_in_router
from routes.mission import router as mission_router
from routes.auth import router as auth_router
from routes.preferences import router as preferences_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(check_in_router)
app.include_router(mission_router)
app.include_router(auth_router)
app.include_router(preferences_router)


@app.get("/")
def root():
    return {
        "message": "Hello from Asahi"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }