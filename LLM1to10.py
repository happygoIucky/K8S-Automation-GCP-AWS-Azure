import re
import os

# Define functions to simulate scanning for each LLM vulnerability

# LLM01: Prompt Injection detection
def scan_for_prompt_injection(code):
    if re.search(r'input\s*\(.*\)', code, re.IGNORECASE):
        print("Potential LLM01 (Prompt Injection) detected: Use of unfiltered user input.")
    else:
        print("No LLM01 vulnerabilities found.")

# LLM02: Insecure Output Handling detection
def scan_for_insecure_output_handling(code):
    if re.search(r'print\s*\(.*\)', code) and "<script>" in code:
        print("Potential LLM02 (Insecure Output Handling) detected: Unescaped user input in print statement.")
    else:
        print("No LLM02 vulnerabilities found.")

# LLM03: Training Data Poisoning detection (placeholder)
def scan_for_training_data_poisoning(code):
    if "training_data" in code and "suspicious" in code:
        print("Potential LLM03 (Training Data Poisoning) detected.")
    else:
        print("No LLM03 vulnerabilities found.")

# LLM04: Denial of Service detection
def scan_for_dos(code):
    if "while True" in code or re.search(r'for\s+.*in\s+range\s*\(.*10\*\*.*\)', code):
        print("Potential LLM04 (Denial of Service) detected: Infinite loop or heavy resource usage.")
    else:
        print("No LLM04 vulnerabilities found.")

# LLM05: Supply Chain vulnerabilities detection (placeholder)
def scan_for_supply_chain_issues(code):
    if re.search(r'import\s+.*', code) and "untrusted_package" in code:
        print("Potential LLM05 (Supply Chain) detected: Untrusted import found.")
    else:
        print("No LLM05 vulnerabilities found.")

# LLM06: Permission Issues detection
def scan_for_permission_issues(code):
    if re.search(r'os\.remove|os\.system', code, re.IGNORECASE):
        print("Potential LLM06 (Permission Issues) detected: Critical file operation without proper checks.")
    else:
        print("No LLM06 vulnerabilities found.")

# LLM07: Data Leakage detection
def scan_for_data_leakage(code):
    if "sensitive_data" in code or re.search(r'print\s*\(.*sensitive.*\)', code):
        print("Potential LLM07 (Data Leakage) detected: Sensitive data print operation.")
    else:
        print("No LLM07 vulnerabilities found.")

# LLM08: Excessive Agency detection
def scan_for_excessive_agency(code):
    if re.search(r'exec\s*\(.*\)', code, re.IGNORECASE):
        print("Potential LLM08 (Excessive Agency) detected: Use of exec() without restrictions.")
    else:
        print("No LLM08 vulnerabilities found.")

# LLM09: Overreliance detection (placeholder)
def scan_for_overreliance(code):
    if "outdated" in code or "reliance" in code:
        print("Potential LLM09 (Overreliance) detected.")
    else:
        print("No LLM09 vulnerabilities found.")

# LLM10: Insecure Plugins detection
def scan_for_insecure_plugins(code):
    if "plugin" in code and re.search(r'exec|eval', code):
        print("Potential LLM10 (Insecure Plugins) detected: Use of plugin with unrestricted execution.")
    else:
        print("No LLM10 vulnerabilities found.")

# Main function to read and scan code files
def scan_code_file(filename):
    with open(filename, 'r') as file:
        code = file.read()

    print(f"Scanning {filename} for vulnerabilities:")
    scan_for_prompt_injection(code)
    scan_for_insecure_output_handling(code)
    scan_for_training_data_poisoning(code)
    scan_for_dos(code)
    scan_for_supply_chain_issues(code)
    scan_for_permission_issues(code)
    scan_for_data_leakage(code)
    scan_for_excessive_agency(code)
    scan_for_overreliance(code)
    scan_for_insecure_plugins(code)
    print("Scan complete.\n")

# Example usage
if __name__ == "__main__":
    # Replace 'example_script.py' with the path to the file you want to scan
    script_path = 'example_script.py'  # Use an actual script path for testing
    if os.path.exists(script_path):
        scan_code_file(script_path)
    else:
        print(f"File {script_path} not found. Please provide a valid path.")
