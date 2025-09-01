from typing import List, Dict, Any
import logging
import json
import os
from pathlib import Path
from langchain.chains import RetrievalQA
from ..utils.types import MermaidData, MermaidDiagram
from ..utils.string import extract_json_array

logger = logging.getLogger(__name__)

MERMAID_QUERY_TEMPLATE = """Изучи этот файл с художественным произведением и придумай и оформи в виде списка mermaid диаграмм с коротким описанием несколько вариантов инфографики по содержанию произведения.

Не больше 10 диаграмм.

Они должны быть понятными и интересными.

Вот некоторые примеры хороших диаграмм:

{examples}

Не обязательно использовать все эти типы инфографики, если они не подходят для этого произведения. Я лишь привел примеры того, что мне понравилось ранее.

Верни результат в формате JSON массива:
[
    {
        "title": "Краткое название диаграммы",
        "code": "код mermaid диаграммы",
        "type": "тип диаграммы (timeline, flowchart, graph, classDiagram, sequenceDiagram, mindmap, pie и т.д.)"
    }
]"""

class MermaidAgent:
    """Agent for generating mermaid diagrams based on literary work content."""
    
    def __init__(self, qa_system: RetrievalQA):
        """
        Initializes the agent with a question-answering system.
        
        Args:
            qa_system: Question-answering system for text analysis
        """
        self.qa = qa_system
        self.examples_file_path = Path(__file__).parent / "mermaid_examples.txt"
        logger.info("MermaidAgent successfully initialized")
    
    def _load_examples(self) -> str:
        """
        Loads mermaid diagram examples from the external file.
        
        Returns:
            str: Content of the examples file
            
        Raises:
            ValueError: If the examples file cannot be read
        """
        try:
            if not self.examples_file_path.exists():
                raise FileNotFoundError(f"Examples file not found: {self.examples_file_path}")
                
            with open(self.examples_file_path, 'r', encoding='utf-8') as f:
                examples_content = f.read()
                
            logger.debug(f"Successfully loaded examples from {self.examples_file_path}")
            return examples_content
            
        except Exception as e:
            logger.error(f"Error loading examples file: {str(e)}")
            raise ValueError(f"Failed to load examples file: {str(e)}")
        
    def get_mermaid_diagrams(self) -> List[MermaidDiagram]:
        """
        Gets the list of mermaid diagrams for the literary work.
        
        Returns:
            List[MermaidDiagram]: List of mermaid diagrams with titles, code and types
            
        Raises:
            ValueError: If failed to get or process data
        """
        try:
            logger.info("Loading mermaid examples from file")
            examples = self._load_examples()
            
            logger.info("Building query with examples")
            query = MERMAID_QUERY_TEMPLATE.format(examples=examples)
            
            logger.info("Requesting mermaid diagrams data")
            result = self.qa({"query": query})
            
            logger.debug("Extracting JSON array from response")
            json_str = result['result']
            json_str = extract_json_array(json_str)
            
            logger.debug("Parsing JSON data")
            diagrams = json.loads(json_str)
            
            if not isinstance(diagrams, list):
                raise ValueError("Received data is not a list")
                
            # Validate diagram structure
            for diagram in diagrams:
                if not isinstance(diagram, dict):
                    raise ValueError("Diagram is not a dictionary")
                if not all(key in diagram for key in ['title', 'code', 'type']):
                    raise ValueError("Diagram missing required keys: title, code, type")
                    
            logger.info(f"Successfully retrieved {len(diagrams)} mermaid diagrams")
            return diagrams
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            raise ValueError(f"Failed to parse JSON data: {str(e)}")
        except Exception as e:
            logger.error(f"Error getting mermaid diagrams data: {str(e)}")
            raise ValueError(f"Failed to get mermaid diagrams data: {str(e)}")