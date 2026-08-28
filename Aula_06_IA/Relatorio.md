# Aula 06 — IA como serviço

Nesta atividade usei o modelo de sentimento que já vinha preparado no projeto. A ideia foi disponibilizar a previsão como um serviço, sem precisar treinar um modelo novo para cada chamada.

O arquivo `modelo.py` possui a função `carregar_modelo()`. Na primeira execução, o modelo é treinado com a base de exemplos e salvo em disco. Nas execuções seguintes, ele é carregado do arquivo salvo. Dessa forma, o treinamento não acontece toda vez que alguém pede uma previsão.

Criei o arquivo `api_ia.py` para usar esse modelo. Ele carrega o modelo uma vez, recebe um texto pela função `prever()` e devolve o resultado da classificação. O resultado informa o texto analisado, o sentimento identificado, a confiança do modelo e o tempo gasto na operação.

Também foi feita uma verificação para não aceitar texto vazio. Se isso acontecer, o programa informa o erro em vez de tentar classificar uma entrada sem conteúdo.

Para testar diretamente pelo terminal, executei:

```bash
python3 api_ia.py
```

Depois basta digitar uma frase, como `o produto chegou rápido e gostei muito`. O programa mostra o resultado da previsão no terminal.

Essa atividade mostrou que o modelo pode ficar separado da aplicação que faz a requisição. Nesse caso, `modelo.py` concentra o classificador e `api_ia.py` faz a parte de serviço. Assim fica mais fácil trocar a forma de acesso ao modelo sem precisar alterar todo o código da classificação.
