from pydantic import BaseModel


class CallbackResponse(BaseModel):
    access_token: str
    token_type: str