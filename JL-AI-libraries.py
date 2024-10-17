import subprocess

# List of libraries with specific vulnerable versions to check for vulnerabilities
vulnerable_libraries = [
    'transformers==4.11.0',  # Example vulnerable version for transformers
    'torch==1.7.0',          # Example vulnerable version for PyTorch
    'tensorflow==2.3.0',     # Example vulnerable version for TensorFlow
    'gemma==0.1.0'           # Hypothetical vulnerable version for Gemma (assuming it exists)
]

def check_vulnerabilities_with_pip_audit():
    print("Checking vulnerabilities with pip-audit...")
    try:
        subprocess.run(['pip-audit'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while auditing libraries with pip-audit: {e}")

def check_vulnerabilities_with_safety():
    print("Checking vulnerabilities with safety...")
    try:
        subprocess.run(['safety', 'check'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while auditing libraries with safety: {e}")

def install_libraries():
    for library in vulnerable_libraries:
        print(f"Installing {library}...")
        subprocess.run(['pip', 'install', library], check=True)

if __name__ == "__main__":
    install_libraries()
    check_vulnerabilities_with_pip_audit()  # Check with pip-audit
    check_vulnerabilities_with_safety()     # Check with safety
