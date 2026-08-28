# Relatório da Aula 04 — gRPC e geração de stubs

Nesta parte do trabalho eu trabalhei com o arquivo `proto/inferencia.proto`. Ele funciona como o contrato do serviço gRPC, ou seja, é onde ficam definidos os métodos disponíveis e o formato das mensagens que serão enviadas entre cliente e servidor.

O contrato possui o método `Prever`, que recebe um texto, e o método `PreverLote`, que recebe uma lista de textos. Também estão definidas as mensagens `PedidoPrever`, `RespostaPrever`, `PedidoLote` e `RespostaLote`.

Para transformar esse contrato em código Python, usei o `grpc_tools.protoc` com o seguinte comando:

```bash
python3 -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/inferencia.proto
```

Depois da execução, foram criados os arquivos `inferencia_pb2.py` e `inferencia_pb2_grpc.py`. O primeiro possui as classes das mensagens do protocolo. O segundo possui as classes usadas para criar o cliente gRPC e registrar a implementação do servidor.

Também conferi o script `scripts/gerar_stubs.sh`, que executa o mesmo comando de forma mais prática. Os arquivos gerados não devem ser alterados manualmente. Se o arquivo `.proto` for modificado, o correto é executar a geração novamente.

No servidor, o método `PreverLote` foi implementado para percorrer os textos recebidos, chamar o modelo para cada um deles e montar uma resposta com vários resultados. O modelo é carregado uma vez quando o servidor é iniciado, em vez de ser carregado novamente a cada requisição.

Para validar o resultado, executei a geração dos stubs e depois verifiquei a sintaxe dos arquivos com:

```bash
python3 -m py_compile inferencia_pb2.py inferencia_pb2_grpc.py
```

A validação terminou sem erros. Assim, a atividade mostrou como o arquivo `.proto` é usado para gerar automaticamente a parte repetitiva da comunicação gRPC, deixando o servidor responsável apenas pela lógica do serviço.

## Arquivos envolvidos

| Arquivo | Função |
|---|---|
| `proto/inferencia.proto` | Define o contrato do serviço. |
| `inferencia_pb2.py` | Classes das mensagens gRPC. |
| `inferencia_pb2_grpc.py` | Classes do cliente e do servidor. |
| `app/servidor_grpc.py` | Implementação dos métodos do serviço. |
| `scripts/gerar_stubs.sh` | Script para gerar os arquivos Python. |
