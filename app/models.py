from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, Table, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

association_table = Table(
    "association",
    Base.metadata,
    Column("discussion_id", UUID(as_uuid=True), ForeignKey("crm.discussions.id")),
    Column("hashtag_id", UUID(as_uuid=True), ForeignKey("crm.hashtags.id")),
    __table_args__={"schema": "crm"},
)


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "crm"}
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_on = Column(DateTime, default=datetime.utcnow())
    name = Column(String, index=True, nullable=False)
    mobile_no = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    discussions = relationship("Discussion", back_populates="user")


class Discussion(Base):
    __tablename__ = "discussions"
    __table_args__ = {"schema": "crm"}
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_on = Column(DateTime, default=datetime.utcnow())
    text = Column(Text, index=True, nullable=False)
    image = Column(String, nullable=True)
    user_id = Column(UUID, ForeignKey("crm.users.id"), nullable=False)
    user = relationship("User", back_populates="discussions")
    hashtags = relationship(
        "Hashtag", secondary=association_table, back_populates="discussions"
    )


class Hashtag(Base):
    __tablename__ = "hashtags"
    __table_args__ = {"schema": "crm"}
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_on = Column(DateTime, default=datetime.utcnow())
    name = Column(String, unique=True, index=True)
    discussions = relationship(
        "Discussion", secondary=association_table, back_populates="hashtags"
    )


class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = {"schema": "crm"}
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_on = Column(DateTime, default=datetime.utcnow())
    text = Column(Text)
    user_id = Column(UUID, ForeignKey("crm.users.id"))
    discussion_id = Column(UUID, ForeignKey("crm.discussions.id"))


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = {"schema": "crm"}
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_on = Column(DateTime, default=datetime.utcnow())
    user_id = Column(UUID, ForeignKey("crm.users.id"))
    discussion_id = Column(UUID, ForeignKey("crm.discussions.id"))


class Follow(Base):
    __tablename__ = "follow"
    __table_args__ = {"schema": "crm"}
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_on = Column(DateTime, default=datetime.utcnow())
    user_id = Column(UUID, ForeignKey("crm.users.id"))
    follow_user_id = Column(UUID, ForeignKey("crm.users.id"))
