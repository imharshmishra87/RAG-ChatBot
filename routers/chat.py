from Validation.DataValidation import Chat
from fastapi import FastAPI, status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from Services.ChatGeneration import Basechat
from Core.security import get_current_user

# Class initialisation 
model=Basechat()

router=APIRouter(prefix="/chat",tags=["chat_bot"])

@router.post("/")
def chat(input:Chat, current_user:str=Depends(get_current_user)):

    # Mainly responsible for chat generation, perform semantic search and output the data based on the query by filtering course_id and video_id, it also handles the error if the course or video does not exist in the database.

    query=input.input
    course_id=input.course_id
    video_id=input.video_id

    try:
        result=model.chat(query,course_id,video_id)

        # model.chat is mainly responsible for generating o/p based on the query by filtering course_id and video_id

        return{
            "AI":result["AImessage"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )