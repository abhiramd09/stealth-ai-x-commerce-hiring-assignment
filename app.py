import uvicorn
from fastapi import FastAPI

from models.request_model import RequestBody

app = FastAPI()


@app.post("/post-endpoint")
async def handle_post(request_body: RequestBody):
    response = {
        "message": "Data received successfully",
        "received_data": request_body.dict()
    }
    return response

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)