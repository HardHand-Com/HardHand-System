import os

def check_install(package_name):
    """Funkce pro kontrolu, zda je balíček nainstalován."""
    return os.system(f"dpkg -l {package_name} > /dev/null 2>&1") == 0

print("Checking if packages are installed")


# Kontrola, zda jsou balíčky nainstalovány
if not check_install("tur-repo"):
    print("Tur-repo is not installed. Installing...")
    os.system("pkg install tur-repo")
else:
    print("Tur-repo is already installed.")

if not check_install("rust"):
    print("Rust is not installed. Installing...")
    os.system("pkg install rust")
else:
    print("Rust is already installed.")

if not check_install("mongodb"):
    print("MongoDB is not installed. Installing...")
    os.system("pkg install mongodb")
else:
    print("MongoDB is already installed.")

print("All required packages are installed.")

# Nyní můžeme pokračovat v pokračování skriptu podle potřeby
exit()