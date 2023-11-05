# Real Time Vehicle Tracking System

This is a simple real time vehicle tracking system that tracks the location of a vehicle and compute it's arrival time from a given station.

## API Usage Demo
Here is a demo of the API usage using Postman.

[API Usage Demo in IPYNB](https://github.com/Emeruem-Kennedy1/real-time-vehicle-tracking/blob/main/backend_api_usage_tutorial.ipynb)

## Technologies Used
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)


To see the folder structure of the project, click [here](#folder-structure).

## Features
- Sign up and login
- Create API Keys for Users
- Create a vehicle
- Create a station
- compute the arrival time of a vehicle from a given station

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

List any prerequisites, libraries, OS version, etc., needed before installing the project. For example:

- Python (v3.8 or later)

### Installing

#### Backend Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Emeruem-Kennedy1/real-time-vehicle-tracking
    ```

2. **create and activate a virtual environment:**
    
    ```bash
    python -m venv venv
    source venv/bin/activate
    ``` 



2. **Navigate to the backend directory:**

    ```bash
    cd backend
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```



#### Running the Backend

- In the main project directory, run the following command:

    ```bash
    python app.py
    ```

  This will start the backend server on `http://127.0.0.1:5000`.


## Folder Structure
```
Heirarchical-Todo-List-App
│
├── Backend/                  # Backend API developed with Flask
│   ├── __init__.py           # Initialization of the Flask app
│   ├── auth.py               # Authentication related operations
│   ├── list.py               # Handling todo list operations
│   ├── models.py             # Database models
│   ├── readme.md             # Backend specific documentation
│   ├── requirements.txt      # Dependencies for the backend
│   └── task.py               # Task management operations
│
├── frontend/                 # Frontend developed using React
│   ├── package-lock.json     # Locked versions of npm dependencies
│   ├── package.json          # NPM package configuration
│   ├── public/               # Public assets like HTML, logo, etc.
│   │   ├── index.html        # Entry HTML file
│   │   ├── logo.png          # App logo
│   │   └── manifest.json     # Web app manifest file
│   ├── src/                  # Source files for React components
│   │   ├── App.js            # Main React application component
│   │   ├── ListAppApiclient.js # API client for backend communication
│   │   ├── components/       # Reusable React components
│   │   ├── contexts/         # React contexts for state management
│   │   ├── hooks/            # Custom React hooks
│   │   ├── index.js          # Entry point for React app
│   │   ├── theme.js          # Theme configuration for the app
│   │   └── views/            # React components for different views/pages
│   └── ...
│
├── tests/                    # Tests for the application
│   ├── __init__.py           # Initialization for tests
│   ├── test_list.py          # Tests for list operations
│   └── test_task.py          # Tests for task operations
│
├── .env                      # Environment variables
├── main.py                   # Main entry point for the Flask application
└── README.md                 # General documentation for the entire project
```