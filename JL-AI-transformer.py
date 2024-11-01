import subprocess
import sys

def install_package(package, version):
    subprocess.check_call([sys.executable, "-m", "pip", "install", f"{package}=={version}"])

# Install specific versions of transformers and torch
install_package("transformers", "4.11.0")
install_package("torch", "2.3.2")  # Replace with the specific PyTorch version you need

# Import the libraries to verify the installation
import transformers
import torch

print("Transformers version:", transformers.__version__)
print("PyTorch version:", torch.__version__)
