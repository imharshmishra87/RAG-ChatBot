from fastapi import  FastAPI
from Core.database import engine, base
from scheduler import scheduler
from routers import admin, chat, instructor,auth
from contextlib import asynccontextmanager

base.metadata.create_all(bind=engine)

@asynccontextmanager
async def scheduler_func(app:FastAPI):
    print("Scheduler Started")
    scheduler.start()

    yield
    print("Scheduler Stoped")
    scheduler.shutdown()


app=FastAPI(title="Course Simplifier",lifespan=scheduler_func)

app.include_router(chat.router)
app.include_router(instructor.router)
app.include_router(admin .router)
app.include_router(auth.router)

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





    




    


    
        


    


    
    


    





    
    






            