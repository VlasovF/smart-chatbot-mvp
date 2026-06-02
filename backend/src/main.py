from fastapi import FastAPI

app = FastAPI(title="Smart Chatbot MVP", version="0.1.0")


@app.get("/")
async def root():
    return {"message": "Smart Chatbot API is running"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
