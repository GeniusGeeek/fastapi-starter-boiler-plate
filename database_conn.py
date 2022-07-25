from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
#SQLALCHEMY_DATABASE_URL = "mysql://user:password@host:3306/db"
#SQLALCHEMY_DATABASE_URL = "mysql://user:password@host/db"

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/fastapi_starter_pack"
#SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://liveuser:livepassword@localhost:3306/livedb"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

