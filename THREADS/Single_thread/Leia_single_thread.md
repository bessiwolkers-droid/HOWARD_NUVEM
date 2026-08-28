# Atividade single-thread

Esta pasta contém a implementação sequencial do servidor TCP de eco.

## Arquivos

- `servidor_sequencial.py`: servidor que atende um cliente por vez.
- `carga.py`: cria vários clientes concorrentes para o teste.
- `relatorio_concorrencia.md`: relatório explicativo da atividade.

## Execução

No primeiro terminal:

```bash
python3 servidor_sequencial.py
```

No segundo terminal:

```bash
python3 carga.py 10
```

Também é possível testar com 50 clientes usando `python3 carga.py 50`.

## Comportamento esperado

O servidor somente aceita o próximo cliente depois que termina o atendimento do cliente atual. Portanto, um cliente lento ou que permaneça conectado pode fazer os demais aguardarem.
