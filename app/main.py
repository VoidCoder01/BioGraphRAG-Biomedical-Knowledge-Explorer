from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import importlib, pkgutil, app.routes

app = FastAPI(title="BioGraphRAG API", version="1.0")

# Allow React frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-register all routers in app/routes/
for _, module_name, _ in pkgutil.iter_modules(app.routes.__path__):
    module = importlib.import_module(f"app.routes.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router)

@app.get("/")
def root():
    return {"message": "BioGraphRAG API running"}
