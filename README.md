# Article Scraper

A FastAPI application designed to scrape articles from various web sources and store them in a database. This project provides a RESTful API for managing sources and articles.

## Features

-   **RESTful API**: Endpoints for creating, reading, and managing sources and articles.
-   **Web Scraping**: A dedicated service to fetch article content from URLs.
-   **Database Integration**: Uses SQLAlchemy ORM to interact with a SQLite database.
-   **Automatic API Docs**: Interactive API documentation provided by Swagger UI and ReDoc.

## Project Structure
```
└── app/
    ├── api/
    │ ├── articles.py
    │ └── sources.py
    ├── models/ 
    │ ├── article.py 
    │ └── source.py 
    ├── schemas/ 
    │ ├── article.py 
    │ └── source.py 
    ├── services/ 
    │ └── scraper.py 
    ├── crud.py 
    ├── database.py 
    ├── dependencies.py 
    └── main.py
```
## Requirements

-   Python 3.11+
-   pip

## Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/Torba2207/Article_Scraper.git
    cd Article_Scraper
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # On Windows
    python -m venv .venv
    .venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    (Ensure you have a `requirements.txt` file in your project root)
    ```sh
    pip install -r requirements.txt
    ```

4.  **Running the Application Locally:**
    To start the development server, run the following command from the project's root directory:
    ```sh
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

---

## Running with Docker (Recommended)

This is the recommended way to run the application for a consistent and isolated environment.

### Requirements

-   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

### Steps

1.  **Build the Docker image:**
    From the project's root directory (where the `Dockerfile` is located), run the build command. This may take a few minutes as it will download Python, Google Chrome, and all dependencies.
    ```sh
    docker build -t scraper-api .
    ```
    * `-t scraper-api` tags the image with a convenient name.

2.  **Run the Docker container:**
    Once the image is built, start a container from it:
    ```sh
    docker run --rm -p 8001:8000 scraper-api
    ```
    * `-p 8001:8000` maps port `8001` on your local machine to port `8000` inside the container.
    * `--rm` automatically removes the container when it's stopped.

3.  **Access the application:**
    The application is now running inside the Docker container. You can access it in your browser:
    -   **API Docs (Swagger):** `http://localhost:8001/docs`
    -   **API Docs (ReDoc):** `http://localhost:8001/redoc