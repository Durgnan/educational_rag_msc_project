import os
import time
from typing import List, Dict
from pathlib import Path
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
# from langchain.retrievers import BM25Retriever, EnsembleRetriever
 
 
class AdvancedRAG:
    def __init__(self,model:str = "gpt-3.5"):
        load_dotenv()
        self.model = model
        if(self.model not in ["gpt-3.5-turbo","gemma2","mistral","llama3.1","llama3","gpt-4","gpt-4o","llama2"]):
            raise ValueError('the model you have provided is not available or exists. please provide one of the below available models.["gpt-3.5","gemma2","mistral","llama3.1","llama3","gpt-4","gpt-4o"]')
        self.embeddings = self.create_embeddings()
        self.prompt = self._create_prompt()
        self.db = "faiss_db_900"
        self.retriever = self._retriever()
        self.model_obj = self._define_model()
        self.qa_chain = self._create_qa_chain()
       
 
    def _retriever(self):
        if(Path(self.db).exists()):
            local_db = FAISS.load_local(self.db,self.embeddings,allow_dangerous_deserialization=True)
            retriever = local_db.as_retriever()
           
            compressor = FlashrankRerank()
            compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor, base_retriever=retriever
            )
            return compression_retriever
        else:
            raise ValueError(
                r"There is no directory called {self.db}. which means you have not trained any files. please train the pdf file using trainer."
            )
   
    def format_docs(self,docs):
        return "\n\n".join(doc.page_content for doc in docs)
   
    def create_embeddings(self):
        return HuggingFaceEmbeddings()
   
    def _define_model(self):
        if(self.model in ["gemma2","mistral","llama3.1","llama3","llama2"]):
           
            model = Ollama(model=self.model)
        elif(self.model == "gpt-4"):
            model = ChatOpenAI(
                        model="gpt-4",
                        temperature=0,
                        max_tokens=None,
                        timeout=None,
                        max_retries=2
            )
        elif(self.model == "gpt-4o"):
            model = ChatOpenAI(
                        model="gpt-4o",
                        temperature=0,
                        max_tokens=None,
                        timeout=None,
                        max_retries=2,
                       
            )
        elif(self.model == "gpt-3.5"):
            model = ChatOpenAI(
                        model="gpt-3.5-turbo",
                        temperature=0,
                        max_tokens=None,
                        timeout=None,
                        max_retries=2
            )
 
        return model
 
   
    def _create_qa_chain(self):
       
        rag_chain = (
                {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
                | self.prompt
                | self.model_obj
                | StrOutputParser()
            )
       
        return rag_chain
 
    def _create_prompt(self):
       
        prompt = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. keep the answer concise and Professional.
                    question: {question}
                    context: {context}
                    Answer:
                 """
        prompt = PromptTemplate.from_template(prompt)
        return prompt
 
 
    def answer_question(self, question: str) -> str:
       
        result = self.qa_chain.invoke(question)
        return result
 
 
 
# Usage example
if __name__ == "__main__":
    rag = AdvancedRAG(model="llama3.1")
   
    # Answer a question from the PDF
    question = '''
    Tell me about dynamic programming
    '''
    start_time = time.time()
    answer = rag.answer_question(question)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Question: {question} : Time Taken {execution_time} seconds")
    print(f"Answer: {answer}")
    
# 1000chunk size to 500
# Llama3 12.90 8.93 9.28 10.92 11.60 11.17
# Gemma2 16.06 11.24 14.76 13.97 17.64 15.78 
# Mistral 15.72 14.57 10.80 13.31 12.05 11.90