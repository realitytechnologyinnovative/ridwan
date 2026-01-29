ARG PYTHON_VERSION=3.10-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install psycopg2 dependencies and other needed packages
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /code

# Copy and install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

# Copy the rest of the code
COPY . /code

# Copy the entrypoint script
COPY startup.sh /code/startup.sh
RUN chmod +x /code/startup.sh

# Expose the app port
EXPOSE 8000

# Use the entrypoint script
ENTRYPOINT ["/code/startup.sh"]
