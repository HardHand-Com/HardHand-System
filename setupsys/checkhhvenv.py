import os

# Zkontrolujte, zda virtuální prostředí 'hhsystem' existuje
if not os.path.isdir("../hhvenv"):
    print("Creating venv 'hhvenv'")
    os.system("cd .. && python3 -m venv hhvenv")
else:
    print("Venv exists")

#os.system("bash activatehhvenv.sh")
exit()