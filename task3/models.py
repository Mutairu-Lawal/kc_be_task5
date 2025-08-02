from pydantic import BaseModel, Field


class JobApplication(BaseModel):
    name: str = Field(..., example="Alice Doe")
    company: str = Field(..., example="Google")
    position: str = Field(..., example="Backend Engineer")
    status: str = Field(..., example="pending")
