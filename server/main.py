from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from modules.load_vectorstore import load_vectorstore, PERSIST_DIR
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from logger import logger

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import os

app = FastAPI(title="RagBot2.0")

# Set up CORS middleware to explicitly allow your frontend's origin
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8501",  # Assuming Streamlit runs on this port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def catch_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception("UNHANDLED EXCEPTION")
        return JSONResponse(status_code=500, content={"error": str(exc)})

@app.post("/upload_pdfs/")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    try:
        logger.info(f"Received {len(files)} files")
        load_vectorstore(files)
        logger.info("Documents added to ChromaDB")
        return {"message": "Files processed and vectorstore updated"}
    except Exception as e:
        logger.exception("Error during PDF upload")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"user query: {question}")

        # Load Chroma vectorstore and retriever
        embedding = OpenAIEmbeddings(model="text-embedding-3-small")
        vectorstore = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embedding
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

        docs = retriever.invoke(question)
        
        # Get chain and query
        chain = get_llm_chain(retriever)
        result = query_chain(chain, question)

        # De-duplicate sources
        unique_sources = list(set([doc.metadata.get('source', 'Unknown') for doc in docs]))
        result['sources'] = unique_sources

        logger.info("Query successful")
        return result

    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/test")
async def test():
    return {"message": "Testing successful..."}
