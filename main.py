from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI()

# Mount static files (icons/images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Home page with form
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Handle form submission
@app.post("/", response_class=HTMLResponse)
async def calculate(request: Request, energy_kwh: float = Form(...)):
    # Send request to your local API
    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8001/calculate", json={"energy_kwh": energy_kwh})

    results = response.json()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": results,
        "energy_kwh": energy_kwh
    })
