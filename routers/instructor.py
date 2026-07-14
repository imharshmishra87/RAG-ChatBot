from Validation.DataValidation import validate,Chat,DelVideo,Delcourse,Updatedata
from pinecone.exceptions import PineconeException
from Core.security import required_role
from Services.Text_Splitter import Textsplit
from Services.Embedding_Generation import Repository
from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from langchain_core.documents import Document
from Services.ChatGeneration import Basechat
import torch
from Services.Embedding_Generation import Repository


# Class initialisation 
splitter=Textsplit()
repobj=Repository()
model=Basechat()



router=APIRouter(prefix="/Instructor",tags=["instructor"])


@router.post('/upload')
def uploadfile(file : validate, current_user:dict=Depends(required_role("Instructor"))):

    # This method is mainly responsible for uploading the transcripts -> Chunking it -> Further storing it as an embedding in the database.

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
        # Split documents into chunks using recurrsive character text splitter 
    except ValueError as v:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(v)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
    try:
        data=repobj.adddocuments(newchunks)
        # Adding those chunks into databse by first converting them into embeddings

    except torch.OutOfMemoryError as oom:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        raise HTTPException(
            detail=f"Server GPU memory exhausted processing this request. Try smaller inputs.{str(oom)}",
            status_code=503
        )
    except RuntimeError as r:
        raise HTTPException(
            detail=str(r),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except ValueError as v:
        raise HTTPException(
            detail=str(v),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        raise HTTPException(
            detail=f"Internal Server error: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return JSONResponse(
    status_code=200,
    content=data["Message"]
)


@router.delete('/course{course_id}/video{video_id}')
def deletevideo(data:DelVideo, current_user:dict=Depends(required_role("Instructor"))):

    # Mainly responsible for deleting the course video transcript, it first checks whether the course or video exist in the database if not it raises an error and if it exists it deletes the video transcript based on the filter method by passing course_id and video_id as a filter.

    try:
        repobj.similarity_search(query=".",course_id=data.course_id,video_id=data.video_id)
        # responsible for checking whether if the course or video exist in the database.
    except ValueError as v:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(v)
        )  
    
    try:
        repobj.deletevideocourse(data.course_id,data.video_id)
        # Deletes the course video using the filter method

    except PineconeException as pe:
        raise HTTPException(
            detail=f"Failed to delete the video: {str(pe)}",
            status_code= status.HTTP_502_BAD_GATEWAY
        )
    except Exception as e:
        raise HTTPException(
            detail=f"Internal Sever error occurred : {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Successfully deleted"
    )


@router.put("/course{course_id}/video{video_id}")
def update(data:Updatedata,current_user:dict=Depends(required_role("Instructor"))):

    # Mainly responsible for updating the video transcript usually involve by first deleting the video transcript and then updating it with a fresh transcript uploaded from the frontend. It first checks whether the course or video exist in the database if not it raises an error and if it exists it deletes the video transcript based on the filter method by passing course_id and video_id as a filter and then it updates with the new transcript.

    try:
        match=repobj.similarity_search(query=".",course_id=data.course_id,video_id=data.video_id)

        # responsible for checking whether if the course or video exist in the database, if not it raises an error and if it exists it returns the match which is used for metadata while updating the course video transcript.

    except ValueError as v:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(v)
        ) 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
    try:
        repobj.deletevideocourse(data.course_id,data.video_id)

        # responsible for deleting the existing course video transcript using the filter method by passing course_id and video_id as a filter.


    except PineconeException as pe:
        raise HTTPException(
            detail=f"Failed to delete the video: {str(pe)}",
            status_code= status.HTTP_502_BAD_GATEWAY
        )
    except Exception as e:
        raise HTTPException(
            detail=f"Internal Sever error occurred : {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
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
        # Split documents into chunks using recurrsive character text splitter
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
        # Adding those chunks into databse by first converting them into embeddings

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
