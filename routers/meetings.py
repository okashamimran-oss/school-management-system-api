from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import ParentMeeting, Parent, Student
from schemas import ParentMeetingCreate, ParentMeetingResponse


router = APIRouter(
    prefix="/meetings",
    tags=["Parent Meetings"]
)


# CREATE
@router.post("/", response_model=ParentMeetingResponse)
def create_meeting(
    meeting: ParentMeetingCreate,
    db: Session = Depends(get_db)
):
    parent = db.query(Parent).filter(
        Parent.id == meeting.parent_id
    ).first()

    if parent is None:
        raise HTTPException(
            status_code=404,
            detail="Parent not found"
        )

    student = db.query(Student).filter(
        Student.id == meeting.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    new_meeting = ParentMeeting(
        parent_id=meeting.parent_id,
        student_id=meeting.student_id,
        meeting_date=meeting.meeting_date,
        purpose=meeting.purpose
    )

    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)

    return new_meeting


# GET ALL
@router.get("/", response_model=list[ParentMeetingResponse])
def get_meetings(
    db: Session = Depends(get_db)
):
    meetings = db.query(ParentMeeting).all()

    return meetings


# GET BY ID
@router.get("/{meeting_id}", response_model=ParentMeetingResponse)
def get_meeting_by_id(
    meeting_id: int,
    db: Session = Depends(get_db)
):
    meeting = db.query(ParentMeeting).filter(
        ParentMeeting.id == meeting_id
    ).first()

    if meeting is None:
        raise HTTPException(
            status_code=404,
            detail="Meeting not found"
        )

    return meeting


# UPDATE
@router.put("/{meeting_id}", response_model=ParentMeetingResponse)
def update_meeting(
    meeting_id: int,
    data: ParentMeetingCreate,
    db: Session = Depends(get_db)
):
    meeting = db.query(ParentMeeting).filter(
        ParentMeeting.id == meeting_id
    ).first()

    if meeting is None:
        raise HTTPException(
            status_code=404,
            detail="Meeting not found"
        )

    parent = db.query(Parent).filter(
        Parent.id == data.parent_id
    ).first()

    if parent is None:
        raise HTTPException(
            status_code=404,
            detail="Parent not found"
        )

    student = db.query(Student).filter(
        Student.id == data.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    meeting.parent_id = data.parent_id
    meeting.student_id = data.student_id
    meeting.meeting_date = data.meeting_date
    meeting.purpose = data.purpose

    db.commit()
    db.refresh(meeting)

    return meeting


# DELETE
@router.delete("/{meeting_id}")
def delete_meeting(
    meeting_id: int,
    db: Session = Depends(get_db)
):
    meeting = db.query(ParentMeeting).filter(
        ParentMeeting.id == meeting_id
    ).first()

    if meeting is None:
        raise HTTPException(
            status_code=404,
            detail="Meeting not found"
        )

    db.delete(meeting)
    db.commit()

    return {
        "message": "Meeting deleted successfully"
    }