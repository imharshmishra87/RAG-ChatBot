from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model=ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite', model_kwargs={"device":0})

class Textsplit:
    def __init__(self):
        pass

    def split(self, docs):
        splitter=RecursiveCharacterTextSplitter(
            chunk_size=45,
            chunk_overlap=10
        )
        chunks=splitter.split_documents([docs])
        if not chunks:
            raise ValueError("Recursive Character Text Splitter Failed to generate chunks")
        return chunks
        



