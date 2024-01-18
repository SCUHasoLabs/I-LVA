from pydantic import BaseModel
from fastapi import FastAPI
import json

app = FastAPI()

data = json.load(open('sample.json'))