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

# Create necessary directories and set permissions
RUN mkdir -p /opt/bitnami/spark/logs && \
    chmod -R 777 /opt/bitnami/spark/logs && \
    mkdir -p /tmp/spark-events && \
    chmod -R 777 /tmp/spark-events

# Set default user
ENV USER=root
ENV HADOOP_USER_NAME=root

# Create core-site.xml with basic configuration
RUN mkdir -p $HADOOP_HOME/etc/hadoop && \
    echo '<?xml version="1.0" encoding="UTF-8"?>' > $HADOOP_HOME/etc/hadoop/core-site.xml && \
    echo '<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>' >> $HADOOP_HOME/etc/hadoop/core-site.xml && \
    echo '<configuration>' >> $HADOOP_HOME/etc/hadoop/core-site.xml && \
    echo '    <property>' >> $HADOOP_HOME/etc/hadoop/core-site.xml && \
    echo '        <name>hadoop.security.authentication</name>' >> $HADOOP_HOME/etc/hadoop/core-site.xml && \
    echo '        <value>simple</value>' >> $HADOOP_HOME/etc/hadoop/core-site.xml && \
    echo '    </property>' >> $HADOOP_HOME/etc/hadoop/core-site.xml && \
    echo '</configuration>' >> $HADOOP_HOME/etc/hadoop/core-site.xml
