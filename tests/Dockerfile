FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PATH="/root/.cargo/bin:$PATH"

# Install system deps first (cached unless you change this list)
RUN apt-get update && apt-get install -y \
    curl wget git build-essential software-properties-common \
    python3 python3-pip python3-venv \
    r-base \
    nodejs npm \
    # gcc \
    # libcjson-dev \
    # libpcre2-dev \
    # rustc cargo \
    perl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy stuff over
COPY . /app
WORKDIR /app/tests


# Install language dependencies
# PCRE (C)
RUN apt-get update && apt-get install -y libpcre2-dev libcjson-dev
# For some reason it can't find libcjson-dev, even though it exists
# RUN wget http://archive.ubuntu.com/ubuntu/pool/universe/c/cjson/libcjson-dev_1.7.17-1_amd64.deb
# RUN dpkg -i libcjson-dev_1.7.17-1_amd64.deb
# R
RUN R -e "install.packages('jsonlite', repos='https://cloud.r-project.org')"
# Python
# I'm really not worried about conflicting with system packages here
RUN pip install --no-cache-dir --break-system-packages -r test-requirements.txt

# Install the library itself
RUN pip install --no-cache-dir --break-system-packages -e ..

ENTRYPOINT ["bash", "manager.sh"]
CMD []
