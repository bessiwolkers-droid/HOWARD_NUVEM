# Aula 04 — gRPC e geração dos stubs

Nesta atividade usei o arquivo `inferencia.proto` para definir o contrato do serviço gRPC. Nesse arquivo ficam os métodos do serviço e o formato das mensagens trocadas entre o cliente e o servidor.

Depois gerei os arquivos Python usando o comando abaixo:

```bash
python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. inferencia.proto
```

O comando criou `inferencia_pb2.py` e `inferencia_pb2_grpc.py`. O primeiro arquivo representa as mensagens do protocolo. O segundo contém as classes que ajudam a criar o cliente e o servidor gRPC.

Também deixei o script `gerar_stubs.sh` na pasta. Ele serve para repetir a geração caso o arquivo `.proto` seja alterado.

A conferência foi feita verificando se os arquivos gerados possuem sintaxe válida:

```bash
python3 -m py_compile inferencia_pb2.py inferencia_pb2_grpc.py
```

O resultado foi concluído sem erro. A parte mais importante que entendi nesta atividade é que o `.proto` funciona como um acordo entre as partes da comunicação. O cliente e o servidor precisam seguir esse mesmo contrato para conseguir trocar as mensagens corretamente.
