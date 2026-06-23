import os
import logging
import httpx
from mcp.server.fastmcp import FastMCP

# 1. Configurazione del Logging (per vedere i passaggi nei log di Docker)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-enterprise-server")

# 2. Inizializzazione del Server MCP
mcp = FastMCP("Enterprise Data Server")


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
# 🧠 SEZIONE IA: Il motore dinamico (Cloud Groq / Locale vLLM)
# -------------------------------------------------------------------------
@mcp.tool()
async def chiedi_all_intelligenza_artificiale(domanda: str) -> str:
    """
    Invia una domanda o un compito direttamente al modello IA Qwen.
    Il sistema seleziona automaticamente se usare Groq Cloud o vLLM locale.
    """
    # Leggiamo la modalità configurata nel Docker Compose (Default: locale)
    ai_mode = os.getenv("AI_MODE", "locale").lower().strip()
    
    url = ""
    headers = {}
    payload = {}

    # --- CASO A: GROQ CLOUD ---
    if ai_mode == "groq":
        groq_host = os.getenv("GROQ_HOST", "https://api.groq.com/openai")
        groq_key = os.getenv("GROQ_API_KEY", "")
        
        logger.info(f"🚀 [IA-CLOUD] Invio richiesta a Groq. Domanda: '{domanda[:40]}...'")
        
        url = f"{groq_host}/v1/chat/completions"
        if groq_key:
            headers["Authorization"] = f"Bearer {groq_key}"
            
        payload = {
            "model": "qwen-2.5-32b",
            "messages": [
                {"role": "system", "content": "Sei un assistente AI Enterprise integrato via MCP. Rispondi in modo professionale e in italiano."},
                {"role": "user", "content": domanda}
            ],
            "temperature": 0.3
        }

    # --- CASO B: LOCALE NVIDIA (vLLM) ---
    else:
        vllm_host = os.getenv("VLLM_HOST", "http://localhost:8000")
        
        logger.info(f"🏠 [IA-LOCALE] Invio richiesta a vLLM locale. Domanda: '{domanda[:40]}...'")
        
        url = f"{vllm_host}/v1/chat/completions"
        payload = {
            "model": "Qwen/Qwen2.5-7B-Instruct",
            "messages": [
                {"role": "system", "content": "Sei un assistente AI Enterprise integrato via MCP. Rispondi in modo professionale e in italiano."},
                {"role": "user", "content": domanda}
            ],
            "temperature": 0.3
        }

    # --- SPEDIZIONE RICHIESTA ---
    async with httpx.AsyncClient(timeout=60.0) as Client:
        try:
            response = await Client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            # Estraiamo la risposta testuale restituita dal modello
            risultato = response.json()
            return risultato["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.error(f"❌ Errore di comunicazione in modalità [{ai_mode.upper()}]: {str(e)}")
            return f"Impossibile parlare con l'IA ({ai_mode}). Errore: {str(e)}"


if __name__ == "__main__":
    # Avvio del server in modalità Standard I/O (richiesta dai client MCP)
    # Questo costringe il server a rimanere attivo in ascolto sulla porta 8000
    mcp.run(transport="sse")