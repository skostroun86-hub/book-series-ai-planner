# AI Book Series Planner

A comprehensive AI environment for planning and writing your book series with advanced features like conversation memory, character tracking, plot management, and semantic search.

## Features

✨ **Advanced AI Capabilities**
- Multi-turn conversation memory (persistent across sessions)
- Context window management (intelligent truncation)
- Character & plot consistency tracking
- Semantic search with vector embeddings (RAG)
- Role-based prompting (Story Architect, Editor, Brainstormer)
- Writing analysis and suggestions

🎯 **Book Series Management**
- Book/Series organization
- Character database with consistency checks
- Plot timeline management
- World-building and lore storage
- Writing progress tracking
- Scene and chapter organization

💾 **Storage & Memory**
- Persistent conversation history
- Vector embeddings for semantic search
- Character profiles with relationships
- Plot points and story arcs
- Writing notes and references

🌐 **Web Interface**
- React-based frontend
- Real-time chat interface
- Book management dashboard
- Character browser
- Timeline visualization
- Writing statistics

🚀 **Deployment**
- Docker Compose for easy setup
- Local LLM integration (Ollama)
- RESTful API
- Production-ready

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Ollama (for local LLM)
- Node.js 18+ (for frontend development)
- Python 3.10+ (for backend development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/skostroun86-hub/book-series-ai-planner.git
   cd book-series-ai-planner
   ```

2. **Install Ollama** (if not already installed)
   - Download from https://ollama.com
   - Pull a model: `ollama pull llama2` or `ollama pull mistral`
   - Run: `ollama serve`

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

4. **Start with Docker Compose**
   ```bash
   docker-compose up
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Manual Setup (Development)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python run.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## Project Structure

```
book-series-ai-planner/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry
│   │   ├── config.py          # Configuration
│   │   ├── database.py        # Database setup
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py        # Chat endpoints
│   │   │   ├── books.py       # Book management
│   │   │   ├── characters.py  # Character management
│   │   │   ├── plots.py       # Plot management
│   │   │   └── search.py      # Semantic search
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── llm.py         # LLM integration
│   │   │   ├── memory.py      # Memory management
│   │   │   ├── embeddings.py  # Vector embeddings
│   │   │   ├── rag.py         # RAG system
│   │   │   └── consistency.py # Character/plot checking
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── prompts.py     # Prompt templates
│   │       └── helpers.py     # Utility functions
│   ├── requirements.txt
│   ├── run.py
│   └── Dockerfile
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── BookManager.tsx
│   │   │   ├── CharacterBrowser.tsx
│   │   │   ├── Timeline.tsx
│   │   │   └── Dashboard.tsx
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── Editor.tsx
│   │   │   ├── Characters.tsx
│   │   └── PlotBoard.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── hooks/
│   │   │   ├── useChat.ts
│   │   │   └── useMemory.ts
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   ├── Dockerfile
│   └── tsconfig.json
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## API Endpoints

### Chat
- `POST /api/chat/message` - Send message with conversation memory
- `GET /api/chat/history/{conversation_id}` - Get conversation history
- `POST /api/chat/role` - Switch AI role (architect, editor, brainstormer)
- `POST /api/chat/clear` - Clear conversation memory

### Books
- `GET /api/books` - List all books
- `POST /api/books` - Create new book
- `GET /api/books/{book_id}` - Get book details
- `PUT /api/books/{book_id}` - Update book
- `DELETE /api/books/{book_id}` - Delete book

### Characters
- `GET /api/characters` - List all characters
- `POST /api/characters` - Create character
- `GET /api/characters/{char_id}` - Get character details
- `PUT /api/characters/{char_id}` - Update character
- `POST /api/characters/check-consistency` - Check consistency

### Plots
- `GET /api/plots` - List all plot points
- `POST /api/plots` - Create plot point
- `GET /api/plots/timeline` - Get timeline view
- `POST /api/plots/analyze` - Analyze plot coherence

### Search
- `POST /api/search/semantic` - Semantic search across all content
- `POST /api/search/characters` - Find similar characters
- `POST /api/search/plots` - Find related plot points

## Configuration

Edit `.env` to customize:

```env
# LLM Configuration
LLM_MODEL=llama2              # or mistral, neural-chat, etc.
OLLAMA_API_URL=http://localhost:11434
CONTEXT_WINDOW=4096           # Max tokens for context

# Database
DATABASE_URL=sqlite:///./book_planner.db

# Embeddings
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Memory Management
MAX_MEMORY_TURNS=20           # Number of turns to keep in memory
MEMORY_CHUNK_SIZE=1000        # Tokens per chunk

# API
API_HOST=0.0.0.0
API_PORT=8000

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

## Memory Management

The system maintains intelligent conversation memory:

1. **Short-term Memory** - Recent turns (kept in context)
2. **Long-term Memory** - Summarized past conversations (stored in DB)
3. **Semantic Memory** - Vector embeddings for RAG
4. **Entity Memory** - Characters, plots, locations (structured storage)

When context gets too large:
1. Recent turns are preserved
2. Older turns are summarized
3. Summaries stored in vector DB
4. Retrieved when relevant to current conversation

## Advanced Features

### Character Consistency Checking
```bash
POST /api/characters/check-consistency
{
  "character_id": "char_123",
  "recent_context": "character interactions from last 5 chapters"
}
```

Responses:
- Trait inconsistencies
- Dialogue style changes
- Motivation alignment
- Relationship consistency

### Plot Coherence Analysis
```bash
POST /api/plots/analyze
{
  "book_id": "book_123"
}
```

Analyzes:
- Plot hole detection
- Pacing issues
- Subplot integration
- Climax alignment

### Semantic Search
```bash
POST /api/search/semantic
{
  "query": "magic system conflicts with earlier rules",
  "limit": 5
}
```

Finds related content across all books/chapters.

## Role-Based AI Prompting

Switch between specialized AI roles:

1. **Story Architect** - Plot planning, structure, pacing
2. **Character Psychologist** - Character development, motivation, arcs
3. **Worldbuilder** - Lore, consistency, geographic/magical systems
4. **Editor** - Writing quality, clarity, grammar, style
5. **Brainstormer** - Creative ideas, plot twists, surprises
6. **Writing Coach** - Motivation, progress tracking, tips

## Performance Optimization

- Vector embeddings cached locally
- Conversation history paginated
- Context window optimized per model
- Batch processing for character checks
- Incremental search indexing

## Troubleshooting

### Ollama Connection Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Pull a model if needed
ollama pull llama2
```

### Database Issues
```bash
# Reset database
rm book_planner.db
# Backend will recreate on startup
```

### Memory Issues
Reduce `MAX_MEMORY_TURNS` in `.env` or increase `MEMORY_CHUNK_SIZE`.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/skostroun86-hub/book-series-ai-planner/issues
- Discussions: https://github.com/skostroun86-hub/book-series-ai-planner/discussions

## Roadmap

- [ ] Multi-language support
- [ ] Collaborative editing
- [ ] Mobile app
- [ ] Advanced visualization dashboard
- [ ] Export to multiple formats (PDF, EPUB, Word)
- [ ] Integration with popular writing tools (Scrivener, Word)
- [ ] Voice dictation support
- [ ] Custom fine-tuning for your writing style
