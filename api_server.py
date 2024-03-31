"""
On-going
"""

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import time
import logging

from async_workflow import mainworkflow
workspace_base = './workspace1'

class Request(BaseModel):
    req_id: int

app = FastAPI()

@app.get("/")
def start():
    return {"message":"test"}

@app.post("/test")
async def test(request: Request):
    st = time.time()
    total_token = await mainworkflow(request.req_id)
    ed = time.time()
    # logging.info(f"{request.req_id} Time elapsed: {ed-st}")
    return {"message":"success", "start": st, "end": ed, "elapsed": ed - st, "req_id": request.req_id, "total_token": total_token}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename=f'{workspace_base}/workflow.log', filemode='w+', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    uvicorn.run(app, port=8002) 