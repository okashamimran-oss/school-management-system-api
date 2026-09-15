from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Attendance, Student
from schemas import AttendanceCreate, AttendanceResponse


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


# CREATE ATTENDANCE
@router.post("/", response_model=AttendanceResponse)
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == attendance.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    new_attendance = Attendance(
        student_id=attendance.student_id,
        date=attendance.date,
        status=attendance.status
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance


# GET ALL
@router.get("/", response_model=list[AttendanceResponse])
def get_attendance(
    db: Session = Depends(get_db)
):
    return db.query(Attendance).all()


# GET BY ID
@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance_by_id(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()

    if attendance is None:
        raise HTTPException(
            status_code=404,
            detail="Attendance not found"
        )

    return attendance


# UPDATE
@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: int,
    data: AttendanceCreate,
    db: Session = Depends(get_db)
):
    attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()

    if attendance is None:
        raise HTTPException(
            status_code=404,
            detail="Attendance not found"
        )

    student = db.query(Student).filter(
        Student.id == data.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    attendance.student_id = data.student_id
    attendance.date = data.date
    attendance.status = data.status

    db.commit()
    db.refresh(attendance)

    return attendance


# DELETE
@router.delete("/{attendance_id}")
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()

    if attendance is None:
        raise HTTPException(
            status_code=404,
            detail="Attendance not found"
        )

    db.delete(attendance)
    db.commit()

    return {
        "message": "Attendance deleted successfully"
    }