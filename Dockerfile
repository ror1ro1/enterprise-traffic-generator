FROM python:3.11-slim

# Blokada tworzenia plików .pyc i włączenie natychmiastowego logowania w konsoli
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Kopiowanie i instalacja bibliotek
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu źródłowego
COPY . .

# Uruchomienie serwera webowego na porcie 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
