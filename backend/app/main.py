from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.upload import router as upload_router


app = FastAPI(
    title="MedExplain AI",
    description="AI-powered medical report explanation system",
    version="1.0.0"
)


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Connect the medical report API
app.include_router(upload_router)


@app.get("/")
def home():
    return {
        "message": "MedExplain AI is running!"
    }