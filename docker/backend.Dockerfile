# Dockerfile pour le backend FastAPI
FROM python:3.11-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y build-essential

# Copier le code source
WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Lancer FastAPI avec uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
