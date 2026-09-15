from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import SchoolClass, Section
from schemas import (
    SchoolClassCreate,
    SchoolClassResponse,
    SectionCreate,
    SectionResponse
)

router = APIRouter(
    prefix="/classes", 
    tags=["Classes"]
)


# CREATE CLASS
@router.post("/", response_model=SchoolClassResponse)
def create_class(
    school_class: SchoolClassCreate,
    db: Session = Depends(get_db)
):
    new_class = SchoolClass(
        name=school_class.name
    )

    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return new_class


# GET ALL CLASSES
@router.get("/", response_model=list[SchoolClassResponse])
def get_classes(
    db: Session = Depends(get_db)
):
    classes = db.query(SchoolClass).all()

    return classes


# CREATE SECTION
@router.post("/sections", response_model=SectionResponse)
def create_section(
    section: SectionCreate,
    db: Session = Depends(get_db)
):
    school_class = db.query(SchoolClass).filter(
        SchoolClass.id == section.class_id
    ).first()

    if school_class is None:
        raise HTTPException(
            status_code=404,
            detail="Class not found"
        )

    new_section = Section(
        name=section.name,
        class_id=section.class_id
    )

    db.add(new_section)
    db.commit()
    db.refresh(new_section)

    return new_section


# GET ALL SECTIONS
@router.get("/sections", response_model=list[SectionResponse])
def get_sections(
    db: Session = Depends(get_db)
):
    sections = db.query(Section).all()

    return sections


# GET SECTION BY ID
@router.get("/sections/{section_id}", response_model=SectionResponse)
def get_section(
    section_id: int,
    db: Session = Depends(get_db)
):
    section = db.query(Section).filter(
        Section.id == section_id
    ).first()

    if section is None:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )

    return section


# GET CLASS BY ID
@router.get("/{class_id}", response_model=SchoolClassResponse)
def get_class(
    class_id: int,
    db: Session = Depends(get_db)
):
    school_class = db.query(SchoolClass).filter(
        SchoolClass.id == class_id
    ).first()

    if school_class is None:
        raise HTTPException(
            status_code=404,
            detail="Class not found"
        )

    return school_class


# UPDATE CLASS
@router.put("/{class_id}", response_model=SchoolClassResponse)
def update_class(
    class_id: int,
    school_class: SchoolClassCreate,
    db: Session = Depends(get_db)
):
    existing_class = db.query(SchoolClass).filter(
        SchoolClass.id == class_id
    ).first()

    if existing_class is None:
        raise HTTPException(
            status_code=404,
            detail="Class not found"
        )

    existing_class.name = school_class.name

    db.commit()
    db.refresh(existing_class)

    return existing_class


# DELETE CLASS
@router.delete("/{class_id}")
def delete_class(
    class_id: int,
    db: Session = Depends(get_db)
):
    school_class = db.query(SchoolClass).filter(
        SchoolClass.id == class_id
    ).first()

    if school_class is None:
        raise HTTPException(
            status_code=404,
            detail="Class not found"
        )

    db.delete(school_class)
    db.commit()

    return {
        "message": "Class deleted successfully"
    }