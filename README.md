
# Project README

## Introduction

This document provides a comprehensive guide for setting up and launching the Bayern Election 2023 application. The application is divided into two main components: the server side, which handles the database and API, and the client side, which provides the user interface for voting. Follow these instructions to set up both components and generate voting tokens.

## Prerequisites

Before starting, ensure you have the following installed on your system:
- Docker and Docker Compose
- Python 3.8 or higher
- pip (Python package installer)
- Node.js and npm (Node Package Manager)

## Server Setup

### Step 1: Launch the Database

Navigate to the server directory and launch the database using Docker Compose.

```sh
cd server
docker-compose up
```

### Step 2: Install Server Dependencies

Install the required Python dependencies.

```sh
pip install .
```

### Step 3: Database Migration

Apply database migrations to ensure the database schema is up-to-date.

```sh
alembic upgrade head
```

### Step 4: Populate Database

Run the provided script to fill the database tables with initial data. You might need to set ``src`` as the source folder.

```sh
python src/database/scripts/generation/fill_tables.py
```

### Step 5: Run the Application

Start the server application with live reload enabled for development.

```sh
cd src
uvicorn main:app --reload
```

## Frontend Setup

### Step 1: Install Dependencies

Navigate to the client directory and install the necessary npm packages.

```sh
cd client
npm install --legacy-peer-deps
```

### Step 2: Start the Client Application

Launch the frontend application.

```sh
npm start
```

## Generating Tokens for Voting

### Step 1: Generate Voting Tokens

Generate tokens required for voting. Detailed instructions can be found within the script.

```sh
python server/src/stimmabgabe/generate_tokens.py
```

### Step 2: Vote

With the tokens generated, you can now proceed to vote through the frontend application.

