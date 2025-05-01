FROM alpine:3.14

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk
ENV PATH=$JAVA_HOME/bin:$PATH
ENV TERM=xterm

RUN apk update && \
    apk add --no-cache \
        openjdk11-jre-headless \
        libusb-dev \
        tar \
        bash \
        expect \
        python3 \
        py3-pip \
        py3-virtualenv

RUN mkdir -p /opt/sms /opt/powerview /opt/app

COPY install/linux.tar.gz /opt/sms/
COPY install/automate_install.exp /opt/sms/

WORKDIR /opt/sms
RUN tar -xzvf linux.tar.gz && rm linux.tar.gz
RUN chmod +x /opt/sms/automate_install.exp
RUN /opt/sms/automate_install.exp || true  # in case expect script exits unexpectedly
RUN chmod +x /opt/powerview/powerview

COPY proxy/requirements.txt /opt/app/
COPY proxy/polling_endpoint.py /opt/app/

WORKDIR /opt/app
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

COPY install/entrypoint.sh /entrypoint.sh

# Remove the installer
RUN rm -rf /opt/sms

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]