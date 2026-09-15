from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import Student,Course
from schemas import StudentCreate, StudentResponse
from schemas import StudentCreate,StudentResponse,CourseCreate,CourseResponse
from typing import List
from routers import courses,students,classes, teachers,parents,fees,attendance,exams, meetings,auth

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(courses.router)
app.include_router(students.router)
app.include_router(classes.router)
app.include_router(teachers.router)
app.include_router(parents.router)
app.include_router(fees.router)
app.include_router(attendance.router)
app.include_router(exams.router)
app.include_router(meetings.router)
app.include_router(auth.router)
@app.get("/")
def home():
    return {"message": "Student management system api"}
    

