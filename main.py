from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from model import Student, StudentInDB
from database import collection
from bson.objectid import ObjectId

app = FastAPI()

origins = ['https://cosmocloud-assignment.onrender.com/',"*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def index():
    return {
        "message": "Welcome to the API",
    }


@app.post("/students", response_model=StudentInDB)
async def add_students(student: Student):
    res = await collection.insert_one(student.dict())
    student_in_db = await collection.find_one({"_id": res.inserted_id})
    return StudentInDB(**student_in_db)


@app.get("/students", response_model=List[StudentInDB])
async def get_students(country: Optional[str] = None, age: Optional[int] = None):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}
    students = await collection.find(query).to_list(100)
    return [StudentInDB(**student) for student in students]


@app.get("/students/{id}", response_model=StudentInDB)
async def get_one_student(_id: str):
    res = await collection.find_one({"_id": ObjectId(_id)})
    if res is None:
        raise HTTPException(status_code=404, detail="Student not found")
    res['_id'] = str(res['_id'])
    return res


@app.patch("/students/{id}", response_model=StudentInDB)
async def update_student(id: str, student: Student):
    res = await collection.update_one({"_id": ObjectId(id)},
                                       {"$set":student.dict()}
                                       )
    if res.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    updated_student = await collection.find_one({"_id": ObjectId(id)})
    updated_student['_id'] = str(updated_student['_id'])
    return Student(**updated_student)


@app.delete("/students/{id}")
async def delete_student(id: str):
    res = await collection.delete_one({"_id": ObjectId(id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted successfully"}