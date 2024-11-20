# Navigate-LA-28 Project

A Big Data Management project using geospatial data to help tourists navigate LA. This project includes a React frontend and FastAPI backend, with Hadoop and Spark for data management.

## Table of Contents
- [Navigate-LA-28 Project](#navigate-la-28-project)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Installation and Setup](#installation-and-setup)
    - [Prerequisites](#prerequisites)
    - [Project Setup](#project-setup)
    - [Environment Variables](#environment-variables)
    - [Running the Project](#running-the-project)
    - [Development Workflow](#development-workflow)
    - [Additional Notes](#additional-notes)

## Project Structure

```plaintext
Navigate-LA-28/
├── client/                             # React frontend
│   ├── node_modules/                   # Node.js packages
│   ├── public/                         # Public assets for the frontend
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── robots.txt
│   ├── src/                            # React source code
│   │   ├── assets/
│   │   ├── components/
│   │   │   └── TestProfile.jsx
│   │   ├── constants/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── slices/
│   │   │   ├── index.js
│   │   │   ├── testSlice.js
│   │   │   └── userSlice.js
│   │   ├── styles/
│   │   ├── utils/
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── index.css
│   │   ├── index.js
│   │   └── store.js
│   ├── .gitignore
│   ├── package-lock.json
│   ├── package.json
│   ├── README.md
│   └── .env (example)
│
├── hadoop/
│   └── conf/
│       ├── core-site.xml
│       ├── hdfs-site.xml
│       └── log4j.properties
│
├── navigate_la28/
│   └── server/
│       ├── config/
│       ├── models/
│       ├── routes/
│       ├── schemas/
│       ├── services/
│       ├── tests/
│       ├── utils/
│       ├── .env
│       ├── .env.example
│       ├── .gitignore
│       ├── Dockerfile
│       ├── main.py
│       ├── package-lock.json
│       ├── package.json
│       ├── README.md
│       └── requirements.txt
│
├── spark/
│   └── conf/
│       ├── spark-defaults.conf
│       └── spark-env.sh
│
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Installation and Setup

### Prerequisites

Make sure the following software is installed on your machine:

1. **Docker**: [Download Docker Desktop](https://www.docker.com/products/docker-desktop) to manage containers for frontend, backend, Hadoop, and Spark.
2. **Node.js and npm**: [Download Node.js](https://nodejs.org/) (npm is included with Node.js) to run the React frontend.
3. **Python 3.10+**: [Download Python](https://www.python.org/downloads/) for the FastAPI backend.
4. **Java**: [Download Java JDK](https://www.oracle.com/java/technologies/javase-downloads.html) (required for Hadoop and Spark).
5. **Git**: [Download Git](https://git-scm.com/downloads) for version control.

### Project Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Navigate-LA-28.git
   cd Navigate-LA-28
   ```

2. **Environment Configuration**:
   - Create `.env` files for both the frontend and backend by copying the example files:
     ```bash
     # In the client directory
     cp client/.env client/.env.client
     
     # In the server directory
     cp server/.env server/.env.server
     ```

   - Update these `.env` files with the necessary environment variables (e.g., API URLs, database credentials).

### Environment Variables

- **Frontend**: Environment variables should be prefixed with `REACT_APP_`. Place them in `client/.env`.
  - Example:
    ```plaintext
    REACT_APP_API_URL=http://localhost:8000
    ```

- **Backend**: Place environment variables in `server/.env`. Common variables include database URLs, API keys, etc.
  - Example:
    ```plaintext
    DATABASE_URL=your_database_url_here
    SECRET_KEY=your_secret_key_here
    ```

### Running the Project

1. **Start the Docker Containers**:

   From the root directory, start the containers with Docker Compose:
   ```bash
   docker-compose up -d --build
   ```

   - This will set up the following services:
     - **Frontend**: Runs the React app on `http://localhost:3030`.
     - **Backend**: Runs the FastAPI app on `http://localhost:8000`.
     - **Hadoop and Spark**: Set up for data management.

2. **Verify Services**:

   - Access the **frontend** at `http://localhost:3030`.
   - Access the **backend API** at `http://localhost:8000`.
   - For **Hadoop** and **Spark**, use the Docker container access commands if needed.

3. **Testing and Debugging**:

   - Use `docker-compose logs <service_name>` to view logs for each service (e.g., `docker-compose logs frontend`).
   - To enter a container, use:
     ```bash
     docker exec -it <container_name> /bin/bash
     ```
     For example, to enter the backend:
     ```bash
     docker exec -it navigate_la_backend /bin/bash
     ```

### Development Workflow

- **Frontend**: Edit React files in `client/src/`. Changes will automatically reflect if running in development mode.
- **Backend**: Edit FastAPI files in `server/`. Changes will automatically reflect if running in development mode.

### Additional Notes

- **.gitignore** files are set up to ignore unnecessary files like `__pycache__` in the backend and `node_modules` in the frontend.
- **Redux**: Redux is set up for state management in the frontend. State slices are located in `client/src/slices/`.
