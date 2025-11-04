FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PATH="/root/.cargo/bin:$PATH"

# Install system deps first (cached unless you change this list)
RUN apt-get update && apt-get install -y \
    curl wget git build-essential software-properties-common \
    python3 python3-pip python3-venv \
    r-base \
    nodejs npm \
    perl \
    # rustc cargo \
    # For the PCRE2 C script
    gcc \
    libpcre2-dev \
    libcjson-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install language dependencies
# R
RUN R -e "install.packages('jsonlite', repos='https://cloud.r-project.org')"
# Python
# I'm really not worried about conflicting with system packages here
# Copy over just the requirements file first, so we can cache this command
COPY ./tests/test-requirements.txt /app/tests/
RUN pip install --no-cache-dir --break-system-packages -r /app/tests/test-requirements.txt

# Copy stuff over
COPY . /app
WORKDIR /app/tests

ENV PYTHONUNBUFFERED=1

# Install the library itself
RUN pip install --no-cache-dir --break-system-packages -e ..

ENTRYPOINT ["bash", "manager.sh"]
CMD []
