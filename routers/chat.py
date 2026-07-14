from Validation.DataValidation import Chat
from fastapi import FastAPI, status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from Services.ChatGeneration import Basechat
from Core.security import get_current_user
from Model.model import add_data
from sqlalchemy.orm import Session
from Core.database import get_db

# Class initialisation 
model=Basechat()

router=APIRouter(prefix="/chat",tags=["chat_bot"])

@router.post("/")
def chat(input:Chat, current_user:str=Depends(get_current_user), db:Session=Depends(get_db)):

    # Mainly responsible for chat generation, perform semantic search and output the data based on the query by filtering course_id and video_id, it also handles the error if the course or video does not exist in the database.

    user_data_2_db=add_data(
        db=db,
        user_id=current_user.id,
        role=current_user.role,
        course_id=input.course_id,
        video_id=input.video_id,
        session_id=input.session_id,
        content=input.input
    )
    query=input.input
    course_id=input.course_id
    video_id=input.video_id
    session_id=input.session_id

    try:
        result=model.chat(db,query,course_id,video_id,session_id,current_user.id)

        ai_message_2_db=add_data(
                db=db,
                user_id=current_user.id,
                course_id=course_id,
                video_id=video_id,
                session_id=session_id,
                role="Assistant",
                content=result["AImessage"]
            )

        # model.chat is mainly responsible for generating o/p based on the query by filtering course_id and video_id

        return{
            "AI":result["AImessage"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )