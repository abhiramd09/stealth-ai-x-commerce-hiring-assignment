from pydantic.v1 import BaseModel


class RequestBody(BaseModel):
    country: str
    query: str
