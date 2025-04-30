FROM debian:bullseye-slim

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH
ENV TERM=xterm

# Install Java, Python, and system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-11-jre \
        libusb-1.0-0-dev \
        wget \
        tar \
        sudo \
        bash \
        nano \
        expect \
        python3 \
        python3-pip \
        python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p /opt/sms /opt/powerview /opt/app

# Copy SMS installer and setup
COPY install_SMS.tar.gz /opt/sms/
COPY install_spv.exp /opt/sms/

WORKDIR /opt/sms
RUN tar -xzvf install_SMS.tar.gz && rm install_SMS.tar.gz
RUN chmod +x /opt/sms/install_spv.exp
RUN /opt/sms/install_spv.exp
RUN chmod +x /opt/powerview/powerview

# Copy your scripts and requirements
COPY scripts/requirements.txt /opt/app/
COPY scripts/polling_endpoint.py /opt/app/

# Set up Python virtual environment and install dependencies
WORKDIR /opt/app
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Start powerview and run the script, keeping container alive
CMD ["/bin/bash", "-c", "/opt/powerview/powerview start --no-gui -d && source /opt/app/venv/bin/activate && python /opt/app/polling_endpoint.py & tail -f /dev/null"]