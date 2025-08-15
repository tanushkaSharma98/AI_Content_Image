import pytest
from fastapi import HTTPException
from unittest.mock import patch, MagicMock

from app.core.security import verify_password, get_password_hash, create_access_token, verify_token

class TestSecurity:
    """Test security utilities."""
    
    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        # Should not be the same as original
        assert hashed != password
        
        # Should verify correctly
        assert verify_password(password, hashed) is True
        
        # Should not verify with wrong password
        assert verify_password("wrongpassword", hashed) is False
    
    def test_token_creation_and_verification(self):
        """Test JWT token creation and verification."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data=data)
        
        # Token should be a string
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Should verify correctly
        payload = verify_token(token)
        assert payload["sub"] == "test@example.com"
    
    def test_invalid_token_verification(self):
        """Test token verification with invalid token."""
        result = verify_token("invalid_token")
        assert result is None

class TestAuthLogic:
    """Test authentication logic without HTTP client."""
    
    def test_password_verification_logic(self):
        """Test password verification logic."""
        # Test valid password
        password = "securepassword123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True
        
        # Test invalid password
        assert verify_password("wrongpassword", hashed) is False
        
        # Test empty password
        assert verify_password("", hashed) is False
    
    def test_token_creation_with_expiry(self):
        """Test token creation with custom expiry."""
        from datetime import timedelta
        
        data = {"sub": "test@example.com", "role": "user"}
        token = create_access_token(data=data, expires_delta=timedelta(hours=1))
        
        # Verify token
        payload = verify_token(token)
        assert payload["sub"] == "test@example.com"
        assert payload["role"] == "user"
        assert "exp" in payload
    
    def test_token_with_special_characters(self):
        """Test token creation with special characters in data."""
        data = {"sub": "user@domain.com", "name": "John Doe", "role": "admin"}
        token = create_access_token(data=data)
        
        payload = verify_token(token)
        assert payload["sub"] == "user@domain.com"
        assert payload["name"] == "John Doe"
        assert payload["role"] == "admin"
