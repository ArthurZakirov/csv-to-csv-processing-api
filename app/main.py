from fastapi import FastAPI
from app.routes import transform_routes

app = FastAPI(title="CSV Transformer API")

# Include routes
app.include_router(transform_routes.router)