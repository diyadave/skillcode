from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, get_engine, get_db
from .schemas import ContactCreate
from .crud import create_contact
from .google_sheet import send_to_sheet

app = FastAPI()

# 🚫 DO NOT use load_dotenv on Railway
# load_dotenv() ← REMOVE THIS

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5500",
        "http://localhost:5501",
        "https://magical-pasca-09f99a.netlify.app",
        "https://skillcodeai.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ DATABASE INIT (SAFE)
@app.on_event("startup")
def startup():
    engine = get_engine()
    if engine:
        Base.metadata.create_all(bind=engine)

@app.post("/contact")
def submit_contact(data: ContactCreate, db: Session = Depends(get_db)):
    create_contact(db, data)

    try:
        send_to_sheet(
            data.name,
            data.email,
            data.subject,
            data.message
        )
    except Exception as e:
        print("⚠️ Google Sheet failed:", e)

    return {"success": True, "message": "Message saved successfully"}
