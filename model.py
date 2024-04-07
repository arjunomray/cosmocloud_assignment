from pydantic import BaseModel
from typing import Optional


class Address(BaseModel):
    city: str
    country: str


class Student(BaseModel):
    name: str
    age: int
    address: Address


class AddressUpdate(Address):
    city: Optional[str] = None
    country: Optional[str] = None

class StudentUpdate(Student):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[AddressUpdate] = None
