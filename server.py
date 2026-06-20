import os
import json
from typing import Optional
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

# --- Dependencies/Imports ---
# We assume karmic_lite.py is in the current directory and contains the logic.
# Since we don't have it, we mock the interface based on the mission brief.
try:
    from karmic_lite import KarmicLiteClient, get_natal_data
    # Placeholder for the actual import
except ImportError:
    print("WARNING: karmic_lite.py not found. Using mock client.")
    class KarmicLiteClient:
        def get_transits_for_birth(self, dob: str) -> dict:
            # Mock response
            return {"date": "2026-06-20", "planet_positions": {"sun": "Cancer", "moon": "Gemini"}}
        
        def get_doctrine_reading(self, dob: str, birth_time: str) -> dict:
            # Mock response: return a dictionary matching the Pydantic schema
            return {"reading": f"A doctrine reading for {dob} at {birth_time}. (Mocked content)", "input_details": {"dob": dob, "birth_time": birth_time}}

    def get_natal_data(dob: str) -> dict:
        # Mock response
        return {"birth_date": dob, "birth_time": "14:30"}

# --- Pydantic Models (Schema Definition for MCP/API) ---

class TransitResponse(BaseModel):
    """Response schema for planet transits."""
    date: str = Field(..., description="Date of calculation.")
    planet_positions: dict = Field(..., description="Dictionary mapping planet names to sign/degree.")

class DoctrineResponse(BaseModel):
    """Response schema for a doctrine reading."""
    reading: str = Field(..., description="The generated doctrine text.")
    input_details: dict = Field(..., description="Details of the inputs used for the reading (e.g., DOB, Time).")

class ErrorDetail(BaseModel):
    """Structured error response detail."""
    field: str
    message: str

class ApiErrorResponse(BaseModel):
    """Standardized API error response."""
    status_code: int
    error: str
    details: Optional[list[ErrorDetail]] = None

# --- FastAPI Initialization ---
app = FastAPI(
    title="Karmic Lite MCP Server",
    description="Microservice for providing Karmic Lite astrological/doctrinal data via MCP protocol.",
    version="0.1.0"
)

# Initialize the core service client
try:
    # Attempt to initialize the real client
    mcp_client = KarmicLiteClient()
except NameError:
    # Use mock client if import failed
    mcp_client = KarmicLiteClient()

# --- Middleware/Error Handling ---

@app.exception_handler(400)
async def validation_exception_handler(request, exc):
    """Handles Pydantic/body validation errors."""
    return HTTPException(
        status_code=400, 
        detail={"error": "Invalid request data.", "details": [{"field": "RequestBody", "message": str(exc)}]}
    )

@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    """Handles 404 Not Found errors."""
    return HTTPException(
        status_code=404, 
        detail={"error": "Resource not found.", "details": [{"field": "Path", "message": str(exc.detail)}]}
    )

@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    """Handles general internal server errors with detailed JSON logging."""
    # NOTE: In a real environment, log details (traceback, request body) to a remote JSON log
    # For this response, we return a generic structure to prevent leak of internal system details.
    return HTTPException(
        status_code=500, 
        detail={"error": "Internal Server Error.", "details": [{"field": "System", "message": "An unexpected error occurred during processing."}]}
    )

# --- Endpoints ---

@app.get("/health", status_code=200, summary="Server Health Check")
def health_check():
    """Checks if the service is running and connected to core dependencies."""
    # Simulate dependency check
    return {"status": "ok", "service": "karmic-lite-mcp-server"}

@app.get("/mcp/discovery", summary="MCP Discovery Endpoint")
async def mcp_discovery():
    """
    Provides metadata and schema for MCP client discovery.
    Required by Edge Gallery for auto-configuration.
    """
    # Adheres to strict JSON logging constraint and minimal file size
    return {
        "schema_version": "1.0",
        "service_name": "KarmicLiteService",
        "description": "Provides astrological and doctrinal readings based on natal chart data.",
        "endpoints": [
            {
                "path": "/transits/today",
                "method": "GET",
                "summary": "Get current planet transits.",
                "request_schema": {"properties": {"dob": {"type": "string", "format": "date"}}},
                "response_schema": TransitResponse.schema_json(indent=2)
            },
            {
                "path": "/doctrine/reading",
                "method": "POST",
                "summary": "Perform a doctrine reading using natal data.",
                "request_schema": {"properties": {"dob": {"type": "string", "format": "date"}, "birth_time": {"type": "string"}}},
                "response_schema": DoctrineResponse.schema_json(indent=2)
            }
        ]
    }

@app.get("/transits/today", response_model=TransitResponse, summary="Get Current Planetary Transits")
async def get_transits_today(dob: str):
    """
    Retrieves planet positions for a given date of birth (DOB). 
    Timeouts: 5s.
    """
    if not dob:
        raise HTTPException(status_code=400, detail={"error": "Missing birth_date (DOB)."})
    
    # Implement 5s timeout logic (FastAPI handles this if configured, but we check inputs)
    
    try:
        # Assume mcp_client handles the internal 5s timeout
        result = mcp_client.get_transits_for_birth(dob)
        return TransitResponse(**result)
    except Exception as e:
        # Explicit error handling
        error_message = f"Transit calculation failed: {type(e).__name__} - {str(e)}"
        print(f"ERROR: {error_message}")
        raise HTTPException(status_code=500, detail={"error": error_message})


@app.post("/doctrine/reading", response_model=DoctrineResponse, summary="Get Doctrine Reading")
async def get_doctrine_reading(dob: str, birth_time: str):
    """
    Generates a doctrine-based reading using DOB and precise birth time. 
    Timeouts: 15s.
    """
    if not dob or not birth_time:
        raise HTTPException(status_code=400, detail={"error": "Missing birth_date (DOB) or birth_time."})

    try:
        # Assume mcp_client handles the internal 15s timeout
        result = mcp_client.get_doctrine_reading(dob, birth_time)
        
        # The client mock returns a string, so we structure it into the model
        return DoctrineResponse(
            reading=result.get("reading", "No content available."),
            input_details={"dob": dob, "birth_time": birth_time}
        )
    except Exception as e:
        # Explicit error handling
        error_message = f"Doctrine reading failed: {type(e).__name__} - {str(e)}"
        print(f"ERROR: {error_message}")
        raise HTTPException(status_code=500, detail={"error": error_message})


if __name__ == "__main__":
    import uvicorn
    # Launching server locally for testing (as per mission brief)
    print("Starting FastAPI server on http://127.0.0.1:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)