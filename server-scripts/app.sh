#!/bin/bash

# Function to start the Django app
start_app() {
    # Navigate to your Django project directory
    cd /home/ubuntu/frms-backend/

    # Start the Django app
    nohup python3.10 manage.py runserver 0.0.0.0:8000 &

    # Wait for a few seconds to allow the app to start
    sleep 5

    # Refresh Nginx configuration
    sudo service nginx reload

    echo "Django app started and Nginx refreshed."
}

# Function to stop the Django app
stop_app() {
    # Find the process ID (PID) of the running Django app
    pid=$(lsof -t -i:8000)

    # Check if the PID exists
    if [ -z "$pid" ]; then
        echo "No Django app is currently running on port 8000."
    else
        # Kill the Django app process
        kill $pid
        echo "Django app stopped."
    fi

    # Refresh Nginx configuration
    sudo service nginx reload
"app.sh" 47L, 1058B                                                                                             6,33          Top
#!/bin/bash

# Function to start the Django app
start_app() {
    # Navigate to your Django project directory
    cd /home/ubuntu/frms-backend/

    # Start the Django app
    nohup python3.10 manage.py runserver 0.0.0.0:8000 &

    # Wait for a few seconds to allow the app to start
    sleep 5

    # Refresh Nginx configuration
    sudo service nginx reload

    echo "Django app started and Nginx refreshed."
}

# Function to stop the Django app
stop_app() {
    # Find the process ID (PID) of the running Django app
    pid=$(lsof -t -i:8000)

    # Check if the PID exists
    if [ -z "$pid" ]; then
        echo "No Django app is currently running on port 8000."
    else
        # Kill the Django app process
        kill $pid
        echo "Django app stopped."
    fi

    # Refresh Nginx configuration
    sudo service nginx reload

    echo "Nginx refreshed."
}

# Check the command-line argument
if [ "$1" == "--start" ]; then
    start_app
elif [ "$1" == "--stop" ]; then
    stop_app
else
    echo "Invalid argument. Use --start or --stop."
fi
