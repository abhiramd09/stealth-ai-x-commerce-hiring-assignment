def validate_google_gemini_response(response: dict) -> bool:
    """
    Validates the response from Google Gemini API to ensure it contains the required fields.

    Args:
        response (dict): The response from Google Gemini API.

    Returns:
        bool: True if the response is valid, False otherwise.
    """

    if not isinstance(response, dict):
        return False


    if not all(key in response for key in ["link", "price", "currency", "productName"]):
        return False
    if not isinstance(response["price"], str) or response["price"] is None:
        return False
    if not isinstance(response["currency"], str) or response["currency"] is None:
        return False
    if not isinstance(response["link"], str) or not response["link"].startswith("http"):
        return False
    if not isinstance(response["productName"], str) or response["productName"] is None:
        return False

    return True