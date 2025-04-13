from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import YandexGPT
from pathlib import Path
import logging
from typing import Optional
from pydantic import BaseModel

from config import (
    FILE_PATH,
    TEXT_SPLITTER_CHUNK_SIZE,
    TEXT_SPLITTER_OVERLAP,
    YANDEX_API_KEY,
    YANDEX_FOLDER_ID,
    SEARCH_K
)
from .embeddings import RateLimitedEmbeddings

logger = logging.getLogger(__name__)

class QASystemConfig(BaseModel):
    """Configuration for the question-answering system."""
    file_path: Path
    chunk_size: int
    chunk_overlap: int
    api_key: str
    folder_id: str
    search_k: int
    model_uri: str = f'gpt://{YANDEX_FOLDER_ID}/yandexgpt-32k/latest'

def create_qa_system(config: Optional[QASystemConfig] = None) -> RetrievalQA:
    """
    Creates and configures the question-answering system.
    
    Args:
        config: System configuration. If None, values from config.py are used
        
    Returns:
        RetrievalQA: Configured question-answering system
        
    Raises:
        ValueError: If system creation fails
    """
    try:
        if config is None:
            config = QASystemConfig(
                file_path=FILE_PATH,
                chunk_size=TEXT_SPLITTER_CHUNK_SIZE,
                chunk_overlap=TEXT_SPLITTER_OVERLAP,
                api_key=YANDEX_API_KEY,
                folder_id=YANDEX_FOLDER_ID,
                search_k=SEARCH_K
            )
            
        logger.info("Loading and splitting text")
        loader = TextLoader(str(config.file_path), encoding="utf-8")
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap
        )
        texts = text_splitter.split_documents(documents)
        logger.info(f"Text split into {len(texts)} chunks")
        
        logger.info("Initializing embeddings and vector store")
        embeddings = RateLimitedEmbeddings()
        vectorstore = FAISS.from_documents(texts, embeddings)
        
        logger.info("Initializing LLM")
        llm = YandexGPT(
            api_key=config.api_key,
            folder_id=config.folder_id,
            model_uri=config.model_uri
        )
        
        logger.info("Creating QA system")
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="map_reduce",
            retriever=vectorstore.as_retriever(search_kwargs={"k": config.search_k}),
            return_source_documents=False
        )
        
        logger.info("QA system successfully created")
        return qa
        
    except Exception as e:
        logger.error(f"Error creating QA system: {str(e)}")
        raise ValueError(f"Failed to create question-answering system: {str(e)}") 