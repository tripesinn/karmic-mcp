# Live Endpoint Verification (2026-06-20)

Captured from `http://34.163.125.49:8000` (live GCP e2-small instance, europe-west9-a).

## `/health` — Health check
```json
{"status":"ok","service":"karmic-lite-mcp-server"}
```

## `/mcp/discovery` — Schema (excerpt)
```json
{
  "schema_version": "1.0",
  "service_name": "KarmicLiteService",
  "endpoints_count": 2,
  "endpoints": [
    {
      "path": "/transits/today",
      "method": "GET"
    },
    {
      "path": "/doctrine/reading",
      "method": "POST"
    }
  ]
}
```

## `/transits/today?dob=1990-05-15` — Transit example
```json
{"date":"2026-06-20","planet_positions":{"sun":"Cancer","moon":"Gemini"}}
```

## Latency test (`/health` x3)
```
  request 1: HTTP 200 in 0.034722s
  request 2: HTTP 200 in 0.038031s
  request 3: HTTP 200 in 0.036188s
```
