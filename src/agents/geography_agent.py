from typing import List, Dict, Any
import logging
from langchain.chains import RetrievalQA
from yandex_geocoder import Client
from ..utils.types import MapData, Location
from config import YANDEX_GEOCODER_API_KEY

logger = logging.getLogger(__name__)

GEOGRAPHY_QUERY = """Выведи список географических объектов из текста. Только названия через запятую."""

class GeographyAgent:
    """Agent for analyzing geographical objects in the text."""
    
    def __init__(self, qa_system: RetrievalQA):
        """
        Initializes the agent with a question-answering system.
        
        Args:
            qa_system: Question-answering system for text analysis
        """
        self.qa = qa_system
        self.locator = Client(YANDEX_GEOCODER_API_KEY)
        logger.info("GeographyAgent successfully initialized")
        
    def get_coordinates(self, text: str) -> List[Location]:
        """
        Gets coordinates for a list of geographical objects.
        
        Args:
            text: String with geographical object names separated by commas
            
        Returns:
            List[Location]: List of objects with coordinates
            
        Raises:
            ValueError: If failed to get coordinates
        """
        try:
            locations = text.split(', ')
            result = []
            logger.info(f"Getting coordinates for {len(locations)} objects")
            
            for loc in set(locations):  # Remove duplicates
                try:
                    logger.debug(f"Requesting coordinates for {loc}")
                    coords = self.locator.coordinates(loc)
                    if coords:
                        result.append({"name": loc, "coordinates": [str(c) for c in coords]})
                        logger.debug(f"Coordinates for {loc} successfully obtained")
                except Exception as e:
                    logger.warning(f"Failed to get coordinates for {loc}: {str(e)}")
                    continue
            
            logger.info(f"Successfully obtained coordinates for {len(result)} objects")
            return result
            
        except Exception as e:
            logger.error(f"Error getting coordinates: {str(e)}")
            raise ValueError(f"Failed to get coordinates: {str(e)}")
        
    def get_toponims_data(self) -> List[Location]:
        """
        Gets a list of geographical objects with coordinates.
        
        Returns:
            List[Location]: List of objects with coordinates
            
        Raises:
            ValueError: If failed to get or process data
        """
        try:
            logger.info("Requesting list of geographical objects")
            result = self.qa({"query": GEOGRAPHY_QUERY})
            
            logger.debug("Getting coordinates for objects")
            coordinates_json = self.get_coordinates(result['result'])
            
            if not coordinates_json:
                logger.warning("Failed to get coordinates for any object")
                
            logger.info(f"Successfully processed data for {len(coordinates_json)} objects")
            return coordinates_json
            
        except Exception as e:
            logger.error(f"Error processing geographical data: {str(e)}")
            raise ValueError(f"Failed to process geographical data: {str(e)}") 