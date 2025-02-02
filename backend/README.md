# Faqify Backend

Faqify is a simple yet powerful FAQ management system that allows you to create, retrieve, and manage frequently asked questions. This backend service is built using Python and Flask, with PostgreSQL as the database, and supports multilingual translation of FAQs.

---

## Table of Contents

- [Folder Structure](#folder-structure)
- [Setup Instructions](#setup-instructions)
  - [1. Install Dependencies](#1-install-dependencies)
  - [2. Set Environment Variables](#2-set-environment-variables)
  - [3. Create the Database](#3-create-the-database)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Language Codes](#language-codes)
- [Running Tests](#running-tests)
- [License](#license)

---

## Folder Structure

The project structure is organized as follows:

```bash
.
├── app
│   ├── __init__.py
│   ├── database.py
│   ├── log.py
│   ├── message.py
│   ├── multithreading.py
│   ├── redis.py
│   ├── routes.py
│   ├── templates
│   │   └── index.html
│   └── translate.py
├── tests
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_multithreading.py
│   ├── test_redis.py
│   ├── test_routes.py
│   └── test_translate.py
├── README.md
├── requirements.txt
├── run.py
├── setup_db.py
└── LICENSE
```

- **app/**: Contains the main application modules including routes, database operations, caching, translation, and multithreading.
- **tests/**: Contains unit and integration tests for various components of the backend.
- **run.py**: The entry point to start the Flask application.
- **setup_db.py**: A helper script for initializing the database.
- **requirements.txt**: Lists all the Python dependencies for the project.

---

## Setup Instructions


### 1. Install Dependencies

Create a virtual environment and install the required packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file inside the `app` directory (or in the project root if configured that way) and set your environment variables:

```bash
DB_USER="YOUR_DB_USER"
DB_PASS="YOUR_DB_PASS"
```

Replace `YOUR_DB_USER` and `YOUR_DB_PASS` with your PostgreSQL credentials.

### 3. Create the Database

Create a PostgreSQL database named `faqdb` by following these steps:

1. Open PostgreSQL:
   ```bash
   sudo -u postgres psql
   ```
2. Create the database:
   ```sql
   CREATE DATABASE faqdb;
   ```
3. Exit PostgreSQL:
   ```sql
   \q
   ```

Use the provided `setup_db.py` script after database creation to initialize the database:

- **Note:** You can always rerun the script to clean up the **database** as well as the **cache**.

```bash
python setup_db.py
```

---

## Usage

### Running the Application

Start the Flask application using:

```bash
python run.py
```

By default, the server will run on [http://localhost:5000](http://localhost:5000).

### API Endpoints

You can interact with the API endpoints using tools like [Postman](https://www.postman.com/) or `curl`. The base URL for the API is: `http://localhost:5000/api`

Here are the available endpoints:

1. **Welcome Endpoint**

   - **URL:** `GET /`
   - **Description:** Returns a welcome message or the index page.
   - **Example:**
     ```bash
     curl "http://localhost:5000/api/"
     ```

2. **Initialize Database**

   - **URL:** `POST /init-db`
   - **Description:** Initializes the database.
   - **Example:**
     ```bash
     curl -X POST "http://localhost:5000/api/init-db"
     ```

3. **Create FAQ**

   - **URL:** `POST /create-faq`
   - **Description:** Creates a new FAQ entry and returns its ID.
   - **Example:**
     ```bash
     curl -X POST "http://localhost:5000/api/create-faq" \
          -H "Content-Type: application/json" \
          -d '{"question": "What is Faqify?", "answer": "Faqify is a FAQ management system."}'
     ```

4. **Get Specific FAQ**

   - **URL:** `GET /faq/{id}`
   - **Description:** Retrieves a FAQ by its ID.
   - **Example:**
     ```bash
     curl "http://localhost:5000/api/faq/1"
     ```

5. **Get All FAQs**

   - **URL:** `GET /faqs/`
   - **Description:** Retrieves all FAQs.
   - **Example:**
     ```bash
     curl "http://localhost:5000/api/faqs/"
     ```

6. **Get FAQs in a Specific Language**

   - **URL:** `GET /faqs/?lang={LANG_CODE}`
   - **Description:** Retrieves all FAQs translated into the specified language.
   - **Example:**
     ```bash
     curl "http://localhost:5000/api/faqs/?lang=hi"
     ```

7. **Populate Dummy Data**

   - **URL:** `POST /dummy-data`
   - **Description:** Populates the database with dummy FAQ data.
   - **Example:**
     ```bash
     curl -X POST "http://localhost:5000/api/dummy-data"
     ```

### Language Codes

Faqify supports multiple Indian languages. The most popular language codes are:

- `en` — English
- `hi` — Hindi
- `kn` — Kannada
- `ta` — Tamil
- `te` — Telugu
- `bn` — Bengali
- `ml` — Malayalam
- `gu` — Gujarati
- `mr` — Marathi
- `pa` — Punjabi

When using the `/faqs/?lang={LANG_CODE}` endpoint, make sure to pass one of the supported language codes.

---

## Running Tests

Unit and integration tests are written using Pytest. To run the tests, execute the following command in the project root:

```bash
pytest
```

This command will run all tests located in the `tests` folder.

## Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request for review.

## License

This project is licensed under the terms of the [MIT License](LICENSE).