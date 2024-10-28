from pydantic import BaseModel


class ReadProgress(BaseModel):
    top: int
    bottom: int
