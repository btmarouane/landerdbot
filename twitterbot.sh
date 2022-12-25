#!/bin/bash

# Check the number of arguments
if [ $# -ne 1 ]; then
    echo "Usage: $0 [start|stop|status]"
    exit 1
fi

# Get the command (start, stop, or status)
command=$1

# Check the command
if [ "$command" = "start" ]; then
    # Start the service
    sudo systemctl start twitterbot
elif [ "$command" = "stop" ]; then
    # Stop the service
    sudo systemctl stop twitterbot
elif [ "$command" = "status" ]; then
    # Check the status of the service
    sudo systemctl status twitterbot
else
    # Invalid command
    echo "Invalid command: $command"
    exit 1
fi