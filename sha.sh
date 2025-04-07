#!/bin/bash
# Path to Python in your virtual environment
PYTHON="./.venv/Scripts/python"

"$PYTHON" -m ectf25.utils.flash ./decoder/build_out/max78000.bin COM3 
"$PYTHON" -m ectf25.tv.list COM3 
"$PYTHON" -m ectf25.tv.subscribe subscription.bin COM3                
"$PYTHON" -m ectf25.utils.tester --port COM3 -s secrets/secrets.json rand -c 1 -f 64