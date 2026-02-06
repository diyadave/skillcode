from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, get_engine, get_db
Base.metadata.create_all(bind=get_engine())
from .schemas import ContactCreate
from .crud import create_contact
from .google_sheet import send_to_sheet

app = FastAPI()
from dotenv import load_dotenv
load_dotenv()

# ✅ CORS FIX (THIS IS THE KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5500",
        "http://localhost:5501",
    ],
    allow_credentials=True,
    allow_methods=["*"],   # MUST allow OPTIONS
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.post("/contact")
def submit_contact(data: ContactCreate, db: Session = Depends(get_db)):
    contact = create_contact(db, data)  # ✅ DB always works

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
