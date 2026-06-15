# -------------------------------------------------------------------------------
# 1. IL PUNTO DI PARTENZA (L'ambiente base)
# Prende dal web un mini-computer Linux "congelato" che ha già Python 3.11 installato.
# Il flag "-slim" indica che è la versione più leggera e veloce, senza programmi inutili.
# -------------------------------------------------------------------------------
FROM python:3.11-slim

# -------------------------------------------------------------------------------
# 2. LA CARTELLA DI LAVORO (Il quartier generale)
# Crea una cartella chiamata "/app" dentro il computer virtuale di Docker.
# Da questo momento in poi, tutte le operazioni successive avverranno lì dentro.
# -------------------------------------------------------------------------------
WORKDIR /app

# -------------------------------------------------------------------------------
# 3. IL PASSAGGIO DEI REQUISITI (La lista della spesa)
# Prende il file "requirements.txt" dal tuo PC reale e lo copia dentro la cartella del container.
# Il punto "." alla fine significa proprio: "copialo qui, nella cartella corrente (/app)".
# -------------------------------------------------------------------------------
COPY requirements.txt .

# -------------------------------------------------------------------------------
# 4. L'INSTALLAZIONE DELLE LIBRERIE (Allestimento officina)
# Esegue il comando nel terminale interno di Docker per installare FastMCP e HTTPX.
# Il flag "--no-cache-dir" evita di salvare i file di installazione temporanei su internet,
# tenendo il container leggero e piccolo.
# -------------------------------------------------------------------------------
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------------------------------------------------------
# 5. IL PASSAGGIO DEL CODICE (Il motore dell'applicazione)
# Prende il tuo file "server.py" (quello con la funzione per i codici fiscali)
# dal tuo PC reale e lo copia dentro il container.
# Lo facciamo DOPO l'installazione delle librerie così, se modifichi solo il codice,
# Docker non perderà tempo a reinstallare ogni volta i pacchetti da zero.
# -------------------------------------------------------------------------------
COPY server.py .

# -------------------------------------------------------------------------------
# 6. L'INTERRUTTORE DI ACCENSIONE (Il via libera)
# Questo comando NON viene eseguito ora, ma definisce cosa deve fare Docker 
# quando deciderai di accendere il container. In pratica lancia il server Python.
# Il flag "-u" (unbuffered) costringe Python a sputare fuori i dati e i log all'istante, 
# senza accumularli in memoria, cosa vitale per far parlare l'MCP con l'IA.
# -------------------------------------------------------------------------------
CMD ["python", "-u", "server.py"]