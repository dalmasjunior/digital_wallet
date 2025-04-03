# Wallet API

## Descrição
A Wallet API é uma API REST para gerenciamento de carteiras digitais e transações financeiras. Ela permite que os usuários criem carteiras, realizem depósitos, transferências e consultem transações.

## Tecnologias Utilizadas
- Python 3
- Django Rest Framework (DRF)
- PostgreSQL
- Docker & Docker Compose

## Instalação

### Requisitos
- Docker e Docker Compose instalados
- Python 3 e virtualenv (se não estiver rodando via Docker)

### Rodando com Docker
1. Clone o repositório:
   ```sh
   git clone https://github.com/dalmasjunior/digital_wallet.git
   cd wallet-api
   ```
2. Construa e suba os containers:
   ```sh
   docker-compose up --build
   ```
5. A API estará disponível em `http://127.0.0.1:8000/`

### Rodando sem Docker
1. Crie um ambiente virtual e ative-o:
   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
2. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
3. Aplique as migrações:
   ```sh
   python manage.py migrate
   ```
4. Inicie o servidor:
   ```sh
   python manage.py runserver
   ```

## Endpoints Principais

### Criar um usuário
```http
POST /api/auth/register/
```
Body:
```json
{
  "username": "seu_usuario",
  "password": "sua_senha",
  "email": "email@example.com"
}
```

### Login
```http
POST /api/auth/login/
```

### Criar uma carteira
```http
POST /api/wallets/
```

### Depositar fundos em uma carteira
```http
POST /api/wallets/{id}/deposit/
```
Body:
```json
{
  "amount": 100.0
}
```

### Transferir fundos entre carteiras
```http
POST /api/wallets/{id}/transfer/
```
Body:
```json
{
  "to_wallet": 2,
  "amount": 50.0
}
```

### Listar transações de uma carteira
Para usar esse endpoint, faça uma requisição `GET` para `/api/wallets/{id}/transactions/` com parâmetros opcionais `start_date` e `end_date`.

**Exemplos de uso:**
- Listar todas as transações:
  ```http
  GET /api/wallets/1/transactions/
  ```
- Listar transações a partir de uma data:
  ```http
  GET /api/wallets/1/transactions/?start_date=2023-01-01
  ```
- Listar transações em um período:
  ```http
  GET /api/wallets/1/transactions/?start_date=2023-01-01&end_date=2023-12-31
  ```

## Testes
Para rodar os testes unitários:
```sh
pytest
```

## Autor
- [Paulo Dalmas](https://github.com/dalmasjunior)

