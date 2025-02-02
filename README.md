# Faqify

This project includes a feature that translates FAQ entries into multiple languages using Google Translate.

## Features

- Translate FAQ entries into multiple languages
- Supports various languages

## Installation

1. Clone the repository:
    ```bash
    git clone git@github.com:AtharvBhujbal/Faqify.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Faqify
    ```
3. Install the dependencies:
    1. Navigate to the backend directory:

        ```bash
        cd backend
        ```

    2. Create a virtual environment:

        ```bash
        python -m venv venv
        ```

    3. Activate the virtual environment:

        ```bash
        source venv/bin/activate
        ```

    4. Install backend dependencies:

        ```bash
        pip install -r requirements.txt
        ``` 

    5. Navigate to frontend:
        ```bash
        cd ../frontend
        ```
    6. Install frontend dependencies:
        ```bash
        npm install 
        ```

## Usage

1. Start backend application:

    **Follow along all commands in [backend/README.md](backend/README.md#setup-instructions) in ***Setup Instruction*** section.**

    Navigate to backend and after activating environment, run the following command.
    
    ```bash
    python3 run.py
    ```

2. Start frontend application:

    Navigate to frontend and run the following command.
    ```bash
    npm start
    ```

3. Open your browser and navigate to `http://localhost:3000`

## Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request for review.

## License

This project is licensed under the MIT License.
