import subprocess
from tempfile import template
import uvicorn

from fastapi import FastAPI, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from fastapi_tailwind import tailwind

from app.models import Base
from app.database import engine
from app.routers import pzem, aht10

# Run Alembic migrations before starting the server
def run_migrations():
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("✅ Alembic migrations applied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Alembic migration failed: {e}")
        exit(1)  # Stop execution if migration fails

run_migrations()  # Ensure DB is up to date

Base.metadata.create_all(bind=engine)

static_files = StaticFiles(directory="app/static")

@asynccontextmanager
async def lifespan(app: FastAPI):
    process = tailwind.compile(static_files.directory + "/css/output.css", watch=True)
    
    yield
    
    process.terminate()

app = FastAPI(
    lifespan=lifespan
)

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", static_files, name="static")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

app.include_router(pzem.router)
app.include_router(aht10.router)

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()