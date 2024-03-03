import os

def check_python_packages():
    """Funkce pro kontrolu nainstalovaných Python balíčků ve virtuálním prostředí."""
    required_packages = ["flask", "time", "pymongo", "requests"]
    installed_packages = os.popen("pip list --format=columns").read()

    missing_packages = []
    for package in required_packages:
        if package not in installed_packages:
            missing_packages.append(package)

    return missing_packages

print("Checking if required Python packages are installed in venv 'hhphisher'")

# Kontrola nainstalovaných Python balíčků
missing_packages = check_python_packages()

if missing_packages:
    print("Some required Python packages are missing. Installing...")
    os.system("pip install " + " ".join(missing_packages))
else:
    print("All required Python packages are already installed.")

# Deaktivace virtuálního prostředí 'hhsystem'
os.system("bash deactivate.sh")
exit()