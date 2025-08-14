# AI Content Explorer

A full-stack AI tool where users can perform web searches and generate images using MCP servers, with authentication and history management.

## Features

- 🔐 **User Authentication**: Register, login, and JWT-based authorization
- 🔍 **Web Search**: Search the web using Tavily MCP server
- 🎨 **Image Generation**: Generate images from text using Flux ImageGen MCP server
- 📊 **Dashboard**: View, filter, and manage search/image history
- 🗑️ **Soft Delete**: Delete items from dashboard (kept in database)
- 📱 **Responsive UI**: Modern React + Tailwind CSS interface

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Alembic
- **Frontend**: React, TypeScript, Tailwind CSS, Vite
- **Database**: PostgreSQL with migrations
- **Authentication**: JWT tokens
- **MCP Servers**: 
  - Tavily Search: https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp
  - Flux ImageGen: https://smithery.ai/server/@falahgs/flux-imagegen-mcp-server

## Project Structure

```
AI_Content_Image/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/routes/      # API endpoints
│   │   ├── core/           # Configuration & security
│   │   ├── db/             # Database models & setup
│   │   ├── schemas/        # Pydantic models
│   │   └── services/       # Business logic
│   ├── alembic/            # Database migrations
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/          # Page components
│   │   ├── components/     # Reusable components
│   │   └── lib/           # API client & utilities
│   └── package.json
├── docker-compose.yml      # PostgreSQL & pgAdmin
└── README.md
```

## Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `hashed_password`
- `role` (user/admin)
- `is_active`
- `created_at`, `updated_at`

### History Table
- `id` (Primary Key)
- `user_id` (Foreign Key to users)
- `type` (search/image)
- `prompt` (user input)
- `result_title` (for search results)
- `result_summary` (for search results)
- `result_url` (search link or image URL)
- `metadata` (JSON for extra data)
- `is_hidden` (soft delete flag)
- `created_at`, `updated_at`

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker & Docker Compose

### 1. Clone and Setup
```bash
git clone <repository-url>
cd AI_Content_Image
```

### 2. Start Database
```bash
docker-compose up -d
```

### 3. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp env.example .env
# Edit .env with your database credentials

# Setup database and run migrations
python setup_db.py

# Start backend server
uvicorn app.main:app --reload
```

### 4. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 5. Access the Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- pgAdmin: http://localhost:5050 (admin@admin.com / admin)

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/refresh` - Refresh JWT token
- `GET /auth/me` - Get current user profile

### Search & Image Generation
- `POST /search` - Search web using Tavily MCP
- `POST /image` - Generate image using Flux MCP

### Dashboard
- `GET /dashboard/items` - Get saved items with filters
- `GET /dashboard/items/{id}` - Get specific item
- `PATCH /dashboard/items/{id}` - Update item
- `DELETE /dashboard/items/{id}` - Soft delete item
- `DELETE /dashboard/items` - Bulk delete items

## Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Database Migrations
```bash
cd backend

# Create new migration
alembic revision --autogenerate -m "Description"

# Run migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/ai_content_db
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MCP_TAVILY_URL=https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp
MCP_FLUX_URL=https://smithery.ai/server/@falahgs/flux-imagegen-mcp-server
DEBUG=True
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.