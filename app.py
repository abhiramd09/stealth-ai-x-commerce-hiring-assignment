import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from pymongo import MongoClient

from models.request_model import RequestBody, ResponseBody, AIResponse
from services.google_gemini_api import scrape_product_details_with_ai
from services.google_search import get_search_query_urls
from utils.validation_utils import validate_google_gemini_response

app = FastAPI()
app.state.mongo_client = MongoClient("mongodb://mongodb:27017/")

# In your endpoint
def get_db():
    return app.state.mongo_client["google-gemini-model-history-db"]

@app.get("/post-endpoint", response_model=ResponseBody)
async def handle_post(request_body: RequestBody, db_client=Depends(get_db)):
    try:
        request_response = []
        query_product = request_body.query
        query_country = request_body.country
        num_of_urls = 7  # Default number of URLs to scrape
        while len(request_response) == 0 and num_of_urls != 1:
            num_of_urls -= 1
            product_urls = get_search_query_urls(query_product, query_country, num_of_urls)
            gemini_responses = scrape_product_details_with_ai(product_urls, query_country, db_client, app.state.model_history)
            for each_response in gemini_responses:
                if validate_google_gemini_response(each_response):
                    ai_response = AIResponse(
                        link=each_response["link"],
                        price=each_response["price"],
                        currency=each_response["currency"],
                        productName=each_response["productName"]
                    )
                    request_response.append(ai_response)
        return ResponseBody(
            product_details=request_response
        )
    except Exception as e:
        return HTTPException(status_code=e.status_code if hasattr(e, 'status_code') else 500,)

if __name__ == "__main__":

    # MongoDB connection
    client = MongoClient("mongodb://mongodb:27017/")
    db_name = "google-gemini-model-history-db"
    if db_name not in client.list_database_names():
        db = client[db_name]  # This will create the db on first insert
    else:
        db = client[db_name]

    # Create collection if it doesn't exist
    collection_name = "gemini-2.5-flash-lite-preview-06-17"
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
    database = client["google-gemini-model-history-db"]
    db_collection = database["gemini-2.5-flash-lite-preview-06-17"]
    app.state.model_history = list(db_collection.find({}))
    uvicorn.run(app, host='0.0.0.0', port=8000)