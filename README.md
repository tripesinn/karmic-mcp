# Karmic Lite MCP Server (English Documentation)

## 🚀 Overview
The Karmic Lite MCP Server is a high-efficiency FastAPI microservice designed to serve Karmic Lite astrological and doctrinal data via the Model Context Protocol (MCP). It provides core endpoints for planetary transit calculations and specialized doctrine readings based on natal chart data.

## 🛠️ Prerequisites
*   Python 3.12+ (Recommended for optimal dependency compatibility)
*   `uvicorn` and `fastapi` (Dependencies listed in `requirements.txt`)
*   The core logic implementation (`karmic_lite.py`) must be available in the project root.

## ⚙️ Local Setup and Installation

1.  **Clone the repository** (if applicable).
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the server:**
    ```bash
    python server.py
    ```
    *The server will start on `http://0.0.0.0:8000`.*

## 🧪 Local Testing and Validation

Use the following commands to validate the API endpoints and confirm MCP schema compatibility.

### 1. Health Check
Check if the service is operational:
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/health
# Expected Output: 200
```

### 2. MCP Discovery Schema
Verify the service metadata required by the Edge Gallery:
```bash
curl -s http://localhost:8000/mcp/discovery | json_pp
# Expected Output: A JSON structure detailing available endpoints.
```

### 3. Test Planetary Transits (Example: Jero's Natal Data)
Use a valid date of birth (DOB) to test the transit endpoint. (Example DOB: `2026-06-20`).
```bash
curl -X GET "http://localhost:8000/transits/today?dob=2026-06-20" | json_pp
# Expected Output: A JSON object matching the TransitResponse schema.
# Example Structure: {"date": "2026-06-20", "planet_positions": {"sun": "Cancer", "moon": "Gemini"}}
```

### 4. Test Doctrine Reading
Test the doctrine reading endpoint with DOB and precise birth time.
```bash
curl -X POST "http://localhost:8000/doctrine/reading?dob=2026-06-20&birth_time=14:30" \
  -H "Content-Type: application/json" -d '{}' | json_pp
# Expected Output: A JSON object matching the DoctrineResponse schema.
# Example Structure: {"reading": "A doctrine reading for 2026-06-20 at 14:30. (Mocked content)", "input_details": {...}}
```

## 🌐 Edge Gallery Registration
Once local testing is complete, the service is ready for registration with the Edge Gallery. The `/mcp/discovery` endpoint provides all necessary schema information for automated setup. Follow the official Edge Gallery documentation for the registration process.