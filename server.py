# importiamo i pacchetti dal nostro ambiente virtuale
import httpx
from mcp.server.fastmcp import FastMCP

#praticamente stiamo usando FastMCP, troviamo tutto sulla guida ufficiale di antropic, diciamo prendi dal pacchetto mcp
#cartella server la classe FastMCP

#ora creiamo il vero e proprio server, mettiamo dentro la variabile mcp_server FastMCP

mcp = FastMCP("Enterprise Data Server")

#creiamo il primo tool della nostra fabrica, in pratica gli stiamo dicendo, 
#Prendi questa funzione che c'è qui sotto, analizzala, 
#impacchettala e inseriscila nel catalogo ufficiale degli strumenti che l'IA può utilizzare

#spiegazione tencnica, creiamo una funzione asincrona che prende in input un int e in output una stringa (-> str:)
#la roba tra virgolette viene passata all'intelligenza artificiale e gli da le istruzioni

@mcp.tool()
async def fetch_enterprise_json(codice_fiscale: str) -> str:
    """
    Recupera i dati aziendali di un utente in formato json partendo dal suo codice fiscale.
    Usa questo strumento quando l'utente chiede informazioni su un dipendeteo un utente specifico
    """
    # con questo url stiamo dicendo dove andare a prendere la cartella del dipendente,
    # la f davanti a https si chiama f string e dice "prendi il valore 
    # che c'è dentro la variabile codice_fiscale e mettilo a fine link"
    url =f"https://jsonplaceholder.typicode.com/users/{codice_fiscale}"

    # ora andiamo a usare httpx per creare il nostro browser in modo che si possa fare la retrive dall'url qui sopra 
    # async with, questo è importante ci garantisce la gestione asincorna del processo e il with ci permette di chiudere
    # l'instanza nel momento che il processo giunge al suo termine, senza RIMAREBBE APERTO memory leak
    # Computer, per favore apri una sessione protetta (async with), accendi un browser invisibile e chiamalo client 
    # (httpx.AsyncClient() as client). Tieniti pronto, perché nelle 
    # righe che seguono userò questo browser per navigare. Appena avrò finito, chiudi tutto da solo e non sprecare memoria".

    async with httpx.AsyncClient() as Client:
        # qui creiamo una nuova variabile e ci mettiamo dentro la risposta del nostro browser, await ci garantisce che 
        # il processo aspetti 

        # Prendi il browser invisibile (client), mandalo all'indirizzo internet 
        # (url) a scaricare i dati della pagina. Aspetta pazientemente 
        # che i dati arrivino (await) e, quando finalmente li hai ricevuti, impacchettali tutti dentro la scatola chiamata response"
        response = await Client.get(url)

        # qui diciamo restituisci solo il testo (.text) lascia stare errori ecc
        return response.text 

# Questa riga dice a Python: "Esegui quello che c'è qui sotto solo se l'utente ha cliccato "Play" 
# o ha lanciato questo specifico file dal terminale. 
# Se questo file è stato aperto di nascosto da un altro programma, non fare nulla e stai fermo".
if __name__ == "__main__":
    # qui diciamo start server con mcp_server... e poi il metodo di comunicazione, in questo caso stdio standard input output
    mcp.run(transport="stdio")