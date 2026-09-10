# C1.A2 — Serviço de inferência distribuído

## 1. Objetivo

O objetivo deste trabalho foi disponibilizar a inferência de sentimento como um serviço distribuído, sem deixar o cliente esperando a resposta do modelo. A ideia é que quem envia o texto receba uma identificação na hora e possa consultar o resultado depois.

O trabalho partiu do kit da disciplina e reaproveita o classificador que já foi usado na Aula 06.

## 2. Organização dos arquivos

Os arquivos ficam na pasta `C1A2`:

- `modelo.py` — classificador de sentimento, o mesmo arquivo da Aula 06
- `fila.py` — funções para colocar tarefas na fila e guardar os resultados no Redis
- `api_rest.py` — a API que recebe os textos
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

## 4. Como executar

Primeiro é preciso subir o Redis, porque a fila depende dele:

```bash
docker compose up -d
```

Depois instalar as dependências e iniciar a API:

```bash
pip install -r requirements.txt
uvicorn api_rest:app --reload --port 8000
```

A documentação automática do FastAPI fica em `http://localhost:8000/docs`.

## 5. Próximos passos

A parte síncrona funciona, mas ela ainda deixa o cliente esperando. As próximas entregas são a submissão assíncrona, a consulta do resultado pela identificação da tarefa e o processo separado que executa as inferências.

## Referência

Kit de partida do trabalho C1.A2. Disponível em: https://github.com/howardroatti/sd-2026-2-kit-c1a2
