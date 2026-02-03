#!/bin/bash

echo "================================================"
echo "  APS NATURALS CHATBOT - WEB UI LAUNCHER"
echo "================================================"
echo ""
echo "Checking if model is trained..."

if [ ! -f "qa_model.h5" ]; then
    echo "Model not found! Training now..."
    python3 train.py
    if [ $? -ne 0 ]; then
        echo ""
        echo "Training failed! Please check the errors above."
        exit 1
    fi
    echo ""
fi

echo "Starting web server..."
echo ""
echo "================================================"
echo "  Open browser at http://localhost:5000"
echo "================================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Try to open browser (works on macOS and Linux)
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:5000 &
elif command -v open > /dev/null; then
    open http://localhost:5000 &
fi

python3 app.py
