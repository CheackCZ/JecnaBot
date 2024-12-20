# JečnáBot

## Obsah
- [Úvod](#úvod)
- [Architektura](#architektura)
- [Funkcionalita](#Funkcionalita)
  - [WebSocket Server](#websocket-server)
  - [WebSocket Klient](#websocket-klient)
  - [Logování a analýza](#logování-a-analýza)
  - [Správa konfigurace](#správa-konfigurace)
- [Instalace](#instalace)
- [Spuštění Projektu](#spuštění-projektu)
  - [Spuštění serveru](#spuštění-klienta)
  - [Spuštění klienta](#spuštění-serveru)
  - [Ukončení Spojování](#ukončení-spojování)
- [Struktura projektu](#struktura-projektu)
- [Testování](#testování)
- [Deployment a odevzdání](#deployment-a-odevzdání)
- [Zdroje](#zdroje)


## Úvod
**JečnáBot** je chatbot (AI) zaměřen a specifikován pouze na školu SPŠE Ječná, tudíž odpovídá pouze na dotazy, které nějak souvisí s touto školou, protože byl vytrénován na testovacích datech (dvakrát), týkajících se pouze této školy. 

Používá webSocket server a klienty, kteří se k serveru připojí a mohou se ptát na otázky. Chatbot následně odpoví pomocí OpenAI API a testovacích dat.

Projekt zahrnuje asynchronní serverovou logiku, správu jednotlivých relací a logování komunikace do souboru. Všechny konfigurační data jsou brána ze souboru config.json.

## Architektura
- `server.py`: Serverová aplikace využívající knihovnu websockets. Zpracovává připojení klientů, správu konfigurace a dynamické generování odpovědí pomocí ResponseLogic.
- `client.py`: Klientská aplikace pro interakci se serverem. Umožňuje uživateli zasílat zprávy a přijímat odpovědi.
- `session.py`: Správa jednotlivých relací WebSocket spojení. Obsahuje logiku pro příjem a zpracování zpráv.
- `response_logic.py`: Zpracování odpovědí pomocí OpenAI API.
- `log_manager.py`: Správa logů a analýza často kladených dotazů


## Funkcionalita
### WebSocket Server:
- Asynchronní komunikace s klienty.
- Dynamická odpověď na otázky pomocí OpenAI API.
- Správa konfigurace za běhu (klávesové zkratky).

### WebSocket Klient:
- Odesílání dotazů na server.
- Příjem odpovědí.
- Možnost odpojení.

### Logování a analýza:
 - Záznam všech dotazů a odpovědí.
 - Identifikace nejčastějších dotazů.

### Správa konfigurace:
 - Validace konfiguračního souboru.
 - Načítání nových nastavení za běhu.


## Instalace
1. Naklonování repozitáře (příp. otevření zip souboru)
  ```
  git clone https://github.com/CheackCZ/JecnaBot.git
  cd JecnaBot
  ```

2. Instalace závislostí (pomocí pip)
 - Projekt je psán v `python 3.13.1`
  ```
  pip install -r requirements.txt
  ```  

3. Nastavení konfigurace
 - v souboru `config.json`:
 ```json
{
    "host": "localhost",
    "port": 7777,
    "ai_prompt": "Responses in english only ...",
    "ai_model": "gpt-4o-mini",
    "openai_api_key": "TVŪJ_API_KLÍČ"
}
```
   - **host** - Adresa serveru (např. `127.0.0.1`).
   - **port** - Port, na kterém bude server naslouchat.
   - **ai_prompt** - Počáteční prompt pro OpenAI API.
   - **ai_model** - Model použitý pro generování odpovědí.
   - **openai_api_key** - API klíč OpenAI.


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

## Struktura projektu
```
.
├── /data                       # Data (trénovací)
│   └── training_Data.jsonl     # Trénovací data (v požadovaném formátu)
│
├── /logs                       # Soubory s logy a statistikami
│   ├── log.txt                 # Logovací data
│   └── stats.txt               # Najčastější dotazy
│
├── /src                        # Zdrojový kód
│   ├── server.py               # Hlavní logika serveru
│   ├── client.py               # Klientská aplikace
│   ├── response_logic.py       # AI Integrace
│   ├── session.py              # Relace jednotlivých komunikačních kanálů
|   └── log_manager.py          # Logování zpráv a nejčastějších dotazů
│
├── /tests                      # Testy
│   ├── test_server.py          # Testy funkcionality serveru
│   ├── test_log_manager.py     # Testy LogManagera
│   ├── test_response_logic.py  # Testy logiky odpovědí (AI)
│   ├── test_client.py          # Testy klienta
│   └── test_session.py         # Testy jednotlivých relací a jejich funkcí
│
├── README.md                   # Popis projektu
└── config.json                 # Konfigurační soubor (např. port, AI detaily)
└── requirements.txt            # Závslosti
```

## Testování
- Byly vytvořeny unit testy pomocí unittest:
  - Testy pro funkce serveru (test_server.py).
  - Testy pro funkce klienta (test_server.py).
  - Analýza logů (test_log_manager.py).
  - Testy pro odpovědi od openai (test_server.py).
  - Testování jednotlivých relací (test_session.py)

- Bylo testován i asynchronní přístup pomocí více připojených uživatelů, více otázek posílaných najednou a asynchronní zapisování do `log.txt` a `stats.txt`.
- Také byli provedeny testy s neplatnou konfigurací a nevalidními vstupy.

__Reporting__
- Bylo by možné dodělat a přidat více uit testů.
- Udělat grafické prostředí.
- Nasadit službu na server.
- Trénovat chatbota s více trénovacími daty.

## Deployment a Odevzdání
- Projekt je odevzdán jako .zip archiv. Avšak je možné si ho stáhnout z githubu po povolení přístupu: [Github](https://github.com/CheackCZ/JecnaBot).

## Zdroje
- [ChatGPT]()
- [Platforma OpenAI API]()
- [Kódy ze cvičení]()
- [Oficiální python dokumentace]()
- [Asynchronní unittesty](https://bbc.github.io/cloudfit-public-docs/asyncio/testing.html)
- [.jsonl](https://jsonlines.org/)
- [Asychnronní používání 1](https://naucse.python.cz/lessons/intro/async/)
- [Asychnronní používání 2](https://www.geeksforgeeks.org/asyncio-in-python/)
...

<br>

__Autor__ - Ondřej Faltin.