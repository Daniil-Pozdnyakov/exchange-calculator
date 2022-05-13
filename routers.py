from fastapi import Depends, UploadFile, File, APIRouter
import os
import shutil
from datetime import date
import crud
import storage
from db import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
def home():
    return {"Welcome to Exchange Calculator! (c) PhyPartners"}


@router.post("/create_currency", tags=["CRUD database"])
def create_currency(first_currency: str, second_currency: str, price: int, date: date,
                    db: Session = Depends(get_db)):
    """
    Create currency
    """
    currency = crud.create_currency(
        db=db,
        date=date,
        first_currency=first_currency,
        second_currency=second_currency,
        price=price,
    )

    return {"currency": currency}


@router.get("/get_currency/{id}/", tags=["CRUD database"])
def get_currency(id: int, db: Session = Depends(get_db)):
    """
    The path parameter for id should have the same name as the argument for id
    so that FastAPI will know that they refer to the same variable
    Returns a currency object if one with the given id exists, else null
    """
    currency = crud.get_currency(db=db, id=id)
    return currency


@router.get("/list_currency", tags=["CRUD database"])
def list_currency(db: Session = Depends(get_db)):
    """
    Fetch a list of all currency object
    Returns a list of objects
    """
    currency_list = crud.list_currency(db=db)
    return currency_list


@router.put("/update_currency/{id}/", tags=["CRUD database"])  # id is a path parameter
def update_currency(id: int, date: date, first_currency: str, second_currency: str, price: int,
                    db: Session = Depends(get_db)):
    """
    Update currency by id
    """
    db_currency = crud.get_currency(db=db, id=id)
    if db_currency:
        updated_currency = crud.update_currency(
            db=db,
            id=id,
            date=date,
            first_currency=first_currency,
            second_currency=second_currency,
            price=price)
        return updated_currency
    else:
        return {"error": f"currency with id {id} does not exist"}


@router.delete("/delete_currency/{id}/", tags=["CRUD database"])  # id is a path parameter
def delete_currency(id: int, db: Session = Depends(get_db)):
    """
    Delete your currency by id
    """
    db_currency = crud.get_currency(db=db, id=id)
    if db_currency:
        return crud.delete_currency(db=db, id=id)
    else:
        return {"error": f"currency with id {id} does not exist"}


@router.get("/get_currency_by_currency_names/{first_currency}/{second_currency}", tags=["CRUD database"])
def get_currency_by_currency_names(first_currency: str, second_currency: str, db: Session = Depends(get_db)):
    """
    The path parameter for currency names should have the same name as the argument for currency names
    so that FastAPI will know that they refer to the same variable
    Returns a currency object if one with the given currency names exists, else null
    """
    currency = crud.get_currency_by_currency_names(
        db=db,
        first_currency=first_currency,
        second_currency=second_currency)

    return currency


@router.get("/get_currency_price_by_date_and_names/{first_currency}/{second_currency}/{date}", tags=["CRUD database"])
def get_currency_price_by_date_and_names(first_currency: str, second_currency: str, date: date,
                                         db: Session = Depends(get_db)):
    """
    get rate with a names currency on current date
    """
    currency = crud.get_currency_price_by_date_and_names(
        db=db,
        first_currency=first_currency,
        second_currency=second_currency,
        date=date
    )
    return currency


@router.post("/upload", tags=["Files"])
def upload(input_file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload your files for db"""
    try:
        os.mkdir("./cache/")
    except FileExistsError:
        pass
    with open(f"./cache/{input_file.filename}", "wb") as buffer:
        shutil.copyfileobj(input_file.file, buffer)
    data = storage.convert_from_csv(input_file.filename)
    shutil.rmtree("./cache/")

    print(data)
    for row in data[1:]:
        for i in range(1, len(row)):
            cur = data[0][i].split("/")
            date_list = [int(item) for item in row[0].split("-")]
            crud.create_currency(
                db=db,
                date=date(date_list[0], date_list[1], date_list[2]),
                first_currency=cur[0],
                second_currency=cur[1],
                price=row[i],
            )
    return {"result": True}
