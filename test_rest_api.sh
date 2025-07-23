#!/bin/bash

# REST API Test Script for Image Background Remover
# This script tests all the REST API endpoints

API_BASE="http://localhost:5000"
TEST_IMAGE="goal.png"  # Using the existing image in the workspace

echo "🧪 Testing Image Background Remover REST API"
echo "============================================="
echo "📡 API Base URL: $API_BASE"
echo ""

# Test 1: API Information
echo "1️⃣  Testing API Information (GET /)"
echo "-----------------------------------"
curl -s -X GET "$API_BASE/" | jq . 2>/dev/null || curl -s -X GET "$API_BASE/"
echo -e "\n"

# Test 2: Health Check
echo "2️⃣  Testing Health Check (GET /health)"
echo "--------------------------------------"
curl -s -X GET "$API_BASE/health" | jq . 2>/dev/null || curl -s -X GET "$API_BASE/health"
echo -e "\n"

# Test 3: API Status
echo "3️⃣  Testing API Status (GET /api/status)"
echo "----------------------------------------"
curl -s -X GET "$API_BASE/api/status" | jq . 2>/dev/null || curl -s -X GET "$API_BASE/api/status"
echo -e "\n"

# Test 4: Remove Background
echo "4️⃣  Testing Background Removal (POST /api/remove-background)"
echo "------------------------------------------------------------"
if [ -f "$TEST_IMAGE" ]; then
    echo "📎 Uploading image: $TEST_IMAGE"
    echo "⏳ Processing... (this may take a moment on first run)"
    
    # Make the API call and save response
    RESPONSE=$(curl -s -X POST -F "image=@$TEST_IMAGE" "$API_BASE/api/remove-background")
    
    # Check if jq is available for pretty printing
    if command -v jq &> /dev/null; then
        echo "$RESPONSE" | jq .
        
        # Extract filename for download test
        FILENAME=$(echo "$RESPONSE" | jq -r '.data.filename // empty')
    else
        echo "$RESPONSE"
        
        # Extract filename without jq (basic grep)
        FILENAME=$(echo "$RESPONSE" | grep -o '"filename":"[^"]*"' | cut -d'"' -f4)
    fi
    
    echo ""
    
    # Test 5: Download File (if we got a filename)
    if [ ! -z "$FILENAME" ] && [ "$FILENAME" != "null" ]; then
        echo "5️⃣  Testing File Download (GET /api/download/$FILENAME)"
        echo "--------------------------------------------------------"
        
        # Test download endpoint
        HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE/api/download/$FILENAME")
        
        if [ "$HTTP_STATUS" = "200" ]; then
            echo "✅ Download successful (HTTP 200)"
            echo "📥 File available at: $API_BASE/api/download/$FILENAME"
            
            # Actually download the file
            curl -s -X GET "$API_BASE/api/download/$FILENAME" -o "downloaded_$FILENAME"
            if [ -f "downloaded_$FILENAME" ]; then
                echo "💾 File downloaded as: downloaded_$FILENAME"
                echo "📊 File size: $(du -h "downloaded_$FILENAME" | cut -f1)"
            fi
        else
            echo "❌ Download failed (HTTP $HTTP_STATUS)"
        fi
    else
        echo "5️⃣  Skipping download test (no filename received)"
    fi
else
    echo "❌ Test image '$TEST_IMAGE' not found!"
    echo "💡 Please ensure you have an image file to test with."
    echo ""
    echo "5️⃣  Testing Error Handling (POST /api/remove-background without file)"
    echo "---------------------------------------------------------------------"
    curl -s -X POST "$API_BASE/api/remove-background" | jq . 2>/dev/null || curl -s -X POST "$API_BASE/api/remove-background"
fi

echo -e "\n"

# Test 6: Invalid Endpoint
echo "6️⃣  Testing Invalid Endpoint (GET /invalid)"
echo "-------------------------------------------"
curl -s -X GET "$API_BASE/invalid" | jq . 2>/dev/null || curl -s -X GET "$API_BASE/invalid"
echo -e "\n"

# Summary
echo "✨ REST API Test Complete!"
echo "========================="
echo "🔍 Check the responses above to verify all endpoints are working"
echo "📝 For detailed API documentation, see API_DOCUMENTATION.md"
echo ""
echo "🚀 Quick curl examples:"
echo "  Health: curl $API_BASE/health"
echo "  Upload: curl -X POST -F \"image=@your_image.jpg\" $API_BASE/api/remove-background"
echo ""