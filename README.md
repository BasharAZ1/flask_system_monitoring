
# System Monitoring Dashboard

A Flask-based web application designed for monitoring the following system resources: disk space, memory utilization, CPU usage, and active processes. This application allows users to monitor the host machine locally using the `psutil` module or connect to a remote Linux kernel OS through SSH to retrieve system information using bash commands. 

## Features

- **Local and Remote Monitoring**: Monitor system resources both locally and on remote Linux systems via SSH.
- **Comprehensive Resource Details**: Track disk space, memory utilization, CPU usage, and active processes.
- **Real-Time Data Visualization**: View real-time data presented in tables and graphs for easy understanding.
- **Alerts for Irregular Values**: Highlight irregular values in red for quick identification of potential issues (irregular values threshold is set to a low value to display this feature).
- **Database Integration**: Stores monitoring data in a database using Flask SQLAlchemy for historical analysis.

## Technologies Used

- Python
- Flask
- Flask SQLAlchemy
- Paramiko (for SSH connections)
- Psutil (for local system monitoring)
- HTML/CSS for the frontend and AJAX for asynchronous functionalities

## Getting Started

### Installation

1. Clone the repository:
```bash
git clone git@github.com:BasharAZ1/flask_system_monitoring.git
```

2. Navigate to the cloned repository

3. Install dependencies from the requirements file (preferably using a fresh virtual environment):
* Creating new virtual environment:
```bash
python3 -m venv env
```
* Activate on Windows:
```bash
./env/Scripts/activate
```
* Activate on Linux/MacOS:
```bash
source env/bin/activate
```
* Install dependencies:
```bash
pip install -r requirements.txt
```

5. Initialize the database with Flask-Migrate:
```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

5. Run the application:
```bash
flask run
```

This will start the Flask server and the application will be accessible at `http://127.0.0.1:5000/`.

## Usage

After starting the application, navigate to your web browser and enter the local server address. The application's web interface will allow you to monitor system resources either locally or remotely by entering the SSH details of the remote Linux system.
