from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import ExamResult, Student, Course
from schemas import ExamResultCreate, ExamResultResponse


router = APIRouter(
    prefix="/exams",
    tags=["Exams"]
)


def calculate_grade(marks: int):
    if marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "Fail"


@router.post("/", response_model=ExamResultResponse)
def create_result(
    result: ExamResultCreate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == result.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    course = db.query(Course).filter(
        Course.id == result.course_id
    ).first()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    grade = calculate_grade(result.marks)

    new_result = ExamResult(
        student_id=result.student_id,
        course_id=result.course_id,
        exam_name=result.exam_name,
        marks=result.marks,
        grade=grade
    )

    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    return new_result


@router.get("/", response_model=list[ExamResultResponse])
def get_results(
    db: Session = Depends(get_db)
):
    return db.query(ExamResult).all()


@router.get("/{result_id}", response_model=ExamResultResponse)
def get_result(
    result_id: int,
    db: Session = Depends(get_db)
):
    result = db.query(ExamResult).filter(
        ExamResult.id == result_id
    ).first()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Result not found"
        )

    return result


@router.put("/{result_id}", response_model=ExamResultResponse)
def update_result(
    result_id: int,
    data: ExamResultCreate,
    db: Session = Depends(get_db)
):
    result = db.query(ExamResult).filter(
        ExamResult.id == result_id
    ).first()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Result not found"
        )

    student = db.query(Student).filter(
        Student.id == data.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    course = db.query(Course).filter(
        Course.id == data.course_id
    ).first()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    result.student_id = data.student_id
    result.course_id = data.course_id
    result.exam_name = data.exam_name
    result.marks = data.marks
    result.grade = calculate_grade(data.marks)

    db.commit()
    db.refresh(result)

    return result


@router.delete("/{result_id}")
def delete_result(
    result_id: int,
    db: Session = Depends(get_db)
):
    result = db.query(ExamResult).filter(
        ExamResult.id == result_id
    ).first()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Result not found"
        )

    db.delete(result)
    db.commit()

    return {
        "message": "Result deleted successfully"
    }