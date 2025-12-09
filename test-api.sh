#!/bin/bash

# TSPRTG Tag Manager - API Test Script

BASE_URL="http://localhost:8000"

echo "🧪 TSPRTG Tag Manager API Tests"
echo "================================"
echo ""

# Test root endpoint
echo "1. Testing root endpoint..."
curl -s $BASE_URL/ | python3 -m json.tool
echo ""

# Test API info
echo "2. Testing API info endpoint..."
curl -s $BASE_URL/api | python3 -m json.tool
echo ""

# Create advertiser
echo "3. Creating test advertiser..."
ADVERTISER=$(curl -s -X POST $BASE_URL/api/advertisers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Company",
    "domains": ["example.com", "test.example.com"],
    "is_active": true
  }')
echo $ADVERTISER | python3 -m json.tool
ADVERTISER_ID=$(echo $ADVERTISER | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
CONTAINER_ID=$(echo $ADVERTISER | python3 -c "import sys, json; print(json.load(sys.stdin)['container_id'])")
echo ""

# List advertisers
echo "4. Listing all advertisers..."
curl -s $BASE_URL/api/advertisers | python3 -m json.tool
echo ""

# Get container code
echo "5. Getting container embed code..."
curl -s $BASE_URL/api/advertisers/$ADVERTISER_ID/code | python3 -m json.tool
echo ""

# Create global script
echo "6. Creating global script..."
curl -s -X POST $BASE_URL/api/scripts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Global Analytics",
    "script_type": "external",
    "content": "https://analytics.example.com/tracker.js",
    "is_enabled": true,
    "priority": 0,
    "is_async": true,
    "is_defer": false
  }' | python3 -m json.tool
echo ""

# Create advertiser-specific script
echo "7. Creating advertiser-specific script..."
curl -s -X POST $BASE_URL/api/advertisers/$ADVERTISER_ID/scripts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Custom Tracking",
    "script_type": "inline",
    "content": "console.log(\"Custom tracking for Test Company\");",
    "is_enabled": true,
    "priority": 1,
    "is_async": false,
    "is_defer": false
  }' | python3 -m json.tool
echo ""

# Test loader endpoint
echo "8. Testing container loader (with valid referer)..."
curl -s -H "Referer: http://example.com/" $BASE_URL/c/$CONTAINER_ID/l.js
echo ""
echo ""

# Test loader endpoint with invalid referer
echo "9. Testing container loader (with invalid referer)..."
curl -s -H "Referer: http://unauthorized.com/" $BASE_URL/c/$CONTAINER_ID/l.js
echo ""
echo ""

# Get health status
echo "10. Getting health status..."
curl -s $BASE_URL/api/health | python3 -m json.tool
echo ""

# Get container stats
echo "11. Getting container statistics..."
curl -s $BASE_URL/api/advertisers/$ADVERTISER_ID/stats | python3 -m json.tool
echo ""

# Get container logs
echo "12. Getting container logs..."
curl -s $BASE_URL/api/health/containers/$ADVERTISER_ID/logs | python3 -m json.tool | head -50
echo ""

echo "✅ All tests completed!"
