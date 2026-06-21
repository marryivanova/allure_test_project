![Python](https://img.shields.io/badge/Language-Python-blue.svg)
![Pytest](https://img.shields.io/badge/Tests-Pytest-green.svg)
![Allure](https://img.shields.io/badge/Reports-Allure-orange.svg)

# 🚀 Allure Test Project: A Foundation for Robust API Testing

This project serves as a comprehensive template for API testing, designed to provide a solid foundation for building automated test suites. It includes example test cases for a user management service, showcasing a flexible architecture that supports detailed reporting with Allure and streamlines routine API request validation processes.

## Table of Contents

-   [Features](#features)
-   [Tech Stack](#tech-stack)
-   [Installation](#installation)
-   [Configuration](#configuration)
-   [Usage](#usage)
-   [Project Structure](#project-structure)
-   [Contributing](#contributing)
-   [License](#license)
-   [Author](#author)

## Features

✨ This project offers a robust set of features to streamline your API testing workflow:

-   **Allure Reporting Integration**: Automatically generates rich, interactive, and detailed test reports, making it easy to analyze test results, track defects, and understand test execution flow.
-   **Fixture-Based Test Setup**: Leverages Pytest fixtures for efficient and reusable test setup and teardown, managing authentication tokens, API clients, and test data.
-   **API Client Abstraction**: Provides a clear and modular way to interact with API endpoints using `httpx`, encapsulating request logic and enhancing test readability.
-   **Pydantic Data Models**: Utilizes Pydantic for robust request and response data validation, ensuring consistency and catching schema-related issues early.
-   **Environment Variable Management**: Seamlessly handles sensitive credentials and dynamic endpoint URLs through `.env` files and `pydantic-settings` for secure and flexible configuration.
-   **Parameterized & E2E Testing**: Includes examples of parameterized tests and end-to-end scenarios for comprehensive coverage of API functionality, from individual endpoints to complex user flows.

## Tech Stack

This project is built with the following technologies:

-   **Python**: The primary programming language used for writing test cases and the testing framework.
-   **Pytest**: A popular and powerful testing framework for Python, used for test discovery, execution, and fixture management.
-   **Allure Framework**: An open-source framework designed to create flexible and detailed test reports. `allure-pytest` integrates it with Pytest.
-   **Pydantic**: A data validation and settings management library, used for defining and validating API request/response models.
-   **Pydantic-Settings**: Extends Pydantic to manage application settings from various sources, including environment variables and `.env` files.
-   **python-dotenv**: Loads environment variables from a `.env` file into `os.environ`.
-   **HTTPX**: A fully featured HTTP client for Python, used for making asynchronous and synchronous API requests.

*Note: While this testing project is built using Python, it is designed to test APIs that could be implemented with various backend technologies, such as Express.js or FastAPI, as indicated in the project's broader context.*

## Installation

To get this project up and running locally, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/allure-test-project.git
    cd allure-test-project

    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv

    ```

3.  **Activate the virtual environment:**

    -   On macOS/Linux:
        ```bash
        source venv/bin/activate

        ```
    -   On Windows:
        ```bash
        .\venv\Scripts\activate

        ```

4.  **Install dependencies:**

    This project does not have a `requirements.txt` file detected, but the following dependencies are inferred from the codebase. You can create a `requirements.txt` or install them manually:

    ```bash
    pip install pytest allure-pytest httpx pydantic "pydantic-settings>=2.0" python-dotenv

    ```

## Configuration

This project relies on environment variables for sensitive data and dynamic settings.

1.  **Create a `.env` file:**

    In the root directory of the project (or one level above `tests/`), create a file named `.env`. This file will store your API base URLs and test user credentials.

2.  **Add environment variables:**

    Populate your `.env` file with the following (replace placeholders with your actual values):

    ```dotenv
    BASE_URL="http://localhost:8000"
    LOGIN_URL="http://localhost:8000/auth"

    # Test User Credentials

    TEST_USER_EMAIL="test@example.com"
    TEST_USER_PASSWORD="securepassword"

    ```

    These variables are loaded and used by `tests/settings.py`.

3.  **Pytest Configuration:**

    The `pytest.ini` file located in the `tests/` directory contains Pytest-specific configurations. You can modify it to adjust test discovery patterns, markers, or other Pytest settings.

    ```ini
    [pytest]
    # Example: add custom markers, specify test paths

    ```

## Usage

This section guides you on how to run the tests and generate Allure reports.

1.  **Ensure your virtual environment is active** (as described in [Installation](#installation)).

2.  **Run all tests:**

    To execute all tests and generate Allure results, use the following command:

    ```bash
    pytest --alluredir=allure-results

    ```

    This command will run all detected Pytest tests and output Allure XML files into the `allure-results/` directory.

3.  **View Allure Reports:**

    After running the tests, you can generate and serve the interactive Allure report:

    ```bash
    allure serve allure-results

    ```

    This will open a new browser window displaying the detailed Allure report, allowing you to navigate through test results, steps, and attachments.

4.  **Extending the Test Suite:**

    -   **Add new test files**: Create new `.py` files under `tests/test_endpoint/` or `tests/test_unit/` for your specific API endpoints or unit tests.
    -   **Define new models**: Use Pydantic in `tests/models/` to define schemas for your API requests and responses.
    -   **Create new API clients**: Extend `tests/base/api/client_api.py` or create new client classes for different services.
    -   **Add fixtures**: Define reusable test setup/teardown logic in `tests/fixtures/` or `conftest.py`.

## Project Structure

```
├── README.md
├── allure-report/                # Generated Allure HTML reports

├── allure-results/               # Raw Allure XML results from test runs

└── tests/
    ├── __init__.py
    ├── base/                     # Base classes and core API client logic

    │   └── api/                  # API client implementations (e.g., AuthenticationClient)

    ├── conftest.py               # Pytest configuration and global fixtures

    ├── fixtures/                 # Reusable test fixtures (e.g., for auth tokens, endpoint clients)

    │   ├── endpoint_client.py
    │   ├── helper_fixtures.py
    │   └── token_auth.py
    ├── models/                   # Pydantic data models for API requests/responses

    │   ├── auth.py
    │   ├── authentication.py
    │   └── users.py
    ├── pytest.ini                # Pytest configuration file

    ├── settings.py               # Project settings loaded from environment variables (.env)

    ├── test_endpoint/            # Integration and End-to-End tests for API endpoints

    │   ├── __init__.py
    │   ├── test_create_user.py   # Example test for user creation

    │   ├── test_e2e/             # End-to-end test scenarios

    │   ├── test_enpoint.py       # Example tests for various user API operations

    │   └── user_helpers.py       # Helper functions specific to user service tests

    ├── test_unit/                # Unit tests for internal utilities or schemas

    │   ├── __init__.py
    │   ├── _helpers_unit.py
    │   ├── test_logging.py
    │   ├── test_perser.py
    │   └── test_shemas.py
    └── utils/                    # Utility functions and common helpers

        ├── assertions/           # Custom assertion helpers

        ├── clients/              # HTTP client builders and wrappers

        ├── constants/            # Global constants (e.g., API routes)

        ├── fakers.py             # Data faker utilities for test data generation

        └── helpers.py            # General utility functions

```

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

All rights reserved.

## Author

-   Your Name / Organization Name
