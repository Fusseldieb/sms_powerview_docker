FROM debian:bullseye-slim

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH
ENV TERM=xterm

RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-11-jre libusb-1.0-0-dev wget tar sudo bash nano expect && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/sms /opt/powerview

COPY install_SMS.tar.gz /opt/sms/

WORKDIR /opt/sms
RUN tar -xzvf install_SMS.tar.gz && \
    rm install_SMS.tar.gz

COPY install_spv.exp /opt/sms/

RUN chmod +x /opt/sms/install_spv.exp

RUN /opt/sms/install_spv.exp

RUN chmod +x /opt/powerview/powerview

CMD ["/bin/bash", "-c", "/opt/powerview/powerview start --no-gui -d && tail -f /dev/null"]
