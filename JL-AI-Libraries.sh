# Bash script example to install all vulnerable versions
#!/bin/bash

# Create virtual environment for Python libraries
python3 -m venv venv
source venv/bin/activate

# Install vulnerable versions of TensorFlow, scikit-learn, and PyTorch
pip install tensorflow==2.3.0 scikit-learn==0.22 torch==1.0.1

# Initialize npm project for JavaScript
mkdir vulnerable-ollama && cd vulnerable-ollama
npm init -y
npm install ollama@v0.1.11
