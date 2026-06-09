from Validation.DataValidation import validate, Chat,DelVideo,Delcourse,Updatedata
from Services.Text_Splitter import Textsplit
from Services.Embedding_Generation import Repository
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from langchain_core.documents import Document
from Services.ChatGeneration import Basechat
import torch
from Services.Embedding_Generation import Repository

from Config.pinecone_config import pineconevectorstore

# Class initialisation 
splitter=Textsplit()
repobj=Repository()
model=Basechat()
vectorstore=pineconevectorstore()



app=FastAPI(title="Course Simplifier")

@app.get('/')
def home():
    return {
        "Message":"Welcome To The Course Simplifier"
    }


@app.get('/health')
def health():
    return {
        "status":"OK",
        "Version": "v1.0.0",
        "app":"AI ChatBot"
    }

@app.post('/upload')
def uploadfile(file : validate):

    document=Document(
        page_content=file.transcript,
        metadata={
            "video_id":file.video_id,
            "course_id":file.course_id,
            "video_title":file.video_title
        }
    )
    
    try:
        newchunks=splitter.split(document)
    except ValueError as v:
        raise HTTPException(
            status_code=404,
            detail=str(v)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
    try:
        data=repobj.adddocuments(newchunks)

    except torch.OutOfMemoryError as oom:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        raise HTTPException(
            detail="Server GPU memory exhausted processing this request. Try smaller inputs.",
            status_code=503
        )
    except RuntimeError as r:
        raise HTTPException(
            detail=str(r),
            status_code=500
        )
    except ValueError as v:
        raise HTTPException(
            detail=str(v),
            status_code=400
        )
    except Exception as e:
        raise HTTPException(
            detail=f"Internal Server error: {str(e)}",
            status_code=500
        )
    
    return JSONResponse(
    status_code=200,
    content=data["Message"]
)

    
@app.post('/chat')
def chat(input:Chat):
    query=input.input
    course_id=input.course_id
    video_id=input.video_id

    try:
        result=model.chat(query,course_id,video_id)
        return{
            "AI":result["AImessage"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@app.delete('/course{course_id}/video{video_id}')
def deletevideo(data:DelVideo):

    try:
        repobj.similarity_search(query=".",course_id=data.course_id,video_id=data.video_id)
    except ValueError as v:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(v)
        )  
    vectorstore.delete(
        filter={"video_id":data.video_id,"course_id":data.course_id}
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Successfully deleted"
    )

@app.delete("/course{course_id}")
def deletecourse(data:Delcourse):
    match=vectorstore.similarity_search(
        query=".",
        k=1,
        filter={"course_id": data.course_id}
        )
    
    if not match:
            raise HTTPException(
            status_code=400,
            detail="Course Not Found"
        )
    
    vectorstore.delete(
        filter={"course_id":data.course_id}
    )

    return JSONResponse(
        status_code=200,
        content="Successfully deleted"
    )

@app.put("/course{course_id}/video{video_id}")
def update(data:Updatedata):

    try:
        match=repobj.similarity_search(query=".",course_id=data.course_id,video_id=data.video_id)
    except ValueError as v:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(v)
        ) 

    vectorstore.delete(
        filter={"video_id":data.video_id,"course_id":data.course_id}
    )

    newdocs=Document(
        page_content=data.transcript,
        metadata={
            "course_id":data.course_id,
            "video_id":data.video_id,
            "video_title":match[0].metadata["video_title"]
        }
    )

    try:
        newchunks=splitter.split(newdocs)
    except ValueError as v:
        raise HTTPException(
            status_code=404,
            detail=str(v)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
    try:
        data=repobj.adddocuments(newchunks)

    except torch.OutOfMemoryError as oom:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        raise HTTPException(
            detail="Server GPU memory exhausted processing this request. Try smaller inputs.",
            status_code=503
        )
    except RuntimeError as r:
        raise HTTPException(
            detail=str(r),
            status_code=500
        )
    except ValueError as v:
        raise HTTPException(
            detail=str(v),
            status_code=400
        )
    except Exception as e:
        raise HTTPException(
            detail=f"Internal Server error: {str(e)}",
            status_code=500
        )

    return {
        "Status":"Success",
        "Message":data["Message"]
    }

    
        


    


    
    


    





    
    






            