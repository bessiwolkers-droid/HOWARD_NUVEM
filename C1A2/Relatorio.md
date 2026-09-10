# C1.A2 — Serviço de inferência distribuído

## 1. Objetivo

O objetivo deste trabalho foi disponibilizar a inferência de sentimento como um serviço distribuído, sem deixar o cliente esperando a resposta do modelo. A ideia é que quem envia o texto receba uma identificação na hora e possa consultar o resultado depois.

O trabalho partiu do kit da disciplina e reaproveita o classificador que já foi usado na Aula 06.

## 2. Organização dos arquivos

Os arquivos ficam na pasta `C1A2`:

- `modelo.py` — classificador de sentimento, o mesmo arquivo da Aula 06
- `fila.py` — funções para colocar tarefas na fila e guardar os resultados no Redis
- `api_rest.py` — a API que recebe os textos, de forma síncrona e assíncrona
- `worker.py` — processo que retira as tarefas da fila e executa as inferências
- `cliente_fila.py` — cliente de teste do caminho assíncrono
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

No terminal deixei uma mensagem com a identificação da tarefa, o tamanho do texto e o tempo da requisição. Isso ajuda a perceber que o tempo de resposta da rota assíncrona é bem menor que o da rota síncrona, porque ela não executa a inferência.

## 5. Consulta do resultado

Com o id devolvido pela rota `POST /predict`, o cliente acompanha o andamento pela rota `GET /resultado/{id}`.

Enquanto a tarefa ainda não foi processada, a resposta mostra o estado em que ela está:

```json
{
  "status": "na_fila"
}
```

Se a identificação não existir, a resposta é `404` em vez de devolver um corpo vazio com código `200`. Isso deixa claro para o cliente a diferença entre uma tarefa que ainda não terminou e uma identificação que nunca foi criada.

Essa rota também escreve uma mensagem no terminal com o estado devolvido, o que ajuda a acompanhar a tarefa mudando de situação sem precisar abrir o Redis.

## 6. Processo que executa as inferências

O arquivo `worker.py` é um programa separado da API. Ele carrega o modelo uma vez e entra em um laço chamando `proxima_tarefa()`, que fica bloqueado esperando aparecer item na fila.

Quando chega uma tarefa, o worker executa a previsão, marca o estado como `pronto`, guarda o tempo da inferência e grava tudo com `guardar_resultado()`. É essa gravação que faz a rota `GET /resultado/{id}` passar a devolver a resposta completa.

O caminho inteiro fica assim:

1. a API recebe o texto e coloca na fila, devolvendo o id na hora
2. o worker retira a tarefa da fila e executa a inferência
3. o worker grava o resultado
4. o cliente consulta o id e recebe o resultado pronto

Como a API e o worker são processos diferentes, cada um carrega o seu próprio modelo, mas sempre uma única vez na inicialização. Também é possível abrir mais de um worker no mesmo Redis, e nesse caso as tarefas se dividem entre eles, porque `proxima_tarefa()` remove o item da fila ao pegá-lo.

Os erros de uma tarefa são registrados no terminal e não derrubam o laço, então o worker continua atendendo as tarefas seguintes.

## 7. Como executar

Primeiro é preciso subir o Redis, porque a fila depende dele:

```bash
docker compose up -d
```

Depois instalar as dependências e iniciar a API:

```bash
pip install -r requirements.txt
uvicorn api_rest:app --reload --port 8000
```

Em outro terminal, dentro da mesma pasta, inicie o worker:

```bash
python3 worker.py
```

A documentação automática do FastAPI fica em `http://localhost:8000/docs`. Para testar o caminho assíncrono pelo terminal, usei o cliente:

```bash
python3 cliente_fila.py "o atendimento foi excelente e muito rapido"
```

Ele mostra o id devolvido na hora e, em seguida, o resultado depois que o worker termina.

## 8. Próximos passos

O caminho assíncrono está completo. Conferi que o mesmo texto recebe a mesma classificação pelas duas rotas, a síncrona e a assíncrona, e que o modelo é carregado uma única vez em cada processo.

Ainda faltam as demais tarefas do trabalho: a interface gRPC com o método de lote, o tratamento de erro com nova tentativa e fila de descarte, e a revisão final da documentação.

## Referência

Kit de partida do trabalho C1.A2. Disponível em: https://github.com/howardroatti/sd-2026-2-kit-c1a2
