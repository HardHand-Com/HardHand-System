#!/bin/bash

# Spustit MongoDB
echo "Starting MongoDB server..."
mongod &

sleep 5

# Venv for first server
echo "Starting venv for first server..."
source hhvenv/bin/activate

# First server
python3 hardhand/app.py &

sleep 1

deactivate

# Venv for second server
echo "Starting venv for second server..."
source hhphisher/bin/activate

# Second server
python3 phisher/app.py

sleep 1

deactivate