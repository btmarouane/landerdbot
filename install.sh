#!/bin/bash

DIR=$(pwd)
START_SCRIPT_PATH=${DIR}/start.sh

# Check if Python is installed
if ! which python3; then
  # Install Python if it is not installed
  apt-get install python3
fi


# Create a virtual environment
if test -d bot-venv; then
  echo "Virtual environment already exists, skipping creation"
else
  python3 -m venv bot-venv
fi

# Activate the virtual environment
source bot-venv/bin/activate

# Install the requirements
if pip freeze | grep -q -f Requirements.txt; then
  echo "Requirements are already installed, skipping installation"
else
  python3 -m pip install --upgrade pip
  python3 -m pip install -r Requirements.txt
fi

cat twitterbot_unit_file > /etc/systemd/system/twitterbot.service

chmod 644 /etc/systemd/system/twitterbot.service
cp twitterbot.sh /usr/local/bin/twitterbot
chmod +x /usr/local/bin/twitterbot
# Run the Python script
systemctl daemon-reload
twitterbot start
