from sqlalchemy.orm import Session
from models import orm_model, schema_model


def login_email(email: str,db: Session):
  return db.query(orm_model.User).filter(orm_model.User.email == email).first()

