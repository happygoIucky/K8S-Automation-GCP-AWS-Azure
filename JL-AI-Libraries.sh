python3 -m venv venv
source venv/bin/activate
pip install tensorflow==2.3.0 scikit-learn==0.22 torch==1.0.1
mkdir vulnerable-ollama && cd vulnerable-ollama
npm init -y
npm install ollama@v0.1.11
