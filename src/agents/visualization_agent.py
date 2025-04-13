import json
import datetime
import logging
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from typing import List, Dict, Any, Union, Optional
from pydantic import BaseModel
from ..utils.types import (
    GraphData,
    TimelineData,
    MapData,
    VisualizationData,
    CharacterRelation,
    TimelineEvent,
    Location
)

logger = logging.getLogger(__name__)

class GraphConfig(BaseModel):
    """Configuration for graph visualization."""
    node_color: str = "skyblue"
    node_size: int = 1500
    font_size: int = 10
    edge_font_size: int = 8
    title: str = "Character Relationship Graph"

class TimelineConfig(BaseModel):
    """Configuration for timeline visualization."""
    figsize: tuple[int, int] = (10, 6)
    marker_color: str = 'blue'
    linestyle: str = '--'
    fontsize: int = 8
    x_limits: tuple[float, float] = (0.99, 1.5)

class MapConfig(BaseModel):
    """Configuration for map visualization."""
    figsize: tuple[int, int] = (12, 8)
    marker_color: str = 'red'
    marker_size: int = 5
    fontsize: int = 8
    padding: int = 5

class VisualizationConfig(BaseModel):
    """General configuration for visualization."""
    graph: GraphConfig = GraphConfig()
    timeline: TimelineConfig = TimelineConfig()
    map: MapConfig = MapConfig()

class VisualizationAgent:
    """Agent for visualizing various types of data."""
    
    def __init__(self, config: Optional[VisualizationConfig] = None):
        """
        Initializes the agent with visualization configuration.
        
        Args:
            config: Visualization configuration. If None, default values are used
        """
        self.config = config or VisualizationConfig()
        logger.info("VisualizationAgent successfully initialized")
        
    def visualize(self, data: VisualizationData) -> None:
        """
        Visualizes data based on its type.
        
        Args:
            data: Data to visualize (graph, timeline, or map)
            
        Raises:
            ValueError: If the data format is not supported
        """
        try:
            if self._is_graph_data(data):
                logger.info("Visualizing relationship graph")
                self._visualize_graph(data)
            elif self._is_timeline_data(data):
                logger.info("Visualizing timeline")
                self._visualize_timeline(data)
            elif self._is_map_data(data):
                logger.info("Visualizing map")
                self._visualize_map(data)
            else:
                raise ValueError("Unsupported data format for visualization")
                
            logger.info("Visualization completed successfully")
            
        except Exception as e:
            logger.error(f"Error during data visualization: {str(e)}")
            raise ValueError(f"Failed to visualize data: {str(e)}")
            
    def _is_graph_data(self, data: VisualizationData) -> bool:
        """Checks if the data is a relationship graph."""
        if not isinstance(data, list):
            return False
        if not data:
            return False
        first_item = data[0]
        return isinstance(first_item, dict) and "name" in first_item and "links" in first_item
        
    def _is_timeline_data(self, data: VisualizationData) -> bool:
        """Checks if the data is a timeline."""
        if not isinstance(data, list):
            return False
        if not data:
            return False
        first_item = data[0]
        return isinstance(first_item, dict) and "date" in first_item and "event" in first_item
        
    def _is_map_data(self, data: VisualizationData) -> bool:
        """Checks if the data is a map."""
        if not isinstance(data, list):
            return False
        if not data:
            return False
        first_item = data[0]
        return isinstance(first_item, dict) and "name" in first_item and "coordinates" in first_item
        
    def _visualize_graph(self, data: GraphData) -> None:
        """Visualizes the relationship graph between characters."""
        try:
            G = nx.Graph()
            
            for character in data:
                name = character["name"]
                G.add_node(name)
                for linked_character, relation in character["links"].items():
                    G.add_edge(name, linked_character, relation=relation)

            pos = nx.spring_layout(G)
            nx.draw(
                G, pos,
                with_labels=True,
                node_color=self.config.graph.node_color,
                node_size=self.config.graph.node_size,
                font_size=self.config.graph.font_size
            )
            edge_labels = nx.get_edge_attributes(G, "relation")
            nx.draw_networkx_edge_labels(
                G, pos,
                edge_labels=edge_labels,
                font_size=self.config.graph.edge_font_size
            )
            
            plt.title(self.config.graph.title)
            plt.axis("off")
            plt.show()
            
        except Exception as e:
            logger.error(f"Error visualizing graph: {str(e)}")
            raise ValueError(f"Failed to visualize graph: {str(e)}")
            
    def _visualize_timeline(self, data: TimelineData) -> None:
        """Visualizes the timeline of events."""
        try:
            for event in data:
                event['date'] = datetime.datetime.strptime(event['date'], '%d %B')

            data.sort(key=lambda x: x['date'])

            dates = [event['date'] for event in data]
            events = [event['event'] for event in data]

            fig, ax = plt.subplots(figsize=self.config.timeline.figsize)
            ax.plot(
                [1] * len(dates), dates,
                marker='o',
                color=self.config.timeline.marker_color,
                linestyle=self.config.timeline.linestyle
            )

            for i, event in enumerate(events):
                ax.annotate(
                    event,
                    (1, dates[i]),
                    xytext=(10, 0),
                    textcoords='offset points',
                    ha='left',
                    va='center',
                    fontsize=self.config.timeline.fontsize
                )

            ax.yaxis.set_major_formatter(DateFormatter('%d %b %Y'))
            ax.set_xlim(self.config.timeline.x_limits)
            ax.set_xticks([])
            plt.gca().yaxis.set_tick_params(rotation=0)

            plt.tight_layout()
            plt.box(False)
            plt.gca().invert_yaxis()

            plt.show()
            
        except Exception as e:
            logger.error(f"Error visualizing timeline: {str(e)}")
            raise ValueError(f"Failed to visualize timeline: {str(e)}")
        
    def _visualize_map(self, data: MapData) -> None:
        """Visualizes the map with geographical objects."""
        try:
            longitudes = [float(coord[0]) for coord in [d['coordinates'] for d in data]]
            latitudes = [float(coord[1]) for coord in [d['coordinates'] for d in data]]
            names = [d['name'] for d in data]

            min_lon, max_lon = min(longitudes), max(longitudes)
            min_lat, max_lat = min(latitudes), max(latitudes)

            fig, ax = plt.subplots(
                figsize=self.config.map.figsize,
                subplot_kw={'projection': ccrs.PlateCarree()}
            )
            ax.add_feature(cfeature.LAND)
            ax.add_feature(cfeature.OCEAN)
            ax.add_feature(cfeature.COASTLINE, linewidth=0.3)
            ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.3)
            ax.add_feature(cfeature.LAKES, alpha=0.5)
            ax.add_feature(cfeature.RIVERS)

            for lon, lat, name in zip(longitudes, latitudes, names):
                ax.plot(
                    lon, lat,
                    marker='o',
                    color=self.config.map.marker_color,
                    markersize=self.config.map.marker_size,
                    transform=ccrs.PlateCarree()
                )
                ax.text(
                    lon, lat, name,
                    fontsize=self.config.map.fontsize,
                    transform=ccrs.PlateCarree(),
                    ha='right',
                    va='bottom'
                )

            ax.set_extent([
                min_lon - self.config.map.padding,
                max_lon + self.config.map.padding,
                min_lat - self.config.map.padding,
                max_lat + self.config.map.padding
            ], crs=ccrs.PlateCarree())

            plt.show()
            
        except Exception as e:
            logger.error(f"Error visualizing map: {str(e)}")
            raise ValueError(f"Failed to visualize map: {str(e)}") 