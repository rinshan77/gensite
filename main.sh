#!/bin/bash

# Run the Python script
python3 src/main.py

# Start the web server
cd public && python3 -m http.server 8888
