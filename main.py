pip install fastapi uvicorn sqlalchemy pandas requests python-multipart

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import pandas as pd
import os


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Database Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./stocks.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Watchlist(Base):
    __tablename__ = "watchlist"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True)

Base.metadata.create_all(bind=engine)

# Alpha Vantage API
API_KEY = "YOUR_API_KEY"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search")
async def search_stock(symbol: str = Form(...)):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    data = requests.get(url).json()
    return data.get("Global Quote", {})

@app.post("/historical")
async def historical_data(symbol: str = Form(...)):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=full"
    data = requests.get(url).json()
    return data.get("Time Series (Daily)", {})

# Watchlist Endpoints
@app.post("/watchlist/add")
async def add_to_watchlist(symbol: str = Form(...)):
    db = SessionLocal()
    db.add(Watchlist(symbol=symbol))
    db.commit()
    return {"message": "Added to watchlist"}

@app.get("/watchlist")
async def get_watchlist():
    db = SessionLocal()
    return db.query(Watchlist).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
