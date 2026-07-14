
from Vectordb.pinecone_config import pineconevectorstore
vectorstore=pineconevectorstore()


class BaseVectorstore:
    def adddocuments(self,documents):
        pass

    def similarity_search(self,query:str,course_id:str,video_id:str):
        pass

    def deletecourse(self,documents):
        pass

    def updatecourse(self,documents):
        pass

    def deletevideocourse(self,documents):
        pass



class Repository(BaseVectorstore):

    def adddocuments(self, documents):

        if not documents:
            return ValueError("Chunks not found")
        

        vectorstore.add_documents(documents=documents)

        return {
            "Status":"Success",
            "Message":"Embeddings are successfully stored in the Database"
        }
    
    def similarity_search(self, query, course_id, video_id):

        match=vectorstore.similarity_search(
        query=query,
        filter={"course_id":course_id,"video_id":video_id}
        )
        if not match:
            raise ValueError("Could not find the content either the particular video or course does not exists in the database")
        return match

    def deletevideocourse(self, course_id, video_id):
                vectorstore.delete(
                    filter={"video_id":video_id,"course_id":course_id}
                )

    def deletecourse(self, course_id):
        match=vectorstore.similarity_search(
        query=".",
        k=1,
        filter={"course_id": course_id}
        )

        if not match:
            raise ValueError("Could not find the desired course, it does not exists in the database")
        
        vectorstore.delete(
        filter={"course_id":course_id}
        )
        


            

        
    
    



        

