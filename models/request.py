from pydantic import BaseModel


class SavePassageRequest(BaseModel):
    content: str
    token: str


class PassageRequest(BaseModel):
    action: str
    param: object | None
    token: str
