from typing import Union

from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio


app = FastAPI()
#app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

counter_lock = asyncio.Lock()
counter = 0


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"likes": counter}
    )

@app.post("/click/like")
async def read_item():
    global counter

    async with counter_lock:
        counter += 1

    return counter

@app.post("/click/unlike")
async def read_item():
    global counter

    async with counter_lock:
        counter -= 1
    
    return counter

