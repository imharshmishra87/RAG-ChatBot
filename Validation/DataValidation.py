import re
from pydantic import BaseModel,Field
from typing import Annotated



class validate(BaseModel):
    video_id:Annotated[str,Field(description="Enter The video id", min_length=1,example="yt rag course 101")]
    course_id:Annotated[str,Field(description="Enter The Course id", min_length=1,example="genai bootcamp 2026")]
    video_title:Annotated[str,Field(description="Enter The Title of the video", min_length=1,example="Building a YouTube RAG Chatbot with FastAPI")]
    transcript:Annotated[str,Field(description="Paste the transcript of the video", min_length=100,example="Paste The Transcript of length greater than 100 char")]


class Chat(BaseModel):
    input:Annotated[str, Field(description="Hello How can i help you")]
    course_id:Annotated[str,Field(description="Enter The Course id", min_length=1,example="genai bootcamp 2026")]
    video_id:Annotated[str,Field(description="Enter The video id", min_length=1,example="yt rag course 101")]
    

class DelVideo(BaseModel):
    video_id:Annotated[str,Field(description="Enter The video id", min_length=1,example="yt rag course 101")]
    course_id:Annotated[str,Field(description="Enter The Course id", min_length=1,example="genai bootcamp 2026")]

class Delcourse(BaseModel):
    course_id:Annotated[str,Field(description="Enter The Course id", min_length=1,example="genai bootcamp 2026")]


class Updatedata(BaseModel):
    course_id:Annotated[str,Field(description="Enter The Course id", min_length=1,example="genai bootcamp 2026")]
    video_id:Annotated[str,Field(description="Enter The video id", min_length=1,example="yt rag course 101")]
    transcript:Annotated[str,Field(description="Paste the updated version of the transcript", min_length=100, example="Paste The Updated Version of the transcript")]

    

class textpreprocessing:

    def __init__(self):
        pass

    def clean_data(text:str)->str:
        allowed_char=r"[^a-zA-Z0-9\s.,?!']"
        preprocessed_data=re.sub(allowed_char,"",text)

        data=re.sub(r"\n+","",preprocessed_data)
        return data
    