# Trabalho 3 — Sebo (WS/API + Protocolo Request/Response)

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

## Endpoints da API

A API segue os padrões REST. Abaixo estão as principais rotas:

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| **GET** | `/produtos` | Lista todo o catálogo. |
| **GET** | `/produtos/{id}` | Busca os detalhes de um produto específico. |
| **POST** | `/produtos` | Cadastra um novo produto no estoque. |
| **POST** | `/produtos/{id}/venda` | Realiza a venda de um item (muda status para indisponível). |
| **POST** | `/transacoes/troca` | Realiza a troca entre dois produtos. |

---
