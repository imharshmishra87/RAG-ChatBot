from Core.database import base
from sqlalchemy import Integer, String, Column,ForeignKey,Text,DateTime
from datetime import datetime
from sqlalchemy.orm import Session,relationship
from fastapi import Depends
from Core.database import get_db

class User(base):

    __tablename__="user"

    id=Column(Integer, primary_key=True, index=True)
    email=Column(String, unique=True, index=True )
    hash=Column(String)
    role=Column(String, default="instructor")
    messages=relationship("ChatMessages",back_populates="user")

class ChatMessages(base):
    __tablename__="chatmessages"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("user.id"),nullable=False)
    course_id=Column(String,index=True,nullable=False)
    video_id=Column(String,index=True,nullable=False)
    session_id=Column(String,index=True,nullable=False)
    role=Column(String,nullable=False)
    content=Column(Text, nullable=False)
    created_at=Column(DateTime,default=datetime.now())
    user=relationship("User",back_populates="messages")


def add_data(
        db:Session,
        user_id:int,
        course_id:str,
        video_id:str,
        session_id:str,
        role:str,
        content:str
    ):
    new_messages=ChatMessages(
        user_id=user_id,
        course_id=course_id,
        session_id=session_id,
        video_id=video_id,
        role=role,
        content=content
    )
    db.add(new_messages)
    db.commit()
    db.refresh(new_messages)
    return new_messages

def get_history(db:Session,user_id:int, session_id:str):
    history=db.query(ChatMessages).filter(
        ChatMessages.user_id==user_id,
        ChatMessages.session_id==session_id
    ).order_by(ChatMessages.created_at.desc()).limit(20).all()

    # This function explictly returns the chat history for a specific user and session, ordered by the time the messages were created. It can be used to retrieve the conversation context for generating AI responses or displaying past interactions in a chat interface.
    return history

