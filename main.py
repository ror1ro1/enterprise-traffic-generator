import asyncio
import json
import logging
import random
import uuid
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from faker import Faker
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse

# Konfiguracja logowania systemowego
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)
fake = Faker()

app = FastAPI(title="Enterprise Traffic Generator API")

PAYMENT_METHODS = ["ALLEGRO_PAY_LATER", "ALLEGRO_PAY_INSTALLMENTS", "BLIK", "CARD"]
GENERATOR_STATUS = {"active": False, "events_generated": 0}

class TransactionEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    user_id: str
    amount: float
    payment_method: str
    status: str
    ip_address: str

async def traffic_loop():
    """Pętla generująca ruch działająca asynchronicznie w tle."""
    while GENERATOR_STATUS["active"]:
        is_fraud = random.random() < 0.05
        amount = round(random.uniform(5000.0, 15000.0), 2) if is_fraud else round(random.uniform(10.0, 1200.0), 2)
        
        event = TransactionEvent(
            user_id=f"USR-{random.randint(10000, 99999)}",
            amount=amount,
            payment_method=random.choice(PAYMENT_METHODS),
            status="SUSPICIOUS" if is_fraud else "SUCCESS",
            ip_address=fake.ipv4()
        )
        
        logger.info(f"LIVE_STREAM: {event.model_dump_json()}")
        GENERATOR_STATUS["events_generated"] += 1
        await asyncio.sleep(0.5)

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Interfejs panelu kontrolnego widoczny w przeglądarce."""
    status_color = "green" if GENERATOR_STATUS["active"] else "red"
    status_text = "RUNNING" if GENERATOR_STATUS["active"] else "STOPPED"
    
    html_content = f"""
    <html>
        <head>
            <title>Allegro Pay Simulation - DevOps Control Panel</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; color: #333; }}
                .card {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }}
                .btn {{ padding: 12px 24px; font-size: 16px; border: none; border-radius: 4px; cursor: pointer; color: white; font-weight: bold; transition: background 0.2s; }}
                .btn-start {{ background-color: #28a745; }}
                .btn-start:hover {{ background-color: #218838; }}
                .btn-stop {{ background-color: #dc3545; margin-left: 10px; }}
                .btn-stop:hover {{ background-color: #c82333; }}
                .status {{ font-weight: bold; color: {status_color}; background: #eee; padding: 4px 8px; border-radius: 4px; }}
                hr {{ border: 0; height: 1px; background: #e0e0e0; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2>FinTech Traffic Producer Control Panel</h2>
                <p>Status systemu: <span class="status">{status_text}</span></p>
                <p>Wygenerowane transakcje: <strong>{GENERATOR_STATUS["events_generated"]}</strong></p>
                <hr>
                <form action="/start" method="post" style="display: inline;">
                    <button type="submit" class="btn btn-start">Uruchom Generator</button>
                </form>
                <form action="/stop" method="post" style="display: inline;">
                    <button type="submit" class="btn btn-stop">Zatrzymaj Generator</button>
                </form>
                <p style="margin-top: 20px;"><small>Odśwież stronę (F5), aby zaktualizować licznik transakcji.</small></p>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/start")
async def start_generator(background_tasks: BackgroundTasks):
    if not GENERATOR_STATUS["active"]:
        GENERATOR_STATUS["active"] = True
        background_tasks.add_task(traffic_loop)
    return {"message": "Generator started", "status": GENERATOR_STATUS}

@app.post("/stop")
async def stop_generator():
    GENERATOR_STATUS["active"] = False
    return {"message": "Generator stopped", "status": GENERATOR_STATUS}
