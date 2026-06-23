import os
import logging
import httpx
from mcp.server.fastmcp import FastMCP

# 1. Configurazione del Logging (per vedere i passaggi nei log di Docker)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-enterprise-server")

# 2. Inizializzazione del Server MCP
mcp = FastMCP("Enterprise Data Server")

# 3. Indirizzo del container vLLM (gestito dalla rete di Docker)
VLLM_HOST = os.getenv("VLLM_HOST", "http://localhost:8000")

# -------------------------------------------------------------------------
# 🚧 SEZIONE JSON (IN PAUSA / DA DEFINIRE)
# -------------------------------------------------------------------------
@mcp.tool()
async def recupera_json_aziendale() -> str:
    """
    [TEMPORANEAMENTE IN STOP]
    Questo tool gestirà il recupero o la ricezione del file JSON aziendale.
    Al momento restituisce un messaggio di standby.
    """
    logger.info("ℹ️ [TOOL] Chiamato tool JSON (attualmente in stop).")
    return "Funzionalità di recupero JSON attualmente in standby. Configurazione in corso."


# -------------------------------------------------------------------------
# 🧠 SEZIONE IA: Il motore per usare effettivamente vLLM
# -------------------------------------------------------------------------
@mcp.tool()
async def chiedi_all_intelligenza_artificiale(domanda: str) -> str:
    """
    Invia una domanda o un compito direttamente al modello IA Qwen (su GPU Nvidia).
    Usa questo strumento per elaborare testi, fare analisi o ragionamenti generici.
    """
    logger.info(f"🚀 [IA] Invio richiesta a vLLM. Domanda: '{domanda[:40]}...'")
    
    # URL ufficiale delle API compatibili con OpenAI esposte da vLLM
    url = f"{VLLM_HOST}/v1/chat/completions"
    
    # Il pacchetto di dati richiesto da vLLM
    payload = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [
            {"role": "system", "content": "Sei un assistente AI Enterprise integrato via MCP. Rispondi in modo professionale e in italiano."},
            {"role": "user", "content": domanda}
        ],
        "temperature": 0.3
    }
    
    # Sessione asincrona protetta per inviare i dati all'IA
    async with httpx.AsyncClient(timeout=60.0) as Client:
        try:
            response = await Client.post(url, json=payload)
            response.raise_for_status()
            
            # Estraiamo la risposta testuale restituita dal modello
            risultato = response.json()
            return risultato["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.error(f"❌ Errore di comunicazione con vLLM: {str(e)}")
            return f"Impossibile parlare con l'IA. Controlla che vLLM sia attivo. Errore: {str(e)}"

if __name__ == "__main__":
    # Avvio del server in modalità Standard I/O (richiesta dai client MCP)
    mcp.run(transport="stdio")