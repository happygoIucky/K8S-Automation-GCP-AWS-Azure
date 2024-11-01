import subprocess
import sys

def install_specific_transformers_version(version):
    subprocess.check_call([sys.executable, "-m", "pip", "install", f"transformers=={version}"])

# Install a specific version of transformers
install_specific_transformers_version("4.11.0")

# Import the transformers library after installation
import transformers
print(transformers.__version__)  # Verify the version
