#!/bin/bash

# Slow Day Network Analyzer - Setup Script
# Author: Christian Paul Cabrera
# This script automates the installation process

echo "═══════════════════════════════════════════"
echo "    Slow Day - Network Traffic Analyzer    "
echo "               Setup Script                "
echo "═══════════════════════════════════════════"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  Warning: This script should be run as root for full functionality"
    echo "   Some features require root privileges for packet capture"
    echo ""
fi

# Check Python version
echo "[1/5] Checking Python version..."
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ Python $PYTHON_VERSION found"
else
    echo "✗ Python 3 not found. Please install Python 3.8 or higher"
    exit 1
fi

# Check pip
echo ""
echo "[2/5] Checking pip..."
if command -v pip3 &>/dev/null; then
    echo "✓ pip3 found"
else
    echo "✗ pip3 not found. Installing pip..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update
        sudo apt-get install -y python3-pip
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        rm get-pip.py
    fi
fi

# Install dependencies
echo ""
echo "[3/5] Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Check for libpcap (required for scapy)
echo ""
echo "[4/5] Checking system dependencies..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if dpkg -l | grep -q libpcap; then
        echo "✓ libpcap found"
    else
        echo "⚠️  libpcap not found. Installing..."
        sudo apt-get install -y libpcap-dev
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    if brew list libpcap &>/dev/null; then
        echo "✓ libpcap found"
    else
        echo "⚠️  libpcap not found. Installing via Homebrew..."
        brew install libpcap
    fi
fi

# Create necessary directories
echo ""
echo "[5/5] Setting up project structure..."
mkdir -p templates
mkdir -p static
mkdir -p logs

echo "✓ Project structure created"

# Test database initialization
echo ""
echo "Testing database initialization..."
python3 -c "from analyzer import NetworkAnalyzer; NetworkAnalyzer(db_path='test.db')" 2>/dev/null
if [ -f "test.db" ]; then
    echo "✓ Database system working"
    rm test.db
else
    echo "⚠️  Database initialization had issues"
fi

echo ""
echo "═══════════════════════════════════════════"
echo "          Installation Complete!           "
echo "═══════════════════════════════════════════"
echo ""
echo "Quick Start:"
echo "  Command Line:  sudo python3 analyzer.py"
echo "  Web Interface: sudo python3 web_server.py"
echo ""
echo "Then open: http://127.0.0.1:5000"
echo ""
echo "⚠️  Important:"
echo "   - Run with sudo/root for packet capture"
echo "   - Only use on authorized networks"
echo "   - Read the LICENSE and README.md"
echo ""
echo "Happy analyzing! 🔍"
