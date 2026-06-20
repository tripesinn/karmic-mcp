#!/bin/bash
# test_client.sh
# Mission: Validate local MCP Server functionality
# Client: Jero (Solo Dev)

SERVER_URL="http://localhost:8000"

echo "=============================================="
echo "✨ 1. Starting Local API Validation Tests ✨"
echo "Server running at: $SERVER_URL"
echo "=============================================="

# --- Test 1: Health Check ---
echo -e "\n--- [TEST 1/3] Health Check (/health) ---"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$SERVER_URL/health")
if [[ "$HTTP_CODE" == "200" ]]; then
    echo "✅ PASS: Health check returned HTTP $HTTP_CODE."
else
    echo "❌ FAIL: Health check returned HTTP $HTTP_CODE. Server might not be running."
    exit 1
fi

# --- Test 2: Planetary Transits (/transits/today) ---
DOB="2026-06-20"
echo -e "\n--- [TEST 2/3] Transits Test (/transits/today?dob=$DOB) ---"
TRANSIT_RESPONSE=$(curl -s -X GET "$SERVER_URL/transits/today?dob=$DOB" | jq -r '.')

if [ $? -eq 0 ] && echo "$TRANSIT_RESPONSE" | jq -e '.date' > /dev/null; then
    TRANSIT_DATE=$(echo "$TRANSIT_RESPONSE" | jq -r '.date')
    TRANSIT_POSITIONS=$(echo "$TRANSIT_RESPONSE" | jq -r '.planet_positions')
    echo "✅ PASS: Transits endpoint returned structured data."
    echo "   -> Date: $TRANSIT_DATE, Positions: $TRANSIT_POSITIONS"
else
    echo "❌ FAIL: Transits endpoint failed or returned invalid JSON."
    echo "Raw response:"
    echo "$TRANSIT_RESPONSE"
    exit 1
fi

# --- Test 3: Doctrine Reading (/doctrine/reading) ---
DOB="2026-06-20"
BIRTH_TIME="14:30"
echo -e "\n--- [TEST 3/3] Doctrine Reading Test (/doctrine/reading) ---"
DOCTRINE_RESPONSE=$(curl -s -X POST "$SERVER_URL/doctrine/reading?dob=$DOB&birth_time=$BIRTH_TIME" \
  -H "Content-Type: application/json" -d '{}' | jq -r '.')

if [ $? -eq 0 ] && echo "$DOCTRINE_RESPONSE" | jq -e '.reading' > /dev/null; then
    DOCTRINE_READING=$(echo "$DOCTRINE_RESPONSE" | jq -r '.reading')
    echo "✅ PASS: Doctrine reading endpoint returned structured data."
    echo "   -> Reading snippet: ${DOCTRINE_READING:0:80}..."
else
    echo "❌ FAIL: Doctrine reading endpoint failed or returned invalid JSON."
    echo "Raw response:"
    echo "$DOCTRINE_RESPONSE"
    exit 1
fi

echo -e "\n=============================================="
echo "🚀 MISSION SUCCESS: Local API Validation Complete."
echo "=============================================="