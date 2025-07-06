from typing import Union

import uvicorn
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

from configs.config import MONGO_URL, MONGO_DB_NAME, MONGO_COLLECTION_NAME
from models.request_model import RequestBody, ResponseBody, AIResponse
from services.google_gemini_service import scrape_product_details_with_ai
from services.google_search_service import get_search_query_urls
from utils.validation_utils import validate_google_gemini_response

app = FastAPI(
    title="AI Web Scraper",
)

def get_mongo_db_collection():
    """
    Dependency to get the MongoDB collection.
    This can be used in route handlers to access the collection.
    """
    mongo_db_client = MongoClient(MONGO_URL)
    mongo_db_connection = mongo_db_client[MONGO_DB_NAME]
    if MONGO_COLLECTION_NAME not in mongo_db_connection.list_collection_names():
        mongo_db_connection.create_collection(MONGO_COLLECTION_NAME)
    mongo_db_collection = mongo_db_connection[MONGO_COLLECTION_NAME]
    return mongo_db_collection

@app.get("/get-product-details", response_model=ResponseBody)
async def handle_post(
        request_body: RequestBody
) -> Union[ResponseBody, HTTPException]:
    """
    Endpoint to handle product details scraping using Google Gemini AI.

    :param request_body:
    :return:
    """
    try:
        request_response = []
        query_product = request_body.query
        query_country = request_body.country
        num_of_urls = 7  # Default number of URLs to scrape
        while len(request_response) == 0 and num_of_urls != 1:
            num_of_urls -= 1
            product_urls = get_search_query_urls(query_product, query_country, num_of_urls)
            gemini_responses = scrape_product_details_with_ai(
                product_urls, query_country, app.state.model_history, get_mongo_db_collection())
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
        return HTTPException(status_code=e.status_code if hasattr(e, 'status_code') else 500, detail=str(e))

if __name__ == "__main__":
    """
    Main entry point for the FastAPI application.
    """
    mongo_collection = get_mongo_db_collection()
    app.state.model_history = list(mongo_collection.find({}, {'_id': 0}))
    print("Fetched model history from MongoDB before the server starts")
    uvicorn.run(app, host='0.0.0.0', port=8000)