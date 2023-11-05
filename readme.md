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
real-time-vehicle-tracking
│
├── backend/                      # Backend API
│   ├── __init__.py               # Initialization of backend package
│   ├── auth/
│   │   └── routes.py             # Authentication routes
│   ├── config.py                 # Configuration settings
│   ├── models.py                 # Database models
│   ├── station/
│   │   ├── __init__.py           # Initialization of station package
│   │   └── routes.py             # Station-related routes
│   ├── user/
│   │   ├── __init__.py           # Initialization of user package
│   │   └── routes.py             # User-related routes
│   └── vehicle/
│       ├── __init__.py           # Initialization of vehicle package
│       └── routes.py             # Vehicle-related routes
│
├── backend_api_usage_tutorial.ipynb  # Jupyter notebook for backend API usage tutorial
├── readme.md                         # README for the repository
└── requirements.txt                  # Required packages
```