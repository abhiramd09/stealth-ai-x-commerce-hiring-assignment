from pydantic import BaseModel


class RequestBody(BaseModel):
    country: str
    query: str

class AIResponse(BaseModel):
    link: str
    price: str
    currency: str
    productName: str

class ResponseBody(BaseModel):
    product_details: list[AIResponse]