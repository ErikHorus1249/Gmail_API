from typing import Union
from fastapi import FastAPI
from invoice import core

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/invoices/{time}")
def read_item(time: int):
    return {"envoices": core(time)}