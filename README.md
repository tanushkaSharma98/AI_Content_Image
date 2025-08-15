# AI Content Explorer 🚀

A full-stack AI tool where authenticated users can perform web searches, generate images, and manage their content history through an intuitive dashboard.

## ✨ Features

- 🔍 **Web Search**: Query web information using Tavily API with fallback to Wikipedia
- 🎨 **AI Image Generation**: Create images from text prompts using Flux ImageGen
- 📊 **Dashboard**: View, edit, and manage search/image history with filtering
- 🔐 **Authentication**: Secure JWT-based user registration and login
- 📱 **Responsive UI**: Modern React interface with Tailwind CSS
- 🧪 **Complete Testing**: Unit, Integration, and E2E tests with 52% coverage

## 🏗️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **AI Services**: 
  - Tavily API for web search
  - Flux ImageGen for image generation
- **Testing**: Pytest with async support

### Frontend
- **Framework**: React 18 with hooks
- **Styling**: Tailwind CSS
- **State Management**: React hooks and context
- **Testing**: Playwright for E2E tests

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 12+
- Git

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/ai-content-explorer.git
cd ai-content-explorer
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and database settings

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd auth-ui

# Install dependencies
npm install

# Start development server
npm start
```

### 4. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔑 Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/ai_content_explorer

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys
TAVILY_API_KEY=your-tavily-api-key
FLUX_API_TOKEN=your-flux-api-token

# App Settings
APP_NAME=AI Content Explorer
DEBUG=True
```

## 🧪 Running Tests

### Single Command (All Tests)
```bash
cd backend
.venv\Scripts\python.exe -m pytest tests -v --cov=app --cov-report=term-missing
```

### Individual Test Categories
```bash
# Unit Tests
.venv\Scripts\python.exe -m pytest tests/unit -v

# Integration Tests  
.venv\Scripts\python.exe -m pytest tests/integration -v

# E2E Tests
.venv\Scripts\python.exe -m pytest tests/e2e -v --headed
```

## 📖 API Documentation

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh access token

### Search Endpoints
- `POST /search/` - Perform web search query

### Image Generation Endpoints
- `POST /image/generate` - Generate image from prompt

### Dashboard Endpoints
- `GET /dashboard/history` - Get user history
- `GET /dashboard/stats` - Get dashboard statistics
- `GET /dashboard/history/{item_id}` - Get specific history item
- `PUT /dashboard/history/{item_id}` - Update history item
- `DELETE /dashboard/history/{item_id}` - Delete history item
- `DELETE /dashboard/history/bulk` - Bulk delete history

## 🗄️ Database Schema

### Users Table
- `id` (Primary Key)
- `email` (Unique)
- `hashed_password`
- `is_active`
- `created_at`
- `updated_at`

### History Table
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `type` (search/image)
- `prompt`
- `result_title`
- `result_summary`
- `result_url`
- `extra_data` (JSON)
- `is_hidden`
- `created_at`
- `updated_at`

## 🔧 Development

### Project Structure
```
ai-content-explorer/
├── backend/
│   ├── app/
│   │   ├── api/routes/     # API endpoints
│   │   ├── core/           # Configuration
│   │   ├── db/             # Database models
│   │   ├── services/       # Business logic
│   │   └── schemas/        # Pydantic models
│   ├── tests/              # Test suite
│   └── requirements.txt    # Python dependencies
├── auth-ui/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   └── package.json        # Node dependencies
└── README.md
```

### Adding New Features
1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes with tests
3. Run test suite: `pytest tests -v`
4. Submit pull request

## 🚀 Deployment

### Production Setup
1. Set `DEBUG=False` in environment
2. Use production PostgreSQL instance
3. Configure CORS for production domain
4. Set up reverse proxy (nginx)
5. Use production-grade WSGI server (gunicorn)

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Ensure all tests pass
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-content-explorer/issues)
- **Documentation**: [API Docs](http://localhost:8000/docs)
- **Email**: your-email@example.com

## 🎯 Roadmap

- [ ] User roles and permissions
- [ ] Advanced search filters
- [ ] Image style customization
- [ ] Export functionality
- [ ] Mobile app
- [ ] API rate limiting
- [ ] Caching layer
- [ ] Analytics dashboard

---

**Built with ❤️ using FastAPI, React, and modern web technologies**
