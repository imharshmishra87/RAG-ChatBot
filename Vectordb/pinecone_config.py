from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone.vectorstores import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

try:
    model=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',model_kwargs={'device':0})
except Exception as e:
    raise RuntimeError(f"Failed to initialize local model weights: {e}")
    

def pineconevectorstore():
    pc= Pinecone(os.getenv("PINECONE_API_KEY"))

    index_name="course-chat-bot"

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    index=pc.Index(index_name)
    vectorstore=PineconeVectorStore(
        index=index,
        embedding=model
    )
    return vectorstore
    