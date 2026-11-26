from fastapi import FastAPI

app = FastAPI(
    title="TaskFlow API",
    description="A Task Management REST API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to TaskFlow API",
        "status": "success"
    }