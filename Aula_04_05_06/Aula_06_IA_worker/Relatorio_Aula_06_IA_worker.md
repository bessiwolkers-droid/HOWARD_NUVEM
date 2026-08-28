# Relatório da Aula 06 — IA como serviço distribuído

Nesta atividade, o modelo de sentimento foi usado como um serviço. A ideia não era treinar um modelo novo, mas fazer com que uma aplicação recebesse um texto, colocasse a tarefa em uma fila e deixasse outro processo realizar a inferência.

O arquivo `app/modelo.py` contém um classificador simples de sentimentos em português. A função `carregar_modelo()` verifica se o modelo já existe no disco. Se ainda não existir, ele é treinado e salvo. Depois disso, o modelo é carregado uma única vez pelo worker e pela API, evitando repetir esse trabalho em cada requisição.

A comunicação entre a API e o worker é feita pelo Redis. Quando a rota `POST /predict` recebe um texto, o arquivo `app/fila.py` gera um identificador, grava a tarefa na lista `tarefas` e salva inicialmente o status `na_fila`.

O worker, no arquivo `app/worker.py`, fica esperando novas tarefas. Quando encontra uma, chama `modelo.prever()` e salva o resultado no Redis usando o mesmo identificador. Dessa forma, o cliente consegue consultar o resultado depois pela rota `GET /resultado/{id}`.

Também foi colocado um tratamento para falhas. A tarefa possui o número de tentativas e pode ser processada até três vezes. Se ocorrer um erro antes desse limite, ela volta para a fila principal. Depois da terceira falha, a tarefa é enviada para a fila `tarefas:dead-letter` e o resultado fica registrado com status `erro`.

A parte da fila de descarte é importante porque uma tarefa que sempre falha não deve ficar sendo processada indefinidamente. Além de evitar esse ciclo, a fila dead-letter permite analisar depois quais tarefas deram problema.

O worker pode ser iniciado com:

```bash
python -m app.worker
```

Antes disso, o Redis deve estar funcionando:

```bash
docker compose up -d
```

A API REST é iniciada em outro terminal:

```bash
uvicorn app.api_rest:app --reload --port 8000
```

O fluxo completo fica assim: a API recebe o texto, cria a tarefa, o Redis guarda a tarefa, o worker realiza a inferência e salva o resultado, e o cliente consulta o identificador até o status mudar para `pronto`.

Foram adicionados logs no worker com o identificador da tarefa, o número da tentativa, o tamanho do texto e o tempo de processamento. Esses registros ajudam a entender o que aconteceu com cada tarefa e também facilitam a investigação de erros.

## Arquivos envolvidos

| Arquivo | Função |
|---|---|
| `app/modelo.py` | Carrega e executa o classificador de sentimentos. |
| `app/fila.py` | Controla as filas e os resultados no Redis. |
| `app/worker.py` | Consome as tarefas e executa as inferências. |
| `app/api_rest.py` | Recebe as requisições e permite consultar os resultados. |
| `docker-compose.yml` | Inicia o Redis. |

A principal ideia observada foi separar o recebimento do pedido do processamento mais demorado. Assim, a API não precisa ficar esperando o modelo terminar para responder ao cliente.
