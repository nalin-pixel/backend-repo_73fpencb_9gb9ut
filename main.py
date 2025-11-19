import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Coffee Show API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContactMessage(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=1, max_length=1000)


@app.get("/")
def read_root():
    return {"message": "Coffee Show Backend is running"}


@app.post("/api/contact")
async def submit_contact(payload: ContactMessage):
    # For demo purposes we just acknowledge receipt.
    # In a real XAMPP/PHP setup you'd save to MySQL; here we can later extend to MongoDB if needed.
    if not payload.name.strip() or not payload.message.strip():
        raise HTTPException(status_code=400, detail="Invalid data")
    return {"status": "ok", "received": payload.dict()}


@app.get("/test")
def test_database():
    """Simple health check"""
    return {"backend": "running"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
