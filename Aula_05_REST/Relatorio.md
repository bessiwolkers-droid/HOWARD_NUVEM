# Aula 05 — REST com FastAPI

Nesta atividade montei uma API REST usando FastAPI para receber um texto e devolver uma classificação de sentimento. A aplicação fica no arquivo `api_rest.py` e o modelo usado por ela fica em `modelo.py`.

A API possui a rota `GET /saude`, que serve para conferir se o serviço está funcionando e se o modelo foi carregado. A rota principal é `POST /prever`. Ela recebe um JSON neste formato:

```json
{
  "texto": "o atendimento foi muito bom"
}
```

Depois de receber o texto, a API chama o modelo e retorna o texto original, o sentimento identificado, o nível de confiança e o tempo gasto na previsão. Também coloquei uma verificação para impedir que uma entrada vazia seja processada.

Para iniciar o serviço, usei:

```bash
uvicorn api_rest:app --reload --port 8000
```

A documentação criada automaticamente pelo FastAPI fica em `http://localhost:8000/docs`. Nessa página é possível testar as rotas sem precisar escrever outro cliente.

O modelo é carregado quando a aplicação é iniciada. Assim, ele não precisa ser preparado novamente a cada requisição. Durante os testes, também deixei uma mensagem no terminal com o tamanho do texto e o tempo da previsão, para acompanhar o que está acontecendo.

A atividade ajudou a entender a diferença entre a lógica do modelo e a forma de disponibilizar essa lógica pela rede. O modelo faz a classificação, enquanto a API recebe os dados, valida a entrada e monta a resposta HTTP.
