import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import Mock, patch

from app.main import app
from app.db.base import get_db, Base
from app.core.config import settings
from app.core.security import create_access_token
from app.db.models.user import User
from app.db.models.history import History

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop tables
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with a fresh database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4tbQJ8Kq8e",  # "password123"
        is_active=True,
        role="user"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_user_token(test_user):
    """Create a JWT token for the test user."""
    return create_access_token(data={"sub": test_user.email})

@pytest.fixture
def authenticated_client(client, test_user_token):
    """Create a test client with authentication."""
    client.headers.update({"Authorization": f"Bearer {test_user_token}"})
    return client

@pytest.fixture
def mock_mcp_gateway():
    """Mock MCP gateway responses."""
    with patch('app.services.mcp_gateway.call_tavily_search') as mock_tavily, \
         patch('app.services.mcp_gateway.call_flux_generate_image_url') as mock_flux:
        
        # Mock Tavily search response
        mock_tavily.return_value = {
            "result_title": "Test Search Result",
            "result_summary": "This is a test search result summary.",
            "result_url": "https://example.com/test-result"
        }
        
        # Mock Flux image generation response
        mock_flux.return_value = {
            "result_title": "Generated Image",
            "result_summary": "Image generated successfully",
            "result_url": "https://example.com/generated-image.jpg"
        }
        
        yield {
            'tavily': mock_tavily,
            'flux': mock_flux
        }

@pytest.fixture
def sample_search_history(db_session, test_user):
    """Create sample search history for testing."""
    history = History(
        user_id=test_user.id,
        type="search",
        prompt="What is quantum computing?",
        result_title="Quantum Computing Explained",
        result_summary="Quantum computing is a type of computation...",
        result_url="https://example.com/quantum-computing",
        is_hidden=False
    )
    db_session.add(history)
    db_session.commit()
    db_session.refresh(history)
    return history

@pytest.fixture
def sample_image_history(db_session, test_user):
    """Create sample image generation history for testing."""
    history = History(
        user_id=test_user.id,
        type="image",
        prompt="A beautiful sunset over mountains",
        result_title="Generated Sunset Image",
        result_summary="AI-generated image of a sunset",
        result_url="https://example.com/sunset-image.jpg",
        is_hidden=False
    )
    db_session.add(history)
    db_session.commit()
    db_session.refresh(history)
    return history
