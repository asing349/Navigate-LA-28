# Use the official Python image as a base
FROM python:3.11.5

# Set the working directory inside the container
WORKDIR /app

# Install GDAL dependencies required for geospatial data processing
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL environment variables
ENV GDAL_VERSION=3.6.2
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Copy Python dependencies file first (to cache Docker layers)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for Hadoop and OpenJDK 8
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    software-properties-common && \
    # Add Adoptium repository for OpenJDK 8
    wget -qO - https://packages.adoptium.net/artifactory/api/gpg/key/public | apt-key add - && \
    echo "deb https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    temurin-8-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for OpenJDK 8
ENV JAVA_HOME=/usr/lib/jvm/temurin-8-jdk-arm64
ENV PATH=$JAVA_HOME/bin:$PATH

# Download Hadoop client jar to support Spark
RUN apt-get install -y wget
RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-client/3.3.1/hadoop-client-3.3.1.jar -P /opt/spark/jars

# Copy all application files into the container
COPY . .

# Expose the application port
EXPOSE 8000

# Start the FastAPI server with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "debug"]
