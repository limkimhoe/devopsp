# Python base with minimal image size
FROM python:3.11-slim
# Install OpenSSH client for ssh command support
RUN apt-get update && apt-get install -y openssh-client

# Create a non-root user (VS Code expects 'vscode' by default)
ARG USER=vscode
ARG UID=1000
ARG GID=1000

# System deps:
# - build-essential, gcc, gfortran: build wheels for scientific libs
# - libopenblas-dev, liblapack-dev: BLAS/LAPACK for numpy/scipy/sklearn
# - libpq-dev: psycopg2 (PostgreSQL client dev headers)
# - curl, git: common dev tooling
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential gcc gfortran \
    libopenblas-dev liblapack-dev \
    libpq-dev \
    curl git ca-certificates sudo \
    && rm -rf /var/lib/apt/lists/*

# Create user
RUN groupadd --gid ${GID} ${USER} \
    && useradd -s /bin/bash --uid ${UID} --gid ${GID} -m ${USER}

# Python config
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Make OpenBLAS default visible
    OPENBLAS_NUM_THREADS=1

# Set up workdir
WORKDIR /workspace

# Optional: pre-copy requirements to leverage Docker layer caching
# (safe even if requirements.txt doesn't exist yet)
COPY requirements.txt /tmp/requirements.txt
RUN pip install -U pip wheel && \
    if [ -f /tmp/requirements.txt ]; then pip install -r /tmp/requirements.txt || true; fi

# Helpful dev tools (optional)
RUN pip install ruff pip-tools ipython

# Expose common dev ports
EXPOSE 5000 8888

USER ${USER}

# Default to a long-running sleep; VS Code Dev Containers will exec into it.
