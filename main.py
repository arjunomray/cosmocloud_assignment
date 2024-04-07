from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from model import Student, StudentUpdate
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
        "get started": "add '/docs/' to the url to see all routes in the swagger ui",
        "author": "Arjun Omray"
    }


@app.post("/students")
async def add_students(student: Student):
    res = await collection.insert_one(student.dict())
    student_in_db = await collection.find_one({"_id": res.inserted_id})
    student_in_db["_id"] = str(res.inserted_id)
    return student_in_db


@app.get("/students")
async def get_students(country: Optional[str] = None, age: Optional[int] = None):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}
    students = await collection.find(query).to_list(100)
    for student in students:
        student['_id'] = str(student['_id'])
    return [student for student in students]


@app.get("/students/{id}")
async def get_one_student(_id: str):
    res = await collection.find_one({"_id": ObjectId(_id)})
    if res is None:
        raise HTTPException(status_code=404, detail="Student not found")
    res['_id'] = str(res['_id'])
    return res


@app.patch("/students/{id}", response_model=Student)
async def update_student(id: str, student: StudentUpdate):
    student_in_db = await collection.find_one({"_id": ObjectId(id)})
    if student_in_db is None:
        raise HTTPException(status_code=404,detail="Student fot found")
    student_in_model = Student(**student_in_db)
    update_values = student.model_dump(exclude_unset=True)
    updated_student = student_in_model.model_copy(update=update_values)
    res = await collection.update_one({"_id": ObjectId(id)},
                                      {"$set": jsonable_encoder(updated_student)}
                                      )
    if res.modified_count == 0:
        raise HTTPException(status_code=400, detail="update failed")
    updated_student = await collection.find_one({"_id": ObjectId(id)})
    updated_student['_id'] = str(updated_student['_id'])
    return Student(**updated_student)


@app.delete("/students/{id}")
async def delete_student(id: str):
    res = await collection.delete_one({"_id": ObjectId(id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted successfully"}
