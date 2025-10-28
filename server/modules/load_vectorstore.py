import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
#from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from logger import logger

# Directory where Chroma will persist data
PERSIST_DIR = "chroma_store"

def load_vectorstore(files):
    try:
        all_docs = []

        # 1. Process uploaded PDF files
        for file in files:
            logger.info(f"Processing file: {file.filename}")

            # Save uploaded file temporarily
            temp_path = f"temp_{file.filename}"
            with open(temp_path, "wb") as f:
                f.write(file.file.read())

            # Load PDF
            loader = PyPDFLoader(temp_path)
            docs = loader.load()
            all_docs.extend(docs)

            # Delete temp file
            os.remove(temp_path)

        logger.info(f"Loaded {len(all_docs)} pages from PDFs")

        # 2. Split documents into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs_split = splitter.split_documents(all_docs)

        logger.info(f"Split into {len(docs_split)} chunks")

        # 3. Initialize embedding model
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # 4. Create or update Chroma vectorstore
        vectorstore = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embeddings
        )

        vectorstore.add_documents(docs_split)
        vectorstore.persist()

        logger.info("Documents successfully added to ChromaDB")

    except Exception as e:
        logger.exception("Error in load_vectorstore")
        raise e
