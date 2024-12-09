# RMM Client
This project is a simplified Remote Monitoring and Management (RMM) system, designed to monitor and manage client machines remotely. It consists of two main components:

**Desktop Application**: A Tkinter-based client-side application that reports machine status and manages logs locally.


## Features

### Desktop Application
- **Machine Status Reporting**:
  - Display the current machine status.
  - Send status updates to the server.
- **Command Execution**:
  - Receive and execute remote commands.
- **Log Management**:
  - Store logs locally using Peewee ORM and sync with the server.


### Project Structure

desktop_app/
├── app.py               # Main Tkinter application
├── api_integration.py   # Handles API communication
├── models.py            # Peewee ORM models
└── requirements.txt     # Dependencies


### Prerequisites

Ensure the following is installed on your system:

- **Python** (version 3.10 or higher)

### Clone the project & Go to the project directory

```bash
git clone https://github.com/suriya-mca/rmm_client.git
cd rmm_client
```

### Create .env file

```bash
API_KEY=api_key
```

### Create virtual environment and activate

```bash
python -m venv env
source venv/bin/activate
```

### Install the dependencies

```bash
pip install -r requirements.txt
```

### Run the app

```bash
python app.py
```


