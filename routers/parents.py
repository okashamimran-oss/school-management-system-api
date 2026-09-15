from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Parent, Student
from schemas import ParentCreate, ParentResponse


router = APIRouter(
    prefix="/parents",
    tags=["Parents"]
)


# CREATE PARENT
@router.post("/", response_model=ParentResponse)
def create_parent(
    parent: ParentCreate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == parent.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    new_parent = Parent(
        name=parent.name,
        phone=parent.phone,
        email=parent.email,
    )

    new_parent.students.append(student)

    db.add(new_parent)
    db.commit()
    db.refresh(new_parent)

    return new_parent


# GET ALL PARENTS
@router.get("/", response_model=list[ParentResponse])
def get_parents(
    db: Session = Depends(get_db)
):
    parents = db.query(Parent).all()

    return parents


# GET PARENT BY ID
@router.get("/{parent_id}", response_model=ParentResponse)
def get_parent(
    parent_id: int,
    db: Session = Depends(get_db)
):
    parent = db.query(Parent).filter(
        Parent.id == parent_id
    ).first()

    if parent is None:
        raise HTTPException(
            status_code=404,
            detail="Parent not found"
        )

    return parent

# UPDATE PARENT
@router.put("/{parent_id}", response_model=ParentResponse)
def update_parent(
    parent_id: int,
    parent: ParentCreate,
    db: Session = Depends(get_db)
):
    existing_parent = db.query(Parent).filter(
        Parent.id == parent_id
    ).first()

    if existing_parent is None:
        raise HTTPException(
            status_code=404,
            detail="Parent not found"
        )

    student = db.query(Student).filter(
        Student.id == parent.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    existing_parent.name = parent.name
    existing_parent.phone = parent.phone
    existing_parent.email = parent.email
    existing_parent.student_id = parent.student_id

    db.commit()
    db.refresh(existing_parent)

    return existing_parent


# DELETE PARENT
@router.delete("/{parent_id}")
def delete_parent(
    parent_id: int,
    db: Session = Depends(get_db)
):
    parent = db.query(Parent).filter(
        Parent.id == parent_id
    ).first()

    if parent is None:
        raise HTTPException(
            status_code=404,
            detail="Parent not found"
        )

    db.delete(parent)
    db.commit()

    return {
        "message": "Parent deleted successfully"
    }