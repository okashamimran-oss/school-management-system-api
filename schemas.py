from datetime import date
from pydantic import BaseModel,Field
from typing import Literal
class StudentCreate(BaseModel):
    name :  str
    age :int
    marks:int
    class_id: int|None = None
    section_id: int|None = None

class StudentResponse(BaseModel):
    id:int
    name: str
    age: int
    marks:int
    class_id: int|None = None
    section_id: int|None = None

    class Config:
        from_attributes = True


class CourseCreate(BaseModel):
    name : str 
    duration : str

class CourseResponse(BaseModel):
    id : int 
    name :str
    duration: str

    class Config:
        from_attributes = True

class SchoolClassCreate(BaseModel):
    name:str

class SchoolClassResponse(BaseModel):
    id:int
    name:str

    class Config:
        from_attributes = True


class SectionCreate(BaseModel):
    name : str
    class_id: int

class SectionResponse(BaseModel):
    id : int
    name: str
    class_id:int

    class Config:
        from_attributes = True


class TeacherCreate(BaseModel):
    name : str
    phone: str
    email: str

class TeacherResponse(BaseModel):
    id : int
    name: str
    phone:str
    email: str

    class Config:
        from_attributes = True

class TeacherCourseCreate(BaseModel):
    teacher_id: int
    course_id:int


class ParentCreate(BaseModel):
    name : str
    phone: str
    email: str
    student_id:int

class ParentResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    students: list[StudentResponse] = []

    class Config:
        from_attributes = True
    
# Student ki basic information
class StudentInfo(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class FeeCreate(BaseModel):
    amount: int
    paid_amount: int = 0
    student_id: int

class FeeResponse(BaseModel):
    id: int
    amount: int
    paid_amount: int
    status: str
    student_id: int
    student: StudentInfo

    class Config:
        from_attributes = True

# Attendance create/update karte waqt
class AttendanceCreate(BaseModel):
    student_id: int
    date: date
    status: Literal["Present", "Absent", "Late", "Leave"]
 
# Attendance GET/POST response
class AttendanceResponse(BaseModel):
    id: int
    date: date
    status: str
    student: StudentInfo

    class Config:
        from_attributes = True

class CourseInfo(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ExamResultCreate(BaseModel):
    student_id: int
    course_id: int
    exam_name: str
    marks: int = Field(ge=0,le=100)


class ExamResultResponse(BaseModel):
    id: int
    exam_name: str
    marks: int
    grade: str

    student: StudentInfo
    course: CourseInfo

    class Config:
        from_attributes = True

class ParentInfo(BaseModel):
    id: int
    name: str

class ParentMeetingCreate(BaseModel):
    parent_id: int
    student_id: int
    meeting_date: date
    purpose: str


class ParentMeetingResponse(BaseModel):
    id: int
    meeting_date: date
    purpose: str
    parent: ParentInfo
    student: StudentInfo

    class Config:
        from_attributes = True

from typing import Literal

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: Literal["admin", "teacher", "user"] = "user"


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email:str
    password:str