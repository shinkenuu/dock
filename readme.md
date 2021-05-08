# Uma API REST com código limpo

# Considerações

- DJANGO seria overkill, não é preciso Admin
- FastAPI cria automático a documentação pedida (sem contar que é async e MUITO leve)
- Poderia ser *BEEEEM* mais simples como meus outros repos. Aproveitei esse para aplicar um pouco de clean-code
- Não implementei Conta.tipoConta pois nao é usado pra nada

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

### Testes unitários

`make test`

### Documentação

FastAPI cria automaticamente <3

`GET /docs`

### Script de inserção de pessoas

Pela separacao de responsabilidades, é possível usar os interactors (ou os controllers)
para executar scripts de carga e descarga de dados

`python scripts/populate_people.py`

Se precisar carregar mais pessoas considere fazer bulk insert


### Dúvidas
No payload de contas devia ir apenas person_id ou um objeto?
Contas deveriam ser consideradas duplicadas se forem da mesma pessoa?
