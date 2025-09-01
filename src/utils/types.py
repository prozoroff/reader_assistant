from typing import TypedDict, List, Dict, Any, Union, Literal
from datetime import datetime

class CharacterRelation(TypedDict):
    """
    Type for representing relationships between characters.
    
    Attributes:
        name: Character name
        links: Dictionary of relationships with other characters, where key is another character's name,
               value is relationship type (e.g., "father", "sister", "friend")
    """
    name: str
    links: Dict[str, str]

class TimelineEvent(TypedDict):
    """
    Type for representing an event on the timeline.
    
    Attributes:
        date: Event date as a string
        event: Event description
    """
    date: str
    event: str

class Location(TypedDict):
    """
    Type for representing a geographical object.
    
    Attributes:
        name: Object name
        coordinates: List of coordinates [longitude, latitude] as strings
    """
    name: str
    coordinates: List[str]

class GraphData(List[CharacterRelation]):
    """
    Type for representing relationship graph data.
    List of relationships between characters.
    """

class TimelineData(List[TimelineEvent]):
    """
    Type for representing timeline data.
    List of events in chronological order.
    """

class MapData(List[Location]):
    """
    Type for representing map data.
    List of geographical objects with coordinates.
    """

class MermaidDiagram(TypedDict):
    """
    Type for representing a mermaid diagram.
    
    Attributes:
        title: Short title/description of the diagram
        code: Mermaid diagram code
        type: Type of diagram (timeline, flowchart, graph, etc.)
    """
    title: str
    code: str
    type: str

class MermaidData(List[MermaidDiagram]):
    """
    Type for representing mermaid diagrams data.
    List of mermaid diagrams with descriptions.
    """

VisualizationData = Union[GraphData, TimelineData, MapData, MermaidData]
"""
Type for representing data that can be visualized.
Can be a relationship graph, timeline, map, or mermaid diagrams.
"""