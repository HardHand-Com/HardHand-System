#!/bin/bash

# Spustit skript checkhhvenv.py
cd setupsys
python install.py
sleep 5
python checkhhvenv.py
python checkphvenv.py
sleep 5
cd ..
source hhvenv/bin/activate && pip install flask flask_sqlalchemy flask_bcrypt pymongo flask_login requests && deactivate
#sleep 1
#source hhvenv/bin/activate && pip install bson && deactivate
sleep 3
source hhphisher/bin/activate && pip install flask pymongo requests && deactivate
rm -r setupsys
echo "Done, run start.sh"
# flask bson flask_sqlalchemy flask_bcrypt flask_login pymongo requests