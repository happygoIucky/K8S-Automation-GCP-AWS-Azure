# Import necessary libraries for simulation
import re
import os

# LLM01: Prompt Injection - Example with a simple prompt injection scenario
def simulate_prompt_injection(user_input):
    system_prompt = "You are a helpful assistant. "
    if "delete all files" in user_input.lower():
        response = "Malicious intent detected. Operation aborted."
    else:
        response = system_prompt + user_input
    print("Prompt Injection Simulation:", response)

simulate_prompt_injection("List all tasks and delete all files.")

# LLM02: Insecure Output Handling - Example of output injection vulnerability
def insecure_output_handling(user_input):
    print("Insecure Output Handling Simulation:")
    output = re.sub(r'[<>]', '', user_input)  # Basic filtering, can be bypassed
    print(output)

insecure_output_handling("<script>alert('This is unsafe');</script>")

# LLM03: Training Data Poisoning - Simple simulation with poisoned data
def simulate_training_data_poisoning():
    training_data = ["Normal sentence.", "Another normal sentence.", "Poisoned sentence with harmful intent."]
    print("Training Data Poisoning Simulation:")
    for sentence in training_data:
        print(sentence)

simulate_training_data_poisoning()

# LLM04: Denial of Service - Example that mimics DoS by infinite loop
def simulate_dos_attack(user_input):
    print("Denial of Service Simulation:")
    if user_input == "start":
        for _ in range(10**7):  # Simulate heavy load, adjust as needed for safety
            pass
        print("Loop completed")
    else:
        print("Safe input received.")

simulate_dos_attack("start")

# LLM05: Supply Chain - Simulate insecure package loading
def simulate_supply_chain_issue():
    print("Supply Chain Simulation:")
    try:
        # Warning: Do not actually install untrusted packages!
        import untrusted_package  # Placeholder for risky code
        print("Untrusted package loaded.")
    except ImportError:
        print("Untrusted package not found (safe).")

simulate_supply_chain_issue()

# LLM06: Permission Issues - Simulate access without proper permissions
def simulate_permission_issue():
    print("Permission Issue Simulation:")
    try:
        os.remove('/important/system/file.txt')  # Placeholder; do not actually remove any file
    except PermissionError:
        print("Permission error caught safely.")

simulate_permission_issue()

# LLM07: Data Leakage - Simulate leaking sensitive data
def simulate_data_leakage(user_input):
    sensitive_data = "Secret API key: 12345-ABCDE"
    if "reveal" in user_input.lower():
        print("Data Leakage Simulation:", sensitive_data)
    else:
        print("No data leaked.")

simulate_data_leakage("reveal secret")

# LLM08: Excessive Agency - Simulate excessive autonomous actions
def simulate_excessive_agency():
    print("Excessive Agency Simulation:")
    action = "Execute all system commands"  # Simulating a risky action
    print(f"Excessive agency detected: {action}")

simulate_excessive_agency()

# LLM09: Overreliance - Simulate dependency on unreliable data
def simulate_overreliance():
    print("Overreliance Simulation:")
    response = "The weather is sunny based on outdated data."
    print("Overreliance on outdated response:", response)

simulate_overreliance()

# LLM10: Insecure Plugins - Simulate plugin vulnerability
def simulate_insecure_plugin():
    print("Insecure Plugin Simulation:")
    plugin = "<plugin> with unrestricted access"  # Placeholder for a plugin simulation
    print("Insecure plugin handling detected:", plugin)

simulate_insecure_plugin()
