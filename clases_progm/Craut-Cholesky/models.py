from pydantic import BaseModel

class MatrixRequest(BaseModel):
    A: list[list[float]]
    b: list[float]