# Reader's Assistant

A project for analyzing and visualizing text data using LLM.

[Explanatory article](https://habr.com/ru/articles/900870/)

[Examples of infographics](https://prozoroff.github.io/reader_assistant/mermaid/)

## Features

- Analysis of character relationships and building a relationship graph
- Creation of event timeline
- Visualization of geographical objects on a map

## Installation

1. Clone the repository:
```bash
git clone https://github.com/prozoroff/reader_assistant.git
cd reader_assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a configuration file `.env` with your API keys:
```
YANDEX_API_KEY=your_api_key
YANDEX_FOLDER_ID=your_folder_id
YANDEX_GEOCODER_API_KEY=your_geocoder_key
```

## Usage

1. Place the text file for analysis in the `data/` directory
2. Run the main script:
```bash
python main.py
```

## Project Structure

```
reader_assistant/
├── README.md
├── requirements.txt
├── config.py
├── main.py
├── src/
│   ├── agents/
│   │   ├── relation_agent.py    # Character relationship analysis
│   │   ├── timeline_agent.py    # Event timeline analysis
│   │   ├── geography_agent.py   # Geographical objects analysis
│   │   └── visualization_agent.py # Data visualization
│   ├── core/
│   │   ├── embeddings.py        # Embeddings processing
│   │   └── qa_system.py         # Question-answering system
│   └── utils/
│       ├── types.py             # Data types
│       └── string.py            # String utilities
└── data/
    └── dairy.txt                # Example text file
```

## Main Components

### Agents

- `RelationGraphAgent`: Analyzes relationships between characters
- `TimelineAgent`: Creates event timeline
- `GeographyAgent`: Analyzes geographical objects
- `VisualizationAgent`: Visualizes data based on its type

### Data Types

- `CharacterRelation`: Describes relationships between characters
- `TimelineEvent`: Describes an event on the timeline
- `Location`: Describes a geographical object
- `VisualizationData`: Union of all data types for visualization

### Utilities

- `extract_json_array`: Extracts a JSON array from a string
- `RateLimitedEmbeddings`: Class for working with embeddings with request rate limiting

## Dependencies

- langchain>=0.1.0
- langchain-community>=0.0.10
- faiss-cpu>=1.7.4
- networkx>=3.1
- matplotlib>=3.7.1
- cartopy>=0.21.1
- yandex-geocoder>=0.1.0
- pydantic>=2.5.0
- tenacity>=8.2.2

## Usage Examples

```python
from src.core.qa_system import create_qa_system
from src.agents.relation_agent import RelationGraphAgent
from src.agents.visualization_agent import VisualizationAgent

qa = create_qa_system()

relation_agent = RelationGraphAgent(qa)
data = relation_agent.get_relations_data()

visualization_agent = VisualizationAgent()
visualization_agent.visualize(data)
```

## License

MIT 
