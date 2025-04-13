from typing import Dict, Any, List
import logging
import json
from langchain.chains import RetrievalQA
from ..utils.types import GraphData, CharacterRelation
from ..utils.string import extract_json_array

logger = logging.getLogger(__name__)

RELATIONS_QUERY = """Представь связь всех главных героев книги в виде списка в формате JSON, где каждый элемент имеет формат:
{
    "name": "имя одного героя",
    "links": {
        "имя другого героя": "тип отношений между ними",
        ...
    }
}
Тип отношений должен быть лаконичным, например: отец, сестра, друг, знакомый, cупруг и т.п."""

class RelationGraphAgent:
    """Agent for analyzing relationships between characters in the text."""
    
    def __init__(self, qa_system: RetrievalQA):
        """
        Initializes the agent with a question-answering system.
        
        Args:
            qa_system: Question-answering system for text analysis
        """
        self.qa = qa_system
        logger.info("RelationGraphAgent successfully initialized")
        
    def get_relations_data(self) -> List[CharacterRelation]:
        """
        Gets the list of relationships between characters.
        
        Returns:
            List[CharacterRelation]: List of relationships between characters
            
        Raises:
            ValueError: If failed to get or process data
        """
        try:
            logger.info("Requesting data about character relationships")
            result = self.qa({"query": RELATIONS_QUERY})
            
            logger.debug("Extracting JSON array from response")
            json_str = result['result']
            json_str = extract_json_array(json_str)
            
            logger.debug("Parsing JSON data")
            relations = json.loads(json_str)
            
            if not isinstance(relations, list):
                raise ValueError("Received data is not a list")
                
            logger.info(f"Successfully retrieved data for {len(relations)} characters")
            return relations
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            raise ValueError(f"Failed to parse JSON data: {str(e)}")
        except Exception as e:
            logger.error(f"Error getting relationship data: {str(e)}")
            raise ValueError(f"Failed to get relationship data: {str(e)}") 