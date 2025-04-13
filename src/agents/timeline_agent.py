from typing import Dict, Any, List
import logging
import json
from langchain.chains import RetrievalQA
from ..utils.types import TimelineData, TimelineEvent
from ..utils.string import extract_json_array

logger = logging.getLogger(__name__)

TIMELINE_QUERY = """Составь список событий в книге в формате JSON:
[
    {
        "date": "Дата события по английски в английской локали",
        "event": "Краткое описание события по русски"
    }
]
Ограничься только 10 событиями"""

class TimelineAgent:
    """Agent for analyzing the timeline of events in the text."""
    
    def __init__(self, qa_system: RetrievalQA):
        """
        Initializes the agent with a question-answering system.
        
        Args:
            qa_system: Question-answering system for text analysis
        """
        self.qa = qa_system
        logger.info("TimelineAgent successfully initialized")
        
    def get_timeline_data(self) -> List[TimelineEvent]:
        """
        Gets the list of timeline events.
        
        Returns:
            List[TimelineEvent]: List of timeline events
            
        Raises:
            ValueError: If failed to get or process data
        """
        try:
            logger.info("Requesting timeline data")
            result = self.qa({"query": TIMELINE_QUERY})
            
            logger.debug("Extracting JSON array from response")
            json_str = result['result']
            json_str = extract_json_array(json_str)
            
            logger.debug("Parsing JSON data")
            events = json.loads(json_str)
            
            if not isinstance(events, list):
                raise ValueError("Received data is not a list")
                
            logger.info(f"Successfully retrieved data for {len(events)} events")
            return events
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            raise ValueError(f"Failed to parse JSON data: {str(e)}")
        except Exception as e:
            logger.error(f"Error getting timeline data: {str(e)}")
            raise ValueError(f"Failed to get timeline data: {str(e)}") 