#!/bin/bash
echo "========================================="
echo "   TALENTSCOUT CHATBOT MONITOR"
echo "   $(date)"
echo "========================================="

# Service status
SERVICE_STATUS=$(sudo systemctl is-active talentscout.service)
if [ "$SERVICE_STATUS" = "active" ]; then
    echo "✅ Service: ACTIVE"
else
    echo "❌ Service: $SERVICE_STATUS"
fi

# Port check
if nc -z localhost 8501 2>/dev/null; then
    echo "✅ Port 8501: OPEN"
else
    echo "❌ Port 8501: CLOSED"
fi

# API key status
if [ -f .env ]; then
    API_KEY=$(grep OPENAI_API_KEY .env | cut -d= -f2)
    if [ -n "$API_KEY" ]; then
        echo "✅ API Key: CONFIGURED"
    else
        echo "⚠️  API Key: NOT SET (using fallback)"
    fi
else
    echo "❌ .env file: MISSING"
fi

# Logs
echo -e "\n=== RECENT LOGS ==="
tail -5 chatbot.log 2>/dev/null || echo "No logs found"

# URLs
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com 2>/dev/null || echo "13.203.206.156")
echo -e "\n=== ACCESS URLS ==="
echo "Local:    http://localhost:8501"
echo "Public:   http://${PUBLIC_IP}:8501"
echo "Demo:     http://13.203.206.156:8501"

echo -e "\n=== QUICK COMMANDS ==="
echo "View logs:    tail -f chatbot.log"
echo "Restart:      sudo systemctl restart talentscout.service"
echo "Stop:         sudo systemctl stop talentscout.service"
echo "Test API:     python test_openai.py"
echo "========================================="
