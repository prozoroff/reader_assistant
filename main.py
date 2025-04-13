from src.core.qa_system import create_qa_system
from src.agents.relation_agent import RelationGraphAgent
from src.agents.timeline_agent import TimelineAgent
from src.agents.geography_agent import GeographyAgent
from src.agents.visualization_agent import VisualizationAgent
import json
import logging
from typing import Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_agents() -> tuple[RelationGraphAgent, TimelineAgent, GeographyAgent, VisualizationAgent]:
    """Creates and returns all necessary agents."""
    qa = create_qa_system()
    return (
        RelationGraphAgent(qa),
        TimelineAgent(qa),
        GeographyAgent(qa),
        VisualizationAgent()
    )

def build_relation_graph(relation_agent: RelationGraphAgent, visualization_agent: VisualizationAgent) -> None:
    """Builds and visualizes the relationship graph between characters."""
    try:
        data = relation_agent.get_relations_data()
        logger.info("Relationship graph data received")
        logger.debug(json.dumps(data, ensure_ascii=False, indent=2))
        visualization_agent.visualize(data)
        logger.info("Relationship graph visualization completed")
    except Exception as e:
        logger.error(f"Error building graph: {str(e)}")
        raise
        
def build_timeline(timeline_agent: TimelineAgent, visualization_agent: VisualizationAgent) -> None:
    """Builds and visualizes the timeline of events."""
    try:
        data = timeline_agent.get_timeline_data()
        logger.info("Timeline data received")
        logger.debug(json.dumps(data, ensure_ascii=False, indent=2))
        visualization_agent.visualize(data)
        logger.info("Timeline visualization completed")
    except Exception as e:
        logger.error(f"Error building timeline: {str(e)}")
        raise
        
def build_map(geography_agent: GeographyAgent, visualization_agent: VisualizationAgent) -> None:
    """Builds and visualizes the map with geographical objects."""
    try:
        data = geography_agent.get_toponims_data()
        logger.info("Geographical objects data received")
        logger.debug(json.dumps(data, ensure_ascii=False, indent=2))
        visualization_agent.visualize(data)
        logger.info("Map visualization completed")
    except Exception as e:
        logger.error(f"Error building map: {str(e)}")
        raise

def main() -> None:
    """Main application function."""
    try:
        relation_agent, timeline_agent, geography_agent, visualization_agent = create_agents()
        
        build_relation_graph(relation_agent, visualization_agent)
        build_timeline(timeline_agent, visualization_agent)
        build_map(geography_agent, visualization_agent)
        
        logger.info("All visualizations successfully built")
    except Exception as e:
        logger.error(f"Critical error in application: {str(e)}")
        raise

if __name__ == "__main__":
    main() 