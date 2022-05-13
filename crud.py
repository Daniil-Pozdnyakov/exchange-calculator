from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import date
from models import Currency


def create_currency(db: Session, date: date, first_currency: str, second_currency: str, price: int):
    """
    function to create a currency model object
    """
    new_currency = Currency(
        date=date,
        first_currency=first_currency,
        second_currency=second_currency,
        price=price,
    )
    db.add(new_currency)
    db.commit()
    db.refresh(new_currency)
    return new_currency


def get_currency(db: Session, id: int):
    """
    get the first record with a given id, if no such record exists, will return null
    """
    db_currency = db.query(Currency).filter(Currency.id == id).first()
    return db_currency


def list_currency(db: Session):
    """
    Return a list of all existing currency records
    """
    all_currency = db.query(Currency).all()
    return all_currency


def update_currency(db: Session, id: int, date: date, first_currency: str, second_currency: str, price: int):
    """
    Update a currency object's attributes
    """
    db_currency = get_currency(db=db, id=id)
    db_currency.date = date
    db_currency.first_currency = first_currency
    db_currency.second_currency = second_currency
    db_currency.price = price

    db.commit()
    db.refresh(db_currency)
    return db_currency


def delete_currency(db: Session, id: int):
    """
    Delete a currency object
    """
    db_currency = get_currency(db=db, id=id)
    db.delete(db_currency)
    db.commit()


def get_currency_by_currency_names(db: Session, first_currency: str, second_currency: str):
    """
    get the all records with a given names currency, if no such record exists, will return null
    """
    db_currency = db.query(Currency).filter(Currency.first_currency.like(first_currency),
                                            Currency.second_currency.like(second_currency)).all()
    if not db_currency:
        db_currency = db.query(Currency).filter(Currency.first_currency.like(second_currency),
                                                Currency.second_currency.like(first_currency)).all()
    return db_currency


def get_currency_price_by_date_and_names(db: Session, first_currency: str, second_currency: str, date: date):
    """
    get rate with a names currency on current date
    """
    db_currency = db.query(Currency).filter(Currency.date.like(date),
                                            Currency.first_currency.like(first_currency),
                                            Currency.second_currency.like(second_currency)).first()
    if not db_currency:
        db_currency = db.query(Currency).filter(Currency.date.like(date),
                                                Currency.first_currency.like(second_currency),
                                                Currency.second_currency.like(first_currency)).first()
    if not db_currency:
        db_currency = db.query(Currency).filter(Currency.date.like(date)).filter(or_(
                                                Currency.first_currency.like(first_currency),
                                                Currency.second_currency.like(first_currency))).all()
        first_list = []
        for item in db_currency:
            if item.first_currency != first_currency:
                first_list.append(item.first_currency)
                first_list.append(1/item.price)
            else:
                first_list.append(item.second_currency)
                first_list.append(1*item.price)

        db_currency = db.query(Currency).filter(Currency.date.like(date)).filter(or_(
            Currency.first_currency.like(second_currency),
            Currency.second_currency.like(second_currency))).all()

        second_list = []
        for item in db_currency:
            if item.first_currency != second_currency:
                second_list.append(item.first_currency)
                second_list.append(1/item.price)
            else:
                second_list.append(item.second_currency)
                second_list.append(1*item.price)

        for i in range(0, len(first_list), 2):
            for j in range(0, len(second_list), 2):
                if first_list[i] == second_list[j]:
                    return first_list[i + 1] * second_list[j + 1]
    return db_currency.price
