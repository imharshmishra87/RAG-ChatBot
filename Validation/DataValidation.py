import re
from pydantic import BaseModel,Field,EmailStr,SecretStr,field_validator,model_validator,ConfigDict
from typing import Annotated,Literal



class validate(BaseModel):
    video_id:Annotated[str,Field(description="Enter The video id", min_length=1,example="yt rag course 101")]
    course_id:Annotated[str,Field(description="Enter The Course id", min_length=1,example="genai bootcamp 2026")]
    video_title:Annotated[str,Field(description="Enter The Title of the video", min_length=1,example="Building a YouTube RAG Chatbot with FastAPI")]
    transcript:Annotated[str,Field(description="Paste the transcript of the video", min_length=100,example="Paste The Transcript of length greater than 100 char")]


class Chat(BaseModel):
    input:Annotated[str, Field(description="Hello How can i help you")]
    course_id:Annotated[str,Field(description="Enter The Course id", min_length=1,example="genai bootcamp 2026")]
    video_id:Annotated[str,Field(description="Enter The video id", min_length=1,example="yt rag course 101")]
    session_id:str

class ChatmessageResponse(BaseModel):
    id:int
    session_id:str
    role:str
    content:str
    model_config=ConfigDict(from_attributes=True)
    

class DelVideo(BaseModel):
    video_id:Annotated[str,Field(description="Enter The video id", min_length=1,example="yt rag course 101")]
    course_id:Annotated[str,Field(description="Enter The Course id", min_length=1,example="genai bootcamp 2026")]

class Delcourse(BaseModel):
    course_id:Annotated[str,Field(description="Enter The Course id", min_length=1,example="genai bootcamp 2026")]


class Updatedata(BaseModel):
    course_id:Annotated[str,Field(description="Enter The Course id", min_length=1,example="genai bootcamp 2026")]
    video_id:Annotated[str,Field(description="Enter The video id", min_length=1,example="yt rag course 101")]
    transcript:Annotated[str,Field(description="Paste the updated version of the transcript", min_length=100, example="Paste The Updated Version of the transcript")]

class Register(BaseModel):
    name:Annotated[str,Field(description="Enter your name", examples=["John"])]
    email:Annotated[EmailStr,Field(description="Enter your name", examples=["xyz@email.com"])]
    password:Annotated[SecretStr,Field(description="Enter The password", max_length=16)]
    confirm_password:Annotated[SecretStr,Field(description="Confirm The password", max_length=16)]
    role:Annotated[Literal["Instructor","Student"],Field("Choose your role")]="Instructor"

    class Config:
        from_attributes=True

    @field_validator("password")
    def validate_password_strength(cls, v: SecretStr) -> SecretStr:
        raw_password = v.get_secret_value()
        # Enforce at least one uppercase, one lowercase, and one digit
        if not re.search(r"[A-Z]", raw_password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", raw_password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"", raw_password):
            raise ValueError("Password must contain at least one number")
        return v

    @model_validator(mode="after")
    def password_match(cls,model):
        if model.password.get_secret_value()!=model.confirm_password.get_secret_value():
            raise ValueError("Emails are not same")
        return model

class RegisterResponse(BaseModel):
    role:str
    email:EmailStr
    model_config=ConfigDict(from_attributes=True)



class textpreprocessing:

    def __init__(self):
        pass

    def clean_data(text:str)->str:
        allowed_char=r"[^a-zA-Z0-9\s.,?!']"
        preprocessed_data=re.sub(allowed_char,"",text)

        data=re.sub(r"\n+","",preprocessed_data)
        return data
    