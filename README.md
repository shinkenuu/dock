# Uma API REST com código limpo

### Quickstart
```shell
poetry install               # Install Python libs
make docker-compose-rebuild  # Build image and start containers 
make db-upgrade              # Run database migrations (create table, indexes, etc)
```

# Considerações

- DJANGO seria overkill, não é preciso Admin
- FastAPI cria automático a documentação + async + MUITO leve
- Poderia ser *BEEEEM* mais simples como meus outros repos. Aproveitei esse para aplicar um pouco de clean-code
- Não implementei Conta.tipoConta pois nao é usado pra nada
- Foi a primeira vez que precisei fazer lock em table, deve haver maneira melhor de implementar. Peço esse feedback de vocês!!!

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

### Dúvidas

No payload de contas devia ir apenas person_id ou um objeto?
Contas deveriam ser consideradas duplicadas se forem da mesma pessoa?
Precisa paginar os extratos?