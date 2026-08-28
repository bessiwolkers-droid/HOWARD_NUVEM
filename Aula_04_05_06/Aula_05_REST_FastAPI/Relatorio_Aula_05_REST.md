# Relatório da Aula 05 — REST com FastAPI

Na atividade da Aula 05, a parte principal foi organizar uma interface REST para o serviço de inferência. A API foi feita com FastAPI e possui uma rota para verificar se o serviço está funcionando, uma rota síncrona e as rotas usadas no processamento assíncrono.

A rota `GET /saude` retorna o estado da aplicação e informa se o modelo já foi carregado. A rota `POST /predict-sync` executa a inferência na hora e devolve o resultado na própria resposta. Ela serve para comparar o funcionamento de uma chamada em que o cliente fica esperando o processamento terminar.

A rota mais importante do trabalho é `POST /predict`. Nela, o texto não é processado diretamente. Primeiro, ele é colocado na fila Redis e a API devolve um identificador com status HTTP `202`:

```json
{
  "id": "id-da-tarefa",
  "status": "na_fila"
}
```

Essa escolha evita que o cliente fique preso esperando a inferência. Para consultar o resultado depois, foi criada a rota `GET /resultado/{id}`. Enquanto o worker ainda não terminou, a resposta informa que a tarefa está na fila. Quando o processamento termina, a resposta contém o texto, o sentimento, a confiança e o tempo da inferência. Se o identificador não existir, a API devolve `404`.

Também foi feita uma validação para não aceitar texto vazio. Nesse caso, a API responde com erro `400`. O modelo é carregado no evento de inicialização da aplicação, portanto não é recriado a cada chamada da API.

Para testar a aplicação, é necessário instalar as dependências, iniciar o Redis e executar o servidor FastAPI:

```bash
pip install -r requirements.txt
docker compose up -d
uvicorn app.api_rest:app --reload --port 8000
```

A documentação automática fica disponível em `http://localhost:8000/docs`. Também é possível usar o cliente de exemplo:

```bash
python exemplos/cliente_rest.py "o atendimento foi ótimo"
```

Durante a implementação, adicionei logs com o identificador da tarefa, o tamanho do texto e o tempo gasto em cada requisição. Isso ajuda a acompanhar o caminho da requisição sem precisar entrar diretamente no Redis.

O ponto principal da atividade foi separar a entrada da tarefa do processamento. A API recebe o pedido rapidamente e o worker fica responsável por processar o texto e salvar o resultado.

## Arquivos envolvidos

| Arquivo | Função |
|---|---|
| `app/api_rest.py` | Define as rotas REST e valida as entradas. |
| `app/fila.py` | Coloca tarefas na fila e busca resultados no Redis. |
| `exemplos/cliente_rest.py` | Executa um teste da API. |
| `docker-compose.yml` | Inicia o Redis usado pela fila. |
