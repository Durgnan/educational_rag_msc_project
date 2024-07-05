# Enhancing Educational Question Answering Systems Using Retrieval-Augmented Generation (RAG) of Subject Related Materials

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

Traditional question answering systems in education often struggle with providing contextually relevant answers. This project seeks to improve these systems by using Retrieval-Augmented Generation (RAG), which combines retrieval of relevant documents with generative models to produce better answers.

## Features

- **RAG Integration**: Combines document retrieval with generation for improved answer quality.
- **Python Backend**: Built with a focus on scalability and efficiency.
- **Dependency Management**: Uses Poetry for managing dependencies.
- **Future Frontend**: A user-friendly interface for students and educators (to be designed).

## Project Structure

.
├── ed_rag (backend)
│ ├── data
│ ├── ed_rag
│ │ ├── init.py
│ ├── tests
│ │ ├── init.py
│ │ └── test_main.py
│ ├── poetry.lock
│ └── pyproject.toml
├── ed_rag_fe
│ ├── index.js
└── README.md
└── .gitignore



## Installation

To set up the project, ensure you have [Poetry](https://python-poetry.org/docs/#installation) installed. Then, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/Durgnan/educational_rag_msc_project.git
    cd educational_rag_msc_project
    ```

2. Install dependencies:
    ```bash
    poetry install
    ```

3. Activate the virtual environment:
    ```bash
    poetry shell
    ```

## Usage

To run the backend server, use the following command:

```bash
poetry run python backend/app/main.py
