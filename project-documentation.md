# Solar Panel AI Assistant

An intelligent chatbot system designed to provide information and assistance regarding solar panels, installation, costs, and market trends using Google's Gemini-Pro API and document retrieval system.

## Implementation Documentation

### Architecture Overview

The project consists of two main components:

1. **Frontend Application (Streamlit)**
   - User interface for chat interactions
   - Real-time message handling
   - Responsive design with custom CSS
   - Session state management

2. **Backend System (Jupyter Notebook)**
   - Document processing pipeline
   - Vector database management
   - Similarity search functionality
   - Integration with Google's Gemini-Pro API

### Key Features

- **Document Processing**
  - PDF extraction and parsing
  - Text chunking and vectorization
  - Metadata management
  - Vector database creation using Chroma DB

- **Search and Retrieval**
  - Semantic similarity search
  - Relevance scoring
  - Context-aware responses
  - Multi-document knowledge base

- **User Interface**
  - Clean, modern design
  - Real-time chat interface
  - Message history management
  - Responsive layout

## Setup Guide

### Prerequisites

- Python 3.10+
- Git
- pip (Python package manager)

### Required Dependencies

```plaintext
streamlit
google-generativeai
python-dotenv
langchain
chromadb
pypdf2
sentence-transformers
pandas
numpy
requests
```

### Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/solar-panel-assistant.git
cd solar-panel-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```plaintext
GOOGLE_API_KEY=your_google_api_key_here
```

### Step-by-Step Run Commands

1. First, process the documents and create the vector database:
```bash
jupyter notebook backend.ipynb
```
- Run all cells in the notebook to process documents and create the vector database

2. Start the Streamlit application:
```bash
streamlit run 1.py
```

The application will be available at `http://localhost:8501`

## Example Conversations

[Space reserved for example conversations to be added later]

## Future Improvements

1. **Enhanced Search Capabilities**
   - Implement hybrid search combining semantic and keyword matching
   - Add support for multi-language queries
   - Improve context retention across conversations

2. **User Interface Enhancements**
   - Add dark mode support
   - Implement file upload functionality for custom documents
   - Add visualization tools for solar panel data

3. **Backend Optimizations**
   - Implement caching for frequent queries
   - Add support for real-time document updates
   - Improve response time through query optimization

4. **Additional Features**
   - Integration with solar panel pricing APIs
   - Real-time energy production calculations
   - Custom installation cost estimator
   - ROI calculator

## Performance Considerations

- The vector database is optimized for quick retrieval with chunk sizes of 300 tokens
- Document processing is done once during setup to create efficient embeddings
- The chat interface is designed to handle concurrent users efficiently
- Response times are typically under 2 seconds for most queries

## Support and Maintenance

For any issues or questions, please:
1. Check the existing documentation
2. Review the example conversations
3. Submit an issue on the GitHub repository
4. Contact the development team

[Example Usage section to be added later]
