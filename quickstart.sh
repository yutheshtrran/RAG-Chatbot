#!/bin/bash

# RAG Chatbot Quick Start Script for Unix/Linux/Mac
# This script sets up and runs the entire project

echo ""
echo "=========================================="
echo "  RAG Chatbot - Quick Start"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "✓ Python and Node.js are installed"
echo ""

# Backend Setup
echo ""
echo "=========================================="
echo "  STEP 1: Backend Setup"
echo "=========================================="
echo ""

cd backend

echo "Installing Python dependencies..."
pip3 install -r app/requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

echo "Initializing backend..."
python3 init.py
if [ $? -ne 0 ]; then
    echo "WARNING: Initialization had issues, continuing anyway..."
fi

echo "✓ Backend initialized"
echo ""

# Frontend Setup
echo ""
echo "=========================================="
echo "  STEP 2: Frontend Setup"
echo "=========================================="
echo ""

cd ../frontend

echo "Installing Node.js dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Node packages"
    exit 1
fi

echo "✓ Node dependencies installed"
echo ""

# Create sample data
echo ""
echo "=========================================="
echo "  STEP 3: Creating Sample Data"
echo "=========================================="
echo ""

cd ../

echo "Creating sample patient data..."
python3 create_sample_data.py
if [ $? -ne 0 ]; then
    echo "WARNING: Failed to create sample data, continuing anyway..."
fi

echo "✓ Sample data created (optional)"
echo ""

# Summary
echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  python3 run.py"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open your browser to: http://127.0.0.1:5173"
echo ""
echo "API Endpoint: http://127.0.0.1:5000/api"
echo ""
echo "For detailed instructions, see SETUP_GUIDE.md and README.md"
echo ""
