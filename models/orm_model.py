from email.policy import default
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database_conn import Base
from sqlalchemy.dialects.mysql import LONGTEXT


class User(Base):
      __tablename__ = 'users'
      id= Column(Integer, primary_key=True, index=True)
      email = Column(String(255), unique=True, index=True)
      name = Column(String(255))
      username = Column(String(255))
      hashed_password = Column(String(255))
      is_admin = Column(Boolean, default=False)
      account_verified = Column(Boolean, default=0, server_default=str(0), nullable=False)
      account_hash = Column(String(255))
      email_otp = Column(Integer)
      unique_id = Column(Integer, unique=True, index=True)
      created_at = Column(String(255))
      accounted_deactiavted = Column(Boolean, default=False)
      user_bio = Column(LONGTEXT,nullable=False,default=None, server_default=None)








