# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/signup?email=student@mergington.edu` | Unregister from an activity                                         |

## Testing

The project includes comprehensive tests for all API endpoints using pytest.

### Running Tests

1. Install test dependencies:

   ```
   pip install pytest
   ```

2. Run the test suite from the repository root:

   ```
   pytest tests/
   ```

3. Run tests with verbose output:

   ```
   pytest tests/ -v
   ```

### Test Coverage

The test suite includes 16 test cases covering:

- **GET /activities**: Response structure, status codes, activity data
- **POST /activities/{activity_name}/signup**: Successful signup, duplicate prevention, error handling
- **DELETE /activities/{activity_name}/signup**: Successful removal, error handling, state updates

All tests use isolated fixtures to ensure a clean state for each test run.

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
