from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Teacher,Course,teacher_courses
from schemas import TeacherCreate, TeacherResponse,TeacherCourseCreate


router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)


# CREATE TEACHER
@router.post("/", response_model=TeacherResponse)
def create_teacher(
    teacher: TeacherCreate,
    db: Session = Depends(get_db)
):
    new_teacher = Teacher(
        name=teacher.name,
        phone=teacher.phone,
        email=teacher.email
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return new_teacher


# GET ALL TEACHERS
@router.get("/", response_model=list[TeacherResponse])
def get_teachers(
    db: Session = Depends(get_db)
):
    teachers = db.query(Teacher).all()

    return teachers


# ASSIGN COURSE TO TEACHER
@router.post("/assign-course")
def assign_course(
    data: TeacherCourseCreate,
    db: Session = Depends(get_db)
):
    teacher = db.query(Teacher).filter(
        Teacher.id == data.teacher_id
    ).first()

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    course = db.query(Course).filter(
        Course.id == data.course_id
    ).first()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    teacher.courses.append(course)

    db.commit()

    return {
        "message": "Course assigned to teacher successfully"
    }



# GET TEACHER BY ID
@router.get("/{teacher_id}", response_model=TeacherResponse)
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db)
):
    teacher = db.query(Teacher).filter(
        Teacher.id == teacher_id
    ).first()

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return teacher


# UPDATE TEACHER
@router.put("/{teacher_id}", response_model=TeacherResponse)
def update_teacher(
    teacher_id: int,
    teacher: TeacherCreate,
    db: Session = Depends(get_db)
):
    existing_teacher = db.query(Teacher).filter(
        Teacher.id == teacher_id
    ).first()

    if existing_teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    existing_teacher.name = teacher.name
    existing_teacher.phone = teacher.phone
    existing_teacher.email = teacher.email

    db.commit()
    db.refresh(existing_teacher)

    return existing_teacher


# DELETE TEACHER
@router.delete("/{teacher_id}")
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db)
):
    teacher = db.query(Teacher).filter(
        Teacher.id == teacher_id
    ).first()

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    db.delete(teacher)
    db.commit()

    return {
        "message": "Teacher deleted successfully"
    }