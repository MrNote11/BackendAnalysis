FROM python:3.11.9-slim

# --------------------------------------------------
# Python environment settings
# --------------------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# --------------------------------------------------
# System dependencies
# --------------------------------------------------
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    libcairo2 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------
# Virtual environment
# --------------------------------------------------
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip

# --------------------------------------------------
# App directory
# --------------------------------------------------
WORKDIR /code

# --------------------------------------------------
# Install Python dependencies first (layer caching)
# --------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --------------------------------------------------
# Copy project code
# --------------------------------------------------
COPY ./src /code

# --------------------------------------------------
# Runtime script
# --------------------------------------------------
COPY ./boot/docker-run.sh /opt/run.sh
RUN chmod +x /opt/run.sh

CMD ["/opt/run.sh"]
