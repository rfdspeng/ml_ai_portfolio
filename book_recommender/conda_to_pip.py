import re

def conda_to_pip(conda_file, pip_file):
    with open(conda_file, 'r') as f:
        lines = f.readlines()

    pip_packages = []
    for line in lines:
        if not line.startswith('#') and line.strip():
            parts = re.split(r'\s+', line)
            if len(parts) >= 2:
                package = parts[0]
                version = parts[1]
                pip_packages.append(f"{package}=={version}")
    
    with open(pip_file, 'w') as f:
        f.write('\n'.join(pip_packages))

    print(f"Converted pip requirements written to {pip_file}")

# Usage
conda_to_pip("requirements_conda.txt", "requirements.txt")