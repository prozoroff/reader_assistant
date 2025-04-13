from typing import List, Optional
import time
import math
import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from pydantic import Field, ConfigDict, BaseModel
from langchain_community.embeddings.yandex import YandexGPTEmbeddings
from config import (
    YANDEX_API_KEY,
    YANDEX_FOLDER_ID,
    EMBEDDINGS_BATCH_SIZE,
    EMBEDDINGS_DELAY_BETWEEN_BATCHES
)

logger = logging.getLogger(__name__)

class EmbeddingsConfig(BaseModel):
    """Configuration for embeddings."""
    api_key: str
    folder_id: str
    batch_size: int
    delay_between_batches: float

class RateLimitedEmbeddings(YandexGPTEmbeddings):
    """Class for working with embeddings with request rate limiting."""
    
    batch_size: int = Field(default=EMBEDDINGS_BATCH_SIZE)
    delay_between_batches: float = Field(default=EMBEDDINGS_DELAY_BETWEEN_BATCHES)
    
    model_config = ConfigDict(extra='allow')
    
    def __init__(
        self,
        config: Optional[EmbeddingsConfig] = None,
        *args,
        **kwargs
    ):
        """
        Initializes embeddings with configuration.
        
        Args:
            config: Embeddings configuration. If None, values from config.py are used
            *args: Additional arguments for the parent class
            **kwargs: Additional named arguments for the parent class
        """
        if config is None:
            config = EmbeddingsConfig(
                api_key=YANDEX_API_KEY,
                folder_id=YANDEX_FOLDER_ID,
                batch_size=EMBEDDINGS_BATCH_SIZE,
                delay_between_batches=EMBEDDINGS_DELAY_BETWEEN_BATCHES
            )
            
        super().__init__(
            api_key=config.api_key,
            folder_id=config.folder_id,
            *args,
            **kwargs
        )
        self.batch_size = config.batch_size
        self.delay_between_batches = config.delay_between_batches

    @retry(
        retry=retry_if_exception_type(Exception),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _embed_batch(self, batch: List[str]) -> List[List[float]]:
        """
        Embeds a batch of texts with retries on errors.
        
        Args:
            batch: List of texts to embed
            
        Returns:
            List[List[float]]: List of embeddings
            
        Raises:
            Exception: If failed to embed the batch after all attempts
        """
        time.sleep(0.1)
        return super().embed_documents(batch)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds a list of texts with request rate control.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List[List[float]]: List of embeddings
            
        Raises:
            Exception: If failed to embed texts
        """
        try:
            logger.info(f"Embedding {len(texts)} texts")
            result = []
            
            for i in range(0, len(texts), self.batch_size):
                batch = texts[i:i + self.batch_size]
                logger.debug(f"Processing batch {i//self.batch_size + 1} of {math.ceil(len(texts)/self.batch_size)}")
                
                batch_result = self._embed_batch(batch)
                result.extend(batch_result)
                
                if i + self.batch_size < len(texts):
                    logger.debug(f"Waiting {self.delay_between_batches} seconds before next batch")
                    time.sleep(self.delay_between_batches)
            
            logger.info(f"Successfully embedded {len(result)} texts")
            return result
            
        except Exception as e:
            logger.error(f"Error embedding texts: {str(e)}")
            raise Exception(f"Failed to embed texts: {str(e)}") 