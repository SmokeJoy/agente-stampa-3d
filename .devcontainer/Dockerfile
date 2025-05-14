# Usa l'immagine Python ufficiale come immagine base
FROM python:3.12-slim

ARG NODE_VERSION=20.14.0

# Imposta la directory di lavoro
WORKDIR /app

# Installa le dipendenze di sistema necessarie per Node.js, build-essential, git e altri strumenti
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    build-essential \
    git \
    # Assicura che nodejs e npm siano installati tramite apt-get
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Rimuovi la precedente installazione di Node.js tramite script se presente
# RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash -
# RUN apt-get install -y nodejs

# Verifica le versioni di Node e npm
RUN node -v
RUN npm -v

# Installa Spectral CLI globalmente tramite npm con versione pinnata
RUN npm install -g @stoplight/spectral-cli@6.15.0
# Installa Redocly CLI globalmente tramite npm con versione pinnata (se ancora necessario)
# RUN npm install -g @redocly/cli@1.13.1 # Rimosso perché non richiesto e causa problemi di versione

# Installa Poetry
ENV POETRY_HOME="/opt/poetry"
# Imposta la versione di Poetry, o la versione desiderata
ENV POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

# Verifica installazione Poetry
RUN poetry --version

# Verifica le installazioni
RUN spectral --version
RUN git --version
# RUN redocly --version # Rimosso perché il pacchetto è stato rimosso

COPY .devcontainer/run_in_container.sh /usr/local/bin/run_in_container.sh
RUN chmod +x /usr/local/bin/run_in_container.sh

# Copia il file requirements.txt (se esiste già, altrimenti verrà creato e copiato dopo)
# COPY requirements.txt .

# Installa le dipendenze Python (se requirements.txt è presente)
# RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto dell'applicazione nel contenitore
COPY . .

# Mantieni il container in esecuzione (opzionale, per debugging)
# CMD ["tail", "-f", "/dev/null"] 

# Configura Poetry per non creare venvs nella directory del progetto 
