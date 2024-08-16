# Enhancing Educational Question Answering Systems Using Retrieval-Augmented Generation (RAG) of Subject-Related Materials

This project aims to enhance educational question answering systems by integrating Retrieval-Augmented Generation (RAG) techniques to provide more accurate and contextually relevant responses. The system leverages a Python backend for processing and generating answers and will feature a frontend for user interaction.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

Traditional question answering systems in education often struggle with providing contextually relevant answers. This project seeks to improve these systems by using Retrieval-Augmented Generation (RAG), which combines the retrieval of relevant documents with generative models to produce better answers.

## Features

- **RAG Integration**: Combines document retrieval with generation for improved answer quality.
- **Python Backend**: Built with a focus on scalability and efficiency.
- **Dependency Management**: Uses Poetry for managing dependencies.
- **Future Frontend**: A user-friendly interface for students and educators (to be designed).

## Project Structure

```plaintext
.
├── README.md
├── ed_rag
│   ├── README.md
│   ├── app.py
│   ├── celery_worker.py
│   ├── data
│   │   └── pdf files
│   ├── ed_rag
│   │   ├── __init__.py
│   │   ├── rag.py
│   │   ├── test.csv
│   │   ├── test.py
│   │   └── trainer.py
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── tests
│   │   ├── __init__.py
│   │   └── test.py
│   └── web
│       ├── __init__.py
│       ├── apis
│       │   ├── __init__.py
│       │   ├── chats.py
│       │   ├── db
│       │   │   ├── __init__.py
│       │   │   └── session.py
│       │   ├── healthcheck.py
│       │   ├── history.py
│       │   ├── tasks.py
│       │   └── upload.py
│       ├── core.py
│       └── models
│           ├── Chat.py
│           ├── __init__.py
├── ed_rag_fe
│   ├── README.md
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── logo192.png
│   │   ├── logo512.png
│   │   ├── manifest.json
│   │   └── robots.txt
│   └── src
│       ├── App.css
│       ├── App.js
│       ├── App.test.js
│       ├── Components
│       │   ├── ChatBoxComponent
│       │   │   ├── ChatBoxComponent.css
│       │   │   └── ChatBoxComponent.js
│       │   ├── ChatInterfaceComponent
│       │   │   ├── ChatInterfaceComponent.css
│       │   │   └── ChatInterfaceComponent.js
│       │   ├── Dock
│       │   │   └── DockComponent.js
│       │   ├── MainComponent
│       │   │   ├── MainComponent.css
│       │   │   └── MainComponent.js
│       │   └── SidebarComponent
│       │       ├── SidebarComponent.css
│       │       └── SidebarComponent.js
│       ├── app
│       │   ├── api.js
│       │   ├── features
│       │   │   ├── chatSlice.js
│       │   │   └── historySlice.js
│       │   └── store.js
│       ├── index.css
│       ├── index.js
│       ├── logo.svg
│       ├── reportWebVitals.js
│       ├── services
│       │   └── MessageService.js
│       └── setupTests.js
```

## Installation

To set up the project, ensure you have [Poetry](https://python-poetry.org/docs/#installation) installed. Then, follow these steps:

### Backend Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Durgnan/educational_rag_msc_project.git
    cd educational_rag_msc_project
    ```

2. **Navigate to the Backend Directory:**

    ```bash
    cd ed_rag
    ```

3. **Install dependencies:**

    ```bash
    poetry install
    ```

4. **Start Redis server:**

    ```bash
    redis-server
    ```

5. **Start Celery Worker:**

    ```bash
    celery -A web.apis.tasks worker --loglevel=info --pool=solo
    ```

6. **Activate the virtual environment:**

    ```bash
    poetry shell
    ```

7. **Start the Flask server:**

    ```bash
    flask run --port 8080
    ```

8. **RAG Initial Training:**

    Initially the RAG needs to be trained based on the Resources you want to add. This can be done from either Frontend or directly uploading files in data/ folder in ed_rag/data/ folder. The files needs to be in PDF as of now. once the files are copied in data folder. Follow these steps to run the trainer pipeline by giving the src in Trainer Object in main function. The Trainer object can either take a Folder or Specific files.

    ```python
    # Please disragard the db param
    rag = Trainer(r"../data/*", db="faiss_db_900") # For All files inside the folder.
    rag = Trainer(r"../data/dp-II-annotated.pdf", db="faiss_db_900")  # For a specific file inside the folder.
    ```

### Frontend Setup

1. **Navigate to the Frontend Directory:**

    ```bash
    cd ed_rag_fe
    ```

2. **Set up the `.env` file for the Backend Server:**

    Ensure the `.env` file in the frontend directory contains the correct backend server URL.

    Example `.env`:

    ```plaintext
    REACT_APP_BASE_URL=http://127.0.0.1:8080
    ```

3. **Install dependencies:**

    ```bash
    npm install
    ```

4. **Start the Frontend:**

    ```bash
    npm start
    ```

    The Frontend will be live on the first available port starting from 3000. For e.g. http://localhost:3000

## Usage

To use the system, first start both the backend and frontend services following the steps above. Then, interact with the system via the frontend interface to ask educational questions and receive contextually enhanced answers.

## Testing the RAG



## Future Work. 

This project is aimed to work more on implementing RAG related features like

1. Hybrid search
2. Reciprocal Rank fusion
3. Chunking best practices and 
4. Cross support for different type of files. 
5. Agentic RAG and Evaluation. 
6. STT TTS Implementation. 
7. MultiModel RAG.

## Contact

For any inquiries, please contact the project maintainer at [durgnan45@gmail.com](mailto:durgnan45@gmail.com).
