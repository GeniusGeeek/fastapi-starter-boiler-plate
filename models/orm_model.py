from email.policy import default
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database_conn import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from sqlalchemy import Text  # for other databases to use a longtext type


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    username = Column(String(255))
    hashed_password = Column(String(255))
    is_admin = Column(Boolean, default=False)
    account_verified = Column(
        Boolean, default=0, server_default=str(0), nullable=False)
    account_hash = Column(String(255))
    email_otp = Column(Integer)
    unique_id = Column(Integer, unique=True, index=True)
    created_at = Column(String(255))
    account_deactiavted = Column(Boolean, default=False)
    user_bio = Column(LONGTEXT)
    user_subscriptions_table = relationship(
        "UserSubscriptions", back_populates="users_table")


class UserSubscriptions(Base):
    __tablename__ = 'user_subscriptions'
    id = Column(Integer, primary_key=True, index=True)
    user_unique_id = Column(String(255), unique=True, index=True)
    start_date = Column(String(255))
    end_date = Column(String(255))
    amount_paid = Column(String(255))
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    is_currently_active = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    users_table = relationship(
        "User", back_populates="user_subscriptions_table")
    subscriptions_table = relationship(
        "Subscriptions", back_populates="user_subscriptions_table")


class Subscriptions(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(String(255), unique=True, index=True)
    duration = Column(String(255))
    amount = Column(String(255))
    description = Column(String(255))
    user_subscriptions_table = relationship(
        "UserSubscriptions", back_populates="subscriptions_table")
