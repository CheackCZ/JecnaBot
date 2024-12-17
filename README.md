# JečnáBot

**JečnáBot** je WebSocket server a klient, který poskytuje odpovědi na dotazy uživatelů o škole SPŠE Ječná s využitím OpenAI API. Projekt zahrnuje asynchronní serverovou logiku, správu jednotlivých relací a logování komunikace do souboru. Všechny konfigurační data jsou brána ze souboru config.json.

## Funkcionalita
- **Server:**
  - Poslouchá připojení přes WebSocket na definovaném hostu a portu.
  - Zpracovává dotazy uživatelů a vrací odpovědi přes OpenAI API.
  - Loguje dotazy a odpovědi do textového souboru `log.txt`.

- **Klient:**
  - Navazuje spojení se serverem.
  - Umožňuje uživateli zasílat dotazy a získávat odpovědi v reálném čase.

## Požadavky
Projekt je napsán v Pythonu (3.13.1) a vyžaduje následující knihovny:
- `websockets` (WebSocket server a klient)
- `openai` (API OpenAI)
- `asnycio` (Asynchronní metody)

### Instalace knihoven
Spusť následující příkazy pro instalaci knihoven:
```bash
pip install websockets openai
```

## Konfigurace
Všechny důležité parametry jsou uloženy v souboru `config.json`:
```json
{
    "host": "127.0.0.1",
    "port": 8765,
    "openai_api_key": "TVŪJ_API_KLÍČ"
}
```
- **host:** Adresa serveru (např. `127.0.0.1`).
- **port:** Port, na kterém bude server naslouchat.
- **openai_api_key:** Tvůj API klíč pro OpenAI.

Ujisti se, že máš platný OpenAI API klíč.

## Asynchronní metody a kooperativní multitasking
Celý projekt je postaven na asynchronních metodách, což umožňuje efektivní zpracování více uživatelských relací současně:
- **Server:** Metody jako `handle_client` a `run` ve `server.py` používají `async` a `await` pro zpracování připojení více uživatelů bez blokování hlavního vlákna.
- **Klient:** Klient v `client.py` komunikuje se serverem asynchronně pomocí `asyncio` a `websockets.connect`, v mětodě `connect`.
- **Kooperativní multitasking:** Asynchronní programování zajišťuje, že úlohy neblokují ostatní relace nebo úlohy. Místo toho úlohy kooperují a střídají se v používání CPU.

Příkladem je čekání na zprávu klienta nebo odpověď od OpenAI API, které neblokuje zpracování dalších relací:
```python
async def handle_session(self):
    while True:
        client_message = await self.websocket.recv()
        response = self.logic.get_answer(client_message)
        await self.websocket.send(response)
```

## Spuštění projektu

### Spuštění serveru
Server lze spustit pomocí příkazu:
```bash
python server.py
```
Server bude naslouchat na adrese a portu specifikovaném v `config.json`.

### Spuštění klienta
Klient připojující se k serveru se spustí takto:
```bash
python client.py
```
Po připojení můžeš začít zasílat dotazy.

### Ukončení spojování
Pro ukončení spojování zadej do klienta příkaz:
```
exit
```
nebo se odpoj ručně pomocí:
```
CTRL + C
```

## Logování
Veškerá komunikace mezi klientem a serverem (dotazy a odpovědi) je zaznamenána do souboru `log.txt`.

## Struktura projektu
```
.
├── /src               # Zdrojový kód
│   ├── server.py         # Hlavní logika serveru
│   ├── client.py         # Klientská aplikace
│   ├── response_logic.py # AI Integrace
│   ├── session.py        # Relace jednotlivých komunikačních kanálů
|   └── log_manager.py  # Logování zpráv 
├── /tests             # Testy
│   ├── test_server.py  # Testy funkcionality serveru
│   ├── test_client.py  # Testy klienta
│   └── test_logic.py   # Testy logiky odpovědí
├── /docs              # Dokumentace
│   ├── requirements.txt
│   └── user_guide.pdf  # Uživatelská příručka (volitelně)
├── README.md       # Popis projektu
└── config.json     # Konfigurační soubor (např. port, AI klíče)
```

## Ukázka použití
1. Spusť server (`server.py`).
2. Spusť klienta (`client.py`).
3. Začni pokládat dotazy a sledovat odpovědi.

Příklad interakce:
```
 > Vy: Jaké obory má SPŠE Ječná?
 └ Bot: SPŠE Ječná nabízí obory jako...
```

### Autor
Ondřej Faltin.
