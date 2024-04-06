from model import Student
from dotenv import load_dotenv

import os

import motor.motor_asyncio


load_dotenv()
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL"))

database = client.StudentList
collection = database.students
