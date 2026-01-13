# Trabalho 3 — Loja de Mídias (WS/API + Protocolo Request/Response)

Este projeto reimplementa o serviço remoto do Trabalho 2 usando **comunicação cliente-servidor via HTTP (WS/API)**, organizado como **protocolo de requisição/resposta**, **sem usar sockets manuais e sem RMI**.

O servidor foi feito em **Python (FastAPI)** e existem **dois clientes em linguagens diferentes do servidor**:
- **JavaScript (Node.js)**
- **Java**

---

## Quick Start

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

uvicorn app.server_api:app --host 0.0.0.0 --port 8000
node clients/client.js 
javac -encoding UTF-8 clients/ClientJava.java
java -cp clients ClientJava
```

Para rodar em outra máquina:

```
$env:API_BASE="http://IP_DO_SERVIDOR:8000"
node clients\client.js

java -cp clients ClientJava http://IP_DO_SERVIDOR:8000/invoke
```

---

## Estrutura

- **Servidor (FastAPI)**
  - Expõe um endpoint principal `POST /invoke`
  - Recebe uma requisição de “invocação remota” e responde com `InvokeReply`

- **Serviços**
  - `CatalogoService`: cadastro, listagem e busca
  - `TransacaoService`: venda e troca
  - `Loja`: estoque e operações de busca/lista

- **Modelos**
  - `Produto` (base)
  - `Livro`, `EBook`, `Apostila`, `CD`
  - Serialização com `__type__` para transportar subclasses via JSON

---

### Endpoint
- `POST /invoke`

### Formato da requisição

```json
{
  "requestId": 1,
  "objectReference": "CatalogoService",
  "methodId": "listar",
  "arguments": {
    "args": [],
    "kwargs": {}
  }
}