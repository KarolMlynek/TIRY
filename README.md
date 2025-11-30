# TIRY

Aplikacja do zarządzania flotą ciężarówek – frontend w React/Vite, backend w FastAPI, wszystko uruchamiane w Dockerze.

## Opis

- **Backend**: FastAPI, odpowiedzialny za API do zarządzania ciężarówkami i kierowcami.  
- **Frontend**: React + Vite, interfejs użytkownika dla aplikacji flotowej.  
- **Docker**: Backend i frontend uruchamiane w kontenerach, z wolumenem `node_modules` dla frontendu, aby uniknąć problemów z zależnościami na różnych architekturach.

## Kontenery

- **backend** – serwer API FastAPI działający na porcie `8000`  
- **frontend** – aplikacja React działająca na porcie `5173`  
- **node_modules** – volume dla zależności Node.js

## Uruchamianie aplikacji

### Pierwsze uruchomienie

W terminalu w katalogu projektu wpisz:  

```bash
docker-compose up --build
```
### Kolejne uruchomienia

```bash
docker-compose up
```

Dostęp

```bash
Frontend: http://localhost:5173

Backend API: http://localhost:8000
```

### Uwagi

Frontend automatycznie proxuje zapytania /api do backendu.

Seed-data (demo) dla backendu uruchamiane jest automatycznie przy starcie.