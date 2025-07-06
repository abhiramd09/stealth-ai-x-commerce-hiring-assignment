import json
from typing import Any

import google.generativeai as genai
from google.generativeai.types import GenerationConfigDict

from configs.config import GEMINI_API_KEY, GEMINI_MODEL_NAME, GEMINI_MODEL_RESPONSE_MIME_TYPE, GEMINI_MODEL_TEMPERATURE

genai.configure(api_key=GEMINI_API_KEY)
generation_config = GenerationConfigDict(
    temperature=GEMINI_MODEL_TEMPERATURE,
    response_mime_type=GEMINI_MODEL_RESPONSE_MIME_TYPE
)
model = genai.GenerativeModel(
    model_name=GEMINI_MODEL_NAME,
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

def scrape_product_details_with_ai(
        product_urls: list, query_location: str, history: list, db_collection: Any) -> dict:
    """
    Scrape product details using Google Gemini AI.

    :param product_urls:
    :param query_location:
    :param history:
    :param db_collection:
    :return:
    """
    try:
        prompt = PROMPT.format(queryLocation=query_location, listOfQueryUrls=product_urls)
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(prompt)
        print(f"Response from Gemini: {response.text}")
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
        print(f"Updated model history with recent interaction.")
        return json.loads(response.text)
    except Exception as e:
        raise Exception(f"Failed to scrape product details: {str(e)}")
