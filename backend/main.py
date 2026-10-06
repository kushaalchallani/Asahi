from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

check_ins=[]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/check-ins")
def create_check_in(feeling: str):
    check_in={
        "feelings": feeling,
        "created_at": datetime.now().isoformat()
    }
    check_ins.append(check_ins)

    return check_in

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