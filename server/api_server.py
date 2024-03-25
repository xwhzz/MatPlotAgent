"""
On-going
"""

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import random
import time
import asyncio
from api_server import mainworkflow
import logging
workspace_base = './workspace'

class Request(BaseModel):
    req_id: int

app = FastAPI()

@app.get("/")
def start():
    return {"message":"test"}

@app.post("/test")
async def test(request: Request):
    st = time.time()
    await mainworkflow(request.req_id)
    ed = time.time()
    logging.info(f"{request.req_id} Time elapsed: {ed-st}")
    return {"message":"success"}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename=f'{workspace_base}/workflow.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    uvicorn.run(app) 