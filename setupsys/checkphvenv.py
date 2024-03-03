import os

# Zkontrolujte, zda virtuální prostředí 'hhsystem' existuje
if not os.path.isdir("../hhphisher"):
    print("Creating venv 'hhphisher'")
    os.system("cd .. && python3 -m venv hhphisher")
else:
    print("Venv exists")

#os.system("bash activatephvenv.sh")
exit()