from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Student,Course
from schemas import StudentCreate, StudentResponse,CourseResponse

# Base prefix "/students" aur Swagger UI tag "Students"
router = APIRouter(prefix="/students", tags=["Students"])

# 1. GET ALL STUDENTS AND PAGINATION
@router.get("/", response_model=list[StudentResponse])
def get_students(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit

    students = db.query(Student).offset(skip).limit(limit).all()

    return students

#--- SEARCH BY STUDENT CODE----

@router.get("/search", response_model=list[StudentResponse])
def search_students(
    name: str,
    db: Session = Depends(get_db)
):
    # 1. Search Query
    students = db.query(Student).filter(
        Student.name.ilike(f"%{name}%")
    ).all()

    # 2. Agar koi record na mila toh 404 Raise karein
    if not students:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No student found with name matching '{name}'"
        )

    return students

# 2. GET STUDENT BY ID
@router.get("/{student_id}", response_model=StudentResponse)
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
    return student

# 3. CREATE STUDENT
@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        name=student.name,
        age=student.age,
        marks=student.marks,
        class_id= student.class_id,
        section_id=student.section_id
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# 4. UPDATE STUDENT BY ID
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student_data: StudentCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
    
    # Fields update karna
    student.name = student_data.name
    student.age = student_data.age
    student.marks = student_data.marks
    
    db.commit()
    db.refresh(student)
    return student

# 5. DELETE STUDENT BY ID
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
    db.delete(student)
    db.commit()
    return {"message": f"Student with ID {student_id} deleted successfully"}


# 1. ASSIGN / ENROLL STUDENT IN A COURSE
@router.post("/student/{student_id}/course/{course_id}")
def enroll_student(student_id: int, course_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()

    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with ID {course_id} not found")

    # Duplicate entry avoid karne ke liye check
    if course in student.courses:
        return {"message": f"Student '{student.name}' is already enrolled in '{course.name}'"}

    student.courses.append(course)
    db.commit()
    return {"message": f"Successfully enrolled '{student.name}' in '{course.name}'"}


# 2. GET ALL ENROLLED COURSES OF A SPECIFIC STUDENT
@router.get("/student/{student_id}/courses", response_model=list[CourseResponse])
def get_student_courses(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")

    return student.courses

# 3. UNENROLL / REMOVE COURSE FROM A STUDENT
@router.delete("/student/{student_id}/course/{course_id}")
def unenroll_student(student_id: int, course_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()

    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or Course not found")

    if course not in student.courses:
        raise HTTPException(status_code=400, detail="Student is not enrolled in this course")

    student.courses.remove(course)
    db.commit()
    return {"message": f"Successfully removed '{course.name}' from '{student.name}'"}
