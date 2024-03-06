from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from utils import send_email

app = FastAPI()


class Info(BaseModel):
    hostname: str
    ntp: str
    status: bool


app = FastAPI()


@app.post("/checker/")
async def create_item(item: Info):
    send_email(item.hostname,
               item.ntp,
               item.status)
    return item