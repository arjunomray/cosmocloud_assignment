from pydantic import BaseModel
from typing import Optional


class Address(BaseModel):
    city: str
    country: str


class Student(BaseModel):
    name: str
    age: int
    address: Address


class StudentInDB(Student):
    id: Optional[str] = None

