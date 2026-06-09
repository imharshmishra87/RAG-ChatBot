from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableSequence
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.output_parsers import StrOutputParser

from Config.pinecone_config import pineconevectorstore
from fastapi.exceptions import HTTPException

vectorstore=pineconevectorstore()

parser=StrOutputParser()

model=ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite', model_kwargs={"device":0})

retriever=vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k":2,"lambda_mult":0.5}
)


prompt=ChatPromptTemplate.from_messages([
    ("system","You are a helpfull AI assistant whose goal is to answer the human query based on the provided context {context} if not enough context provided respond that not enough context available for this query"),

    MessagesPlaceholder(variable_name="chat_history"),

    ("human","{query}")
])

messages=[]

class VideoNotFoundError(Exception):
    pass



class Basechat:
    def __init__(self):
        pass

    def chat(self, query:str,course_id:str, video_id):
        messages.append(HumanMessage(content=query))

        context=retriever.invoke(query,filter={
            "course_id":course_id,
            "video_id":video_id
        })

        if not context:
            raise VideoNotFoundError(f"Could not found video for the particular id : {video_id}")
        

        chain=prompt | model | parser
        try:
            result=chain.invoke({
                "context":context,
                "chat_history":messages,
                "query":query
            })
            messages.append(AIMessage(result))
            return {
                "status":"Success",
                "AImessage":result,
                "Context":context
            }
        except Exception as e:
            raise RuntimeError(f"Unable to generate response: {e}")




    






