from Core.security import required_role
from Validation.DataValidation import Delcourse
from pinecone.exceptions import PineconeException
from Services.Embedding_Generation import Repository
from fastapi import FastAPI, status, APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from Services.Embedding_Generation import Repository


# Class initialisation 
repobj=Repository()



router=APIRouter(prefix="/admin",tags=["admin"])

@router.delete("/course{course_id}")
def deletecourse(data:Delcourse,current_user:dict=Depends(required_role("admin"))):

    # Mainly responsible for deleting the entire course, it first checks whether the course exist in the database if not it raises an error and if it exists it deletes the entire course based on the filter method by passing course_id as a filter.

    try:
        repobj.deletecourse(data.course_id)
        #  If you want to delete the entire course than this method passes the course id and deletes based on filter method.

    except ValueError as v:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= str(v)
        )
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
