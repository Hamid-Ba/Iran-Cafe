#!/bin/bash

# Update requirements.txt from requirements.ini

echo "🔄 Recompiling requirements..."

# Install pip-tools if not available
pip install pip-tools

# Compile requirements.ini to requirements.txt
pip-compile requirements.ini

echo "✅ Requirements updated!"
echo "📋 Next step: rebuild Docker image with ./deploy.sh"