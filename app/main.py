
# IMPORTS
from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine, Base
from app import models
from app.routers import tasks

# CONFIGURATION
app = FastAPI(
    title="TaskFlow API",
    description="A Task Management REST API",
    version="1.0.0"
)

# DATABASE INITIALIZATION
# Create database tables based on the defined SQLAlchemy models.
Base.metadata.create_all(bind=engine)

# ROUTERS
# Register application routers.
app.include_router(tasks.router)

# GENERAL ENDPOINTS
# ROOT
@app.get("/")
def root():
    return {
        "message": "Welcome to TaskFlow API!",
        "status": "success"
    }

# HEALTH CHECK
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

# ABOUT
@app.get("/about")
def about():
    return {
        "project": "TaskFlow API",
        "version": "1.0.0",
        "description": "Task Management Backend"
    }

# DATABASE CHECK
# Verify the connection between FastAPI and PostgreSQL.
@app.get("/db-check")
def database_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "status": "success"
    }
