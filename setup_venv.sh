#!/bin/bash

# Grab directory
current_dir=${PWD}
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# install pip
sudo apt install python3-pip

# install venv
sudo apt install python3-venv

# Create environment
python3 -m venv ${SCRIPT_DIR}

# Activate environment
source ${SCRIPT_DIR}/bin/activate

# Install requirements
pip install -r ./requirements.txt

# Deactivate environment
deactivate