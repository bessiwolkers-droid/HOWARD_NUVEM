# Atividade: servidor single-thread

## 1. Objetivo

O objetivo desta atividade foi fazer duas versões de um servidor TCP de eco. A primeira versão atende um cliente por vez, usando apenas uma thread. A segunda cria uma thread para cada cliente conectado. Depois, foram feitos testes com vários clientes para observar a diferença entre os dois modos de funcionamento.

## 2. Servidor single-thread

No arquivo `servidor_sequencial.py`, o servidor aceita uma conexão e começa a atender aquele cliente. Ele recebe as mensagens com `recv()` e devolve os dados usando `sendall()`.

O problema é que o servidor só aceita outro cliente depois que o primeiro termina. Se o cliente ficar conectado por muito tempo ou demorar para enviar uma mensagem, os outros clientes precisam esperar.

## 3. Servidor multi-thread

No arquivo `servidor_multithread.py`, o servidor também aceita uma conexão, mas, nesse caso, cria uma nova thread para atender o cliente. Depois de criar a thread, o programa principal volta para o `accept()` e pode aceitar outra conexão.

Dessa forma, cada cliente é atendido separadamente. Se um cliente estiver lento, isso não impede que os outros continuem sendo atendidos. No código, as threads são criadas com `daemon=True`, para que sejam encerradas quando o servidor for fechado.

## 4. Teste de carga

O arquivo `carga.py` foi usado para testar os dois servidores. Ele cria vários clientes ao mesmo tempo. Cada cliente se conecta ao servidor, envia três mensagens e espera receber cada mensagem de volta.

No final do teste, o programa mostra o tempo total, o tempo médio de cada cliente e quantos clientes conseguiram terminar.

O mesmo teste foi usado nas duas versões para que a comparação fosse mais justa. Como o teste foi feito localmente e as mensagens são pequenas, os tempos podem ficar parecidos. Mesmo assim, é possível perceber a diferença no funcionamento: o servidor multi-thread consegue continuar atendendo outros clientes enquanto um deles ainda está conectado.

## 5. Como executar

Primeiro, é preciso abrir um terminal dentro da pasta do projeto. Para testar a versão single-thread, execute:

```bash
python3 servidor_sequencial.py
```

Depois, abra outro terminal e execute o cliente de carga:

```bash
python3 carga.py 10
```

O número `10` representa a quantidade de clientes do teste. Para usar 50 clientes, basta executar:

```bash
python3 carga.py 50
```

Depois de terminar o teste, o servidor pode ser encerrado com `Ctrl+C`. Para testar a versão multi-thread, execute:

```bash
python3 servidor_multithread.py
```

Em outro terminal, rode novamente:

```bash
python3 carga.py 10
```

É importante fechar o primeiro servidor antes de iniciar o outro, porque os dois usam a porta `5000`.

## 6. Comparação entre as versões

| Característica | Single-thread | Multi-thread |
|---|---|---|
| Forma de atendimento | Um cliente por vez | Uma thread para cada cliente |
| Cliente lento atrapalha os outros? | Sim | Normalmente não |
| Uso de memória | Menor | Maior, por causa das threads |
| Implementação | Mais simples | Um pouco mais complexa |
| Atendimento simultâneo | Não | Sim |

Na versão single-thread, as conexões são atendidas em sequência. Já na versão multi-thread, os atendimentos podem acontecer ao mesmo tempo e as mensagens podem aparecer misturadas no terminal.

Em um teste simples, a versão multi-thread não necessariamente apresenta um tempo total muito menor. Isso acontece porque as mensagens são pequenas e o servidor está sendo executado no mesmo computador que os clientes. O principal benefício aparece quando existem clientes lentos ou tarefas que demoram mais para serem processadas.

## 7. Condição de corrida e `Lock`

Quando várias threads modificam a mesma variável, pode acontecer uma condição de corrida. Isso ocorre porque uma thread pode ler um valor antes que outra thread termine de atualizá-lo, fazendo com que alguma alteração seja perdida.

Para evitar esse problema, pode-se usar um `Lock` e proteger a parte crítica do código:

```python
with lock:
    total += 1
```

Neste servidor, cada thread trabalha com sua própria conexão e não existe um contador compartilhado. Por isso, não foi necessário usar `Lock`. Se fosse criado um contador global para contar as mensagens de todos os clientes, seria necessário proteger esse contador.

## 8. Conclusão

A versão single-thread é mais simples, mas só consegue atender um cliente por vez. Por causa disso, um cliente lento pode fazer os demais esperarem.

A versão multi-thread resolve esse problema criando uma thread para cada conexão. Assim, vários clientes conseguem ser atendidos ao mesmo tempo. Em troca, o programa usa mais recursos e exige mais cuidado quando existem variáveis compartilhadas.

Com os testes realizados, foi possível observar na prática a diferença entre atender os clientes em sequência e atender cada um em uma thread separada.

## Referência

Aula 03 — Concorrência: um servidor para vários clientes. Disponível em: https://howardroatti.github.io/sistemas-distribuidos-faesa/aulas/aula-03-concorrencia-multiplos-clientes.html
