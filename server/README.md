
## Overview

This project is a backend service built using FastAPI with a PostgreSQL database. It's designed to handle various operations, including comparisons between results, voting processes, and analysis related to specific data sets.

## Structure

- **Main**: The main entry point of the application is located in `main.py`.
- **Routers**: The application's functionality is divided into routers, each handling a different aspect of the application:
  - **Vergleich Router** (`src/routers/vergleich/vergleich_router.py`): Manages the comparison between results of 2018 and 2023.
  - **Voting Router** (`src/routers/voting/voting_router.py`): Handles voting operations, including token verification, and the processing of `erststimmzettel` and `zweitstimmzettel` to receive votes anonymously.
  - **Wahlkreis Router** (`src/routers/wahlkreis/wahlkreis_router.py`): Dedicated to analysis functions.

## Database

- **Models**: Located under `src/database/models`, the database models are defined using SQLAlchemy, Alembic facilitates interaction with the PostgreSQL database.
- **Scripts**:
  - **Generation Scripts** (`src/database/scripts/generation`): Scripts to populate the database.
  - **Analysis Scripts** (`src/database/scripts/analysis`): Scripts to perform data analysis operations.

