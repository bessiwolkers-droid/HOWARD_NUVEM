##servidor multithread

## Arquivos

- `multithred.py`: servidor TCP que cria uma thread para cada cliente.
- `servidor_multicliente.py`: cópia com o nome usado nos slides da Aula 03.
- `carga.py`: abre vários clientes ao mesmo tempo e mede os tempos.
- `servidor_sequencial.py`: versão de comparação, baseada na Aula 02.
- `relatorio_concorrencia.md`: relatório com explicação e resultados.

## Como executar

Abra um terminal e inicie o servidor:

```bash
python multithread.py
```

Em outro terminal, execute o teste com 10 clientes:

```bash
python carga.py 10
```

Para testar com 50 clientes:

```bash
python carga.py 50
```