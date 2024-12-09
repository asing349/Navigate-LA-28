# Use the Bitnami Spark image as the base
FROM bitnami/spark:3.3.0

# Install wget and OpenJDK for Hadoop
USER root
RUN install_packages wget openjdk-11-jdk

# Set up Hadoop
ENV HADOOP_VERSION=3.3.1
RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xzf hadoop-${HADOOP_VERSION}.tar.gz && \
    mv hadoop-${HADOOP_VERSION} /opt/hadoop && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

# Add Hadoop binaries to PATH
ENV PATH=$PATH:/opt/hadoop/bin:/opt/hadoop/sbin

# Set Hadoop environment variables
ENV HADOOP_HOME=/opt/hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
