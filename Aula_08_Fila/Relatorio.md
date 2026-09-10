# Aula 08 — Fila e processamento assíncrono

## 1. Objetivo

Nesta atividade comecei a montar o serviço de inferência do trabalho C1.A2. A ideia é disponibilizar a classificação de sentimento pela rede sem deixar o cliente esperando o modelo terminar.

O serviço reaproveita o classificador que já foi usado na Aula 06 e acrescenta uma fila, para que o pedido e o processamento fiquem separados.

## 2. Organização dos arquivos

Os arquivos ficam na pasta `Aula_08_Fila`:

- `modelo.py` — classificador de sentimento, o mesmo arquivo da Aula 06
- `fila.py` — funções para colocar tarefas na fila e guardar os resultados no Redis
- `api_rest.py` — a API que recebe os textos, de forma síncrona e assíncrona
- `docker-compose.yml` — sobe o Redis usado pela fila

O modelo é carregado uma única vez, quando a aplicação inicia. Assim ele não precisa ser preparado novamente a cada requisição, do mesmo jeito que foi feito na Aula 05.

## 3. Rotas da API

Por enquanto a API possui duas rotas.

A rota `GET /saude` serve para conferir se o serviço está no ar e se o modelo foi carregado.

A rota `POST /predict-sync` faz a previsão de forma síncrona, ou seja, o cliente espera o modelo terminar para receber a resposta. Ela recebe um JSON neste formato:

```json
{
  "texto": "o atendimento foi muito bom"
}
```

A resposta traz o texto original, o sentimento identificado, a confiança do modelo e o tempo gasto. Também coloquei uma verificação para impedir que um texto vazio seja processado.

## 4. Submissão assíncrona

A rota `POST /predict` recebe o mesmo JSON da rota síncrona, mas não espera a previsão terminar. Ela apenas coloca o texto na fila com a função `enfileirar()` e devolve a identificação da tarefa:

```json
{
  "id": "5f2c8e41-9b3d-4a7e-8c15-0d6a2b9f4e73",
  "status": "na_fila"
}
```

A resposta usa o código `202`, que indica que o pedido foi aceito mas ainda não foi concluído. Dessa forma o cliente não fica parado esperando o modelo, que é justamente o problema que a fila resolve.

A verificação de texto vazio continua valendo aqui, e nesse caso a resposta é `400`.

No terminal deixei uma mensagem com a identificação da tarefa, o tamanho do texto e o tempo da requisição. Assim dá para perceber que o tempo de resposta da rota assíncrona é bem menor que o da rota síncrona, porque ela não executa a inferência.

## 5. Como executar

Primeiro é preciso subir o Redis, porque a fila depende dele:

```bash
docker compose up -d
```

Depois instalar as dependências e iniciar a API:

```bash
pip install -r requirements.txt
uvicorn api_rest:app --reload --port 8000
```

A documentação automática do FastAPI fica em `http://localhost:8000/docs`. Por ela já é possível enviar um texto na rota `POST /predict` e ver a identificação sendo devolvida na hora.

## 6. Próximos passos

A tarefa já entra na fila, mas ainda não existe forma de consultar o resultado pela identificação recebida, nem um processo que retire as tarefas da fila e execute as inferências. São as próximas entregas.

## Referência

Kit de partida do trabalho C1.A2. Disponível em: https://github.com/howardroatti/sd-2026-2-kit-c1a2
