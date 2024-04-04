FROM mageai/mageai:latest

# Add non-root user for Mage service
RUN adduser --disabled-password --gecos '' mage && adduser mage mage

# Grant the user permissions to the Mage related directories
RUN mkdir /home/src/mage_data; chown -R mage /home/src/mage_data
RUN mkdir /home/src/default_repo; chown -R mage /home/src/default_repo

ENV PYTHONPATH="${PYTHONPATH}:/home/mage/.local/lib/python3.10/site-packages"

WORKDIR /home/src

COPY . /home/src/

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN apt-get update && apt-get install -y wget unzip && \
    wget http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_122.0.6261.111-1_amd64.deb && \
    apt install -y ./google-chrome-stable_122.0.6261.111-1_amd64.deb && \
    rm google-chrome-stable_122.0.6261.111-1_amd64.deb && \
    apt-get clean

CMD ["/bin/sh", "-c", "/app/run_app.sh"]


