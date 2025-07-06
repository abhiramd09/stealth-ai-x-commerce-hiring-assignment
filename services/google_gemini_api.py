import json
from typing import Any

import google.generativeai as genai
from google.generativeai.types import GenerationConfigDict

genai.configure(api_key="AIzaSyBSfnmiVwjmYa-UyTVGheYbtfiqAn_JpYI")
generation_config = GenerationConfigDict(
    temperature=0,
    response_mime_type="application/json"
)
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash-lite-preview-06-17',
    generation_config=generation_config,
    system_instruction='You are a web scraping expert. Your task is to scrape the product details from the provided URL.'
)
PROMPT = """
You are a web scraping expert in {queryLocation}."
scrape the product name and price from the following list of url's: {listOfQueryUrls}
**Response Format**:
Strictly return the response in a list of valid JSON format with the following keys, each JSON object represents each url
The order of the JSON objects in the list must be in ascending order of price.
1. link: The url in the list of urls for which the product details are scraped
2. price: Price  of the displayed product
3. currency: The currency of the price, must be in text not in symbol
4. productName: The name of the product
"""

def scrape_product_details_with_ai(product_urls: list, query_location: str, db_client: Any, history: list) -> dict:
    try:
        database = db_client["google-gemini-model-history-db"]
        db_collection = database["gemini-2.5-flash-lite-preview-06-17"]
        prompt = PROMPT.format(queryLocation=query_location, listOfQueryUrls=product_urls)
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(prompt)
        history.append({"role": "user", "parts": [prompt]})
        db_collection.insert_one({
            "role": "user",
            "parts": [prompt]
        })
        history.append({"role": "model", "parts": [response.text]})
        db_collection.insert_one({
            "role": "model",
            "parts": [response.text]
        })
        return json.loads(response.text)
    except Exception as e:
        raise Exception(f"Failed to scrape product details: {str(e)}")
