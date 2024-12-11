# Navigate-LA-28 Project

**Group Name:** Navigate-LA-28  
**Group Number:** 4  

## Group Members

| Name            | Email                       | Student ID  |
|------------------|-----------------------------|-------------|
| Aditya Gambhir   | agambhir001@ucr.edu        | 123456789   |
| Faizaan Muzawar  | member2@example.com        | 987654321   |
| Ajit Singh       | member3@example.com        | 456789123   |
| Samara Miramontes| member3@example.com        | 456789123   |
---

## Table of Contents

- [Navigate-LA-28 Project](#navigate-la-28-project)
  - [Group Members](#group-members)
  - [| Samara Miramontes| member3@example.com        | 456789123   |](#-samara-miramontes-member3examplecom---------456789123---)
  - [Table of Contents](#table-of-contents)
  - [Project Title and Overview](#project-title-and-overview)
  - [Author Contributions](#author-contributions)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Installation and Setup](#installation-and-setup)
    - [Environment Configuration](#environment-configuration)
  - [Environment Variables](#environment-variables)
    - [Backend Environment Variables](#backend-environment-variables)
  - [Running the Project](#running-the-project)
  - [Populating the Database](#populating-the-database)
  - [Development Workflow](#development-workflow)
  - [Testing and Debugging](#testing-and-debugging)
  - [Conclusion](#conclusion)
  - [Contact Information](#contact-information)

---

## Project Title and Overview

**Project Title:** Navigate-LA-28  
**Objective:** A Big Data Management project using geospatial data to help tourists navigate LA. The project includes a React frontend, FastAPI backend, and Hadoop/Spark for data processing.

---

## Author Contributions

| Group Member      | Contribution                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| Aditya Gambhir    | Set up the backend (FastAPI), implemented database schema, created endpoints. |
| Member 2 Name     | Developed the frontend using React, integrated Redux for state management.  |
| Member 3 Name     | Configured Docker, implemented Hadoop and Spark integration.               |

---

## Project Structure

```plaintext
Navigate-LA-28/
├── client/                             # React frontend
│   ├── node_modules/                   # Node.js packages
│   ├── public/                         # Public assets for the frontend
│   ├── src/                            # React source code
│   │   ├── assets/                     # Static assets
│   │   ├── components/                 # Reusable UI components
│   │   ├── constants/                  # Application constants
│   │   ├── hooks/                      # Custom React hooks
│   │   ├── services/                   # API and data-fetching utilities
│   │   ├── slices/                     # Redux slices for state management
│   │   ├── styles/                     # CSS files
│   │   ├── utils/                      # Utility functions
│   │   ├── App.js                      # Main React application file
│   │   ├── index.js                    # React app entry point
│   ├── .env.example                    # Example environment variables
│   ├── package.json                    # Node.js dependencies
│
├── server/                             # FastAPI backend
│   ├── config/                         # Configuration files
│   ├── models/                         # Database models
│   ├── routes/                         # API routes
│   ├── schemas/                        # Pydantic schemas
│   ├── tests/                          # Unit tests
│   ├── Dockerfile                      # Docker setup for backend
│   ├── main.py                         # Entry point for FastAPI
│   ├── requirements.txt                # Python dependencies
│
├── hadoop/                             # Hadoop configuration
│   ├── conf/                           # Configuration files
│
├── spark/                              # Spark configuration
│   ├── conf/                           # Configuration files
│
├── docker-compose.yml                  # Docker Compose configuration
└── README.md                           # Project documentation
```

## Prerequisites

Ensure the following software is installed on your machine:

1. **Docker**  
   [Download Docker Desktop](https://www.docker.com/products/docker-desktop) – Used to manage containers for the frontend, backend, Hadoop, Spark, and PostgreSQL.

2. **Node.js and npm**  
   [Download Node.js](https://nodejs.org/) – Required to run the React frontend. npm comes bundled with Node.js.

3. **Python 3.10+**  
   [Download Python](https://www.python.org/downloads/) – Used for the FastAPI backend.

4. **Java JDK (OpenJDK or Oracle JDK)**  
   [Download Java JDK](https://www.oracle.com/java/technologies/javase-downloads.html) – Required for Hadoop and Spark.

5. **Git**  
   [Download Git](https://git-scm.com/downloads) – For version control and repository management.

6. **PostgreSQL**  
   [Download PostgreSQL](https://www.postgresql.org/download/) – Used as the database for the application. Both the main and test databases run in Docker containers.

7. **Hadoop**  
   Hadoop is included in the `docker-compose.yml` setup and requires Java. Documentation: [Apache Hadoop](https://hadoop.apache.org/).

8. **Apache Spark**  
   Spark is included in the `docker-compose.yml` setup. Documentation: [Apache Spark](https://spark.apache.org/).

9. **GDAL (Geospatial Data Abstraction Library)**  
   GDAL is installed as a dependency in the backend Dockerfile and is required for geospatial data processing. Documentation: [GDAL](https://gdal.org/).

10. **React and Redux Libraries**  
    These are installed automatically when running the `npm install` command in the `client` folder. Additional React-related dependencies are:
    - `react-app-rewired`
    - `crypto-browserify`
    - `stream-browserify`
    - `os-browserify`
    - `path-browserify`

    Documentation:  
    - [React](https://reactjs.org/)  
    - [Redux](https://redux.js.org/)

11. **Uvicorn**  
    [Uvicorn](https://www.uvicorn.org/) is the ASGI server used to run the FastAPI backend. It is installed automatically via the backend's `requirements.txt`.

12. **AsyncPG**  
    [AsyncPG](https://magicstack.github.io/asyncpg/) – A fast PostgreSQL driver for Python used in the backend.

## Installation and Setup

### Environment Configuration

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Navigate-LA-28.git
   cd Navigate-LA-28
   ```

2. Configure environment variables:
   - Copy example `.env` files:
     ```bash
     cp server/.env.example server/.env
     ```
   - Update the `.env` files with the necessary variables (e.g., database URL, API keys).

---

## Environment Variables

Here’s the updated section for the `README.md` file, specifically addressing the `.env` file setup for the backend:

---

### Backend Environment Variables

The backend uses a `.env` file for environment-specific configurations. Set up the following variables in `server/.env`:

```plaintext
DATABASE_URL=postgresql+asyncpg://<username>:<password>@<hostname>:<port>/<dbname>
TEST_DATABASE_URL=postgresql+asyncpg://<username>:<password>@<hostname>:<port>/<test_dbname>
SECRET_KEY=your_random_secret_key
REACT_APP_URL=http://localhost:3030
REACT_APP_API_URL=http://localhost:8000
```

## Running the Project

1. Build and run the Docker containers:
   ```bash
   docker-compose up -d --build
   ```

2. Verify services:
   - **Frontend**: [http://localhost:3030](http://localhost:3030)
   - **Backend**: [http://localhost:8000](http://localhost:8000)
   - **Hadoop Web UI**: [http://localhost:9870](http://localhost:9870)
   - **Spark Web UI**: [http://localhost:8080](http://localhost:8080)

---
## Populating the Database

To populate the PostgreSQL database with test data, follow these steps:

1. **Access the backend container**:
   ```bash
   docker exec -it navigate_la_backend bash
   ```

2. **Run the following scripts**:

   - **Populate Users**:
     ```bash
     python scripts/populate_users.py
     ```
     Verify:
     ```bash
     docker exec -it navigate_la_postgres psql -U la28_user -d navigate_la28_db
     SELECT id, username, dob, country FROM users LIMIT 10;
     ```

   - **Populate Bus Stops**:
     ```bash
     python scripts/populate_bus_stops.py
     ```
     Verify:
     ```bash
     SELECT COUNT(*) FROM bus_stops;
     SELECT * FROM bus_stops LIMIT 5;
     ```

   - **Populate Bus Route Usage**:
     ```bash
     python scripts/populate_bus_route_usages.py
     ```
     Verify:
     ```bash
     SELECT COUNT(*) FROM customer_usage;
     SELECT * FROM customer_usage LIMIT 5;
     ```

   - **Populate Places**:
     ```bash
     python scripts/populate_places.py
     ```
     Verify:
     ```bash
     SELECT COUNT(*) FROM places;
     SELECT * FROM places LIMIT 10;
     ```

   - **Populate Reviews**:
     ```bash
     python scripts/populate_reviews.py
     ```
     Verify:
     ```bash
     SELECT COUNT(*) FROM reviews;
     SELECT * FROM reviews LIMIT 10;
     ```

These scripts will populate the database with test data for users, bus stops, routes, places, and reviews, ensuring the application is ready for testing.

---

## Development Workflow

- **Frontend**: Modify files in `client/src/`. Use `npm start` for live reloading.
- **Backend**: Modify files in `server/`. Changes will reload automatically with `uvicorn`.

---

## Testing and Debugging

- View container logs:
  ```bash
  docker-compose logs <service_name>
  ```

- Access a running container:
  ```bash
  docker exec -it <container_name> bash
  ```

## Conclusion

This project, **Navigate-LA-28**, showcases the integration of Big Data Management and geospatial data processing to provide a seamless solution for tourists navigating LA. With a React frontend, FastAPI backend, and robust data handling using Hadoop and Spark, the project aims to demonstrate the potential of modern web technologies and data engineering in real-world applications.

By following the steps outlined in this documentation, developers and testers can easily set up the environment, populate the database with test data, and explore the features of the application. We hope this project serves as a valuable reference for similar big data and geospatial applications.

If you encounter any issues or have any suggestions for improvement, feel free to raise an issue or contribute to the repository. Thank you for exploring **Navigate-LA-28**!

---

## Contact Information

For any queries or support, feel free to contact the group members:

| Name                | Email                       |
|---------------------|-----------------------------|
| Aditya Gambhir      | agambhir001@ucr.edu        |
| Faizaan Muzawar     | member2@example.com        |
| Ajit Singh          | member3@example.com        |
| Samara Miramontes   | member4@example.com        |

We appreciate your time and interest in our project!