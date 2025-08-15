# API Documentation 📚

## Base URL
```
http://localhost:8000
```

## Authentication 🔐

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### 1. Authentication

#### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Login User
```http
POST /auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "is_active": true
  }
}
```

#### Refresh Token
```http
POST /auth/refresh
```

**Headers:**
```
Authorization: Bearer <refresh-token>
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### 2. Search

#### Perform Web Search
```http
POST /search/
```

**Headers:**
```
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "query": "What is quantum computing?"
}
```

**Response:**
```json
{
  "success": true,
  "query": "What is quantum computing?",
  "results": [
    {
      "title": "Quantum Computing Explained",
      "url": "https://example.com/quantum-computing",
      "summary": "Quantum computing is a type of computation...",
      "content": "Detailed content about quantum computing..."
    }
  ],
  "summary": "Quantum computing uses quantum mechanics...",
  "timestamp": "2024-01-15T10:30:00Z",
  "source": "tavily_api"
}
```

### 3. Image Generation

#### Generate Image
```http
POST /image/generate
```

**Headers:**
```
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "prompt": "An astronaut riding a unicorn on Mars"
}
```

**Response:**
```json
{
  "prompt": "An astronaut riding a unicorn on Mars",
  "image_url": "https://example.com/generated-image.jpg",
  "timestamp": "2024-01-15T10:30:00Z",
  "saved_item_id": 123
}
```

### 4. Dashboard

#### Get User History
```http
GET /dashboard/history
```

**Headers:**
```
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `type_filter` (optional): "search" or "image"
- `date_from` (optional): YYYY-MM-DD
- `date_to` (optional): YYYY-MM-DD
- `keyword` (optional): Search in prompt or title
- `include_hidden` (optional): true/false

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "type": "search",
    "prompt": "What is quantum computing?",
    "result_title": "Quantum Computing Explained",
    "result_summary": "Quantum computing uses quantum mechanics...",
    "result_url": "https://example.com/quantum-computing",
    "extra_data": {},
    "is_hidden": false,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

#### Get Dashboard Statistics
```http
GET /dashboard/stats
```

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "total_searches": 25,
  "total_images": 15,
  "recent_searches": 8,
  "recent_images": 5,
  "period_days": 30
}
```

#### Get Specific History Item
```http
GET /dashboard/history/{item_id}
```

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "type": "search",
  "prompt": "What is quantum computing?",
  "result_title": "Quantum Computing Explained",
  "result_summary": "Quantum computing uses quantum mechanics...",
  "result_url": "https://example.com/quantum-computing",
  "extra_data": {},
  "is_hidden": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Update History Item
```http
PUT /dashboard/history/{item_id}
```

**Headers:**
```
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "prompt": "Updated prompt text",
  "result_title": "Updated Title",
  "result_summary": "Updated summary text"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "type": "search",
  "prompt": "Updated prompt text",
  "result_title": "Updated Title",
  "result_summary": "Updated summary text",
  "result_url": "https://example.com/quantum-computing",
  "extra_data": {},
  "is_hidden": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

#### Delete History Item
```http
DELETE /dashboard/history/{item_id}
```

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "message": "History item deleted successfully"
}
```

#### Bulk Delete History
```http
DELETE /dashboard/history/bulk
```

**Headers:**
```
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "item_ids": [1, 2, 3]
}
```

**Response:**
```json
{
  "message": "3 history items deleted successfully"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. Consider implementing rate limiting for production use.

## CORS

CORS is configured to allow requests from:
- `http://localhost:3000` (Frontend development)
- `http://localhost:8000` (Backend)

## Testing

### Test Coverage
- **Unit Tests**: 52% coverage
- **Integration Tests**: API endpoint testing
- **E2E Tests**: Frontend-backend integration

### Run Tests
```bash
# All tests
pytest tests -v --cov=app --cov-report=term-missing

# Specific test categories
pytest tests/unit -v
pytest tests/integration -v
pytest tests/e2e -v --headed
```

## SDK Examples

### Python
```python
import httpx

async def search_web(query: str, token: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/search/",
            json={"query": query},
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.json()
```

### JavaScript
```javascript
const searchWeb = async (query, token) => {
  const response = await fetch('http://localhost:8000/search/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ query })
  });
  return response.json();
};
```

### cURL
```bash
# Search
curl -X POST "http://localhost:8000/search/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is quantum computing?"}'

# Generate Image
curl -X POST "http://localhost:8000/image/generate" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "An astronaut riding a unicorn on Mars"}'
```

## Support

For API support and questions:
- Check the interactive docs at `/docs`
- Review the test suite for usage examples
- Open an issue on GitHub
