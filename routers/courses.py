from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Course
from schemas import CourseCreate, CourseResponse

router = APIRouter(prefix="/courses", tags=["Courses"])

# 1. GET ALL COURSES
@router.get("", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

# 2. GET COURSE BY ID
@router.get("/{course_id}", response_model=CourseResponse)
def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found"
        )
    return course

# 3. CREATE COURSE
@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(name=course.name, duration=course.duration)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

# 4. UPDATE COURSE BY ID
@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    existing_course = db.query(Course).filter(Course.id == course_id).first()
    if not existing_course:
        raise HTTPException(status_code=404, detail="Course not found")
    existing_course.name = course.name
    existing_course.duration = course.duration
    db.commit()
    db.refresh(existing_course)
    return existing_course

# 5. DELETE COURSE BY ID
@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"message": f"Course {course_id} deleted"}