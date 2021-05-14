# A clean-architecture with a REST api

### Quickstart
```shell
poetry install               # Install Python libs
make docker-compose-rebuild  # Build image and start containers 
make db-upgrade              # Run database migrations (create table, indexes, etc)
```

### Manual de Execução + Testes da API

Postman collection no diretório dos testes

- Criar uma conta

`POST /accounts`

- Operação de depósito

`POST /accounts/{account_id}/transactions` com value positivo

- Operação de Consulta de Saldo

`GET /accounts/{account_id}` com o id da conta

- Operação de Saque

`POST /accounts/{account_id}/transactions` com value negativo

- Bloqueio de Conta

`PATCH /accounts/{account_id}` com is_active = false

- Extrato de transações

`GET /accounts/{account_id}/transactions`

- Extrato por período

`GET /accounts/{account_id}/transactions?min_date=2020-01-01&max_date=2020-06-01`

### Testes unitários

`make test`

### Linter

`make lint`

### Documentação

FastAPI cria automaticamente <3

`GET /docs`

### Script de inserção de pessoas

Pela separacao de responsabilidades, é possível usar os interactors (uma vez que não há use-cases para pessoas)
para executar scripts de carga e descarga de dados

`python populate_people`

Se precisar carregar mais pessoas considere fazer bulk insert
