#!/bin/bash
set -e

echo "WEB-LANG-DET | Creating virtual Python environment..."
python3 -m venv venv
source venv/bin/activate
echo "WEB-LANG-DET | Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -e .

echo "WEB-LANG-DET | Installation complete"
echo "WEB-LANG-DET | To use, activate the virtual environment with 'source venv/bin/activate', and run 'web-lang' help for list of commands."
