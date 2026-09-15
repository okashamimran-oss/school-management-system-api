from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Fee, Student
from schemas import FeeCreate, FeeResponse


router = APIRouter(
    prefix="/fees",
    tags=["Fees"]
)


def calculate_status(amount: int, paid_amount: int):
    if paid_amount == 0:
        return "Unpaid"
    elif paid_amount < amount:
        return "Partial"
    else:
        return "Paid"


@router.post("/", response_model=FeeResponse)
def create_fee(
    fee: FeeCreate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == fee.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    status = calculate_status(
        fee.amount,
        fee.paid_amount
    )

    new_fee = Fee(
        amount=fee.amount,
        paid_amount=fee.paid_amount,
        status=status,
        student_id=fee.student_id
    )

    db.add(new_fee)
    db.commit()
    db.refresh(new_fee)

    return new_fee


@router.get("/", response_model=list[FeeResponse])
def get_fees(
    db: Session = Depends(get_db)
):
    return db.query(Fee).all()


@router.get("/{fee_id}", response_model=FeeResponse)
def get_fee(
    fee_id: int,
    db: Session = Depends(get_db)
):
    fee = db.query(Fee).filter(
        Fee.id == fee_id
    ).first()

    if fee is None:
        raise HTTPException(
            status_code=404,
            detail="Fee record not found"
        )

    return fee


@router.put("/{fee_id}", response_model=FeeResponse)
def update_fee(
    fee_id: int,
    fee_data: FeeCreate,
    db: Session = Depends(get_db)
):
    fee = db.query(Fee).filter(
        Fee.id == fee_id
    ).first()

    if fee is None:
        raise HTTPException(
            status_code=404,
            detail="Fee record not found"
        )

    fee.amount = fee_data.amount
    fee.paid_amount = fee_data.paid_amount
    fee.student_id = fee_data.student_id

    fee.status = calculate_status(
        fee.amount,
        fee.paid_amount
    )

    db.commit()
    db.refresh(fee)

    return fee


@router.delete("/{fee_id}")
def delete_fee(
    fee_id: int,
    db: Session = Depends(get_db)
):
    fee = db.query(Fee).filter(
        Fee.id == fee_id
    ).first()

    if fee is None:
        raise HTTPException(
            status_code=404,
            detail="Fee record not found"
        )

    db.delete(fee)
    db.commit()

    return {
        "message": "Fee record deleted successfully"
    }