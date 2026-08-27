# Servidor multithread com múltiplos clientes

## 1. Objetivo

O objetivo deste trabalho foi criar um servidor capaz de atender vários clientes ao mesmo tempo. Para isso, usei sockets TCP e threads em Python, seguindo o conteúdo das Aulas 01, 02 e 03 da disciplina.

## 2. Relação com as aulas

Na Aula 01, foi apresentado o conceito de sistemas distribuídos. São vários computadores ou processos que trabalham pela rede e parecem funcionar como um único sistema. Também foi mostrado que a rede pode apresentar falhas e atrasos.

Na Aula 02, foram apresentados os sockets e o modelo cliente-servidor. O servidor fica ouvindo uma porta e o cliente se conecta para trocar mensagens. Neste trabalho, usei TCP, porque ele mantém uma conexão e garante a entrega das mensagens.

Na Aula 03, foi apresentado o problema de um servidor que atende um cliente por vez. Enquanto esse cliente está sendo atendido, os outros precisam esperar. A solução estudada foi criar uma thread para cada cliente. Assim, o servidor volta rapidamente para o `accept()` e consegue receber novas conexões.

## 3. Desenvolvimento

O arquivo principal foi chamado de `multithred.py`, conforme solicitado. Ele cria um socket TCP na porta 5000 e fica esperando conexões. Sempre que um cliente se conecta, o servidor cria uma nova thread para atender aquele cliente.

Cada thread recebe as mensagens e devolve a mesma mensagem para o cliente. Esse funcionamento é conhecido como servidor de eco. A opção `daemon=True` faz com que as threads sejam encerradas junto com o servidor.

Também foi criado o arquivo `carga.py`. Ele abre vários clientes usando threads, envia três mensagens para cada um e mede o tempo total e o tempo médio de atendimento.

## 4. Testes realizados

Os testes foram executados localmente, usando o endereço `127.0.0.1`, a porta 5000 e três mensagens por cliente. Todos os clientes receberam resposta do servidor.

| Tipo de servidor | Clientes | Mensagens por cliente | Tempo total | Tempo médio por cliente | Clientes concluídos |
|---|---:|---:|---:|---:|---:|
| Multithread | 10 | 3 | 0,0122 s | 0,0098 s | 10 |
| Multithread | 50 | 3 | 0,0355 s | 0,0205 s | 50 |
| Sequencial | 10 | 3 | 0,0131 s | 0,0103 s | 10 |
| Sequencial | 50 | 3 | 0,0269 s | 0,0188 s | 50 |

Como o teste foi feito no mesmo computador e as mensagens eram pequenas, os tempos ficaram muito próximos. Por isso, o resultado não mostra uma grande diferença de velocidade. Mesmo assim, o servidor multithread conseguiu atender os clientes sem deixar um cliente preso esperando o encerramento dos outros.

Em um caso real, com clientes mais lentos ou com tarefas que demorassem mais para serem processadas, a diferença seria mais perceptível. No servidor sequencial, um cliente lento pode bloquear o atendimento dos demais. No servidor multithread, cada cliente fica em sua própria thread, diminuindo esse problema.

## 5. Conclusão

O trabalho mostrou, na prática, como a concorrência pode melhorar o atendimento de um servidor. O servidor sequencial atende um cliente por vez, enquanto o servidor multithread cria uma thread para cada conexão e consegue atender vários clientes em andamento.

Também é importante tomar cuidado com dados compartilhados entre threads. Quando duas threads alteram a mesma variável ao mesmo tempo, pode ocorrer uma condição de corrida. Nessa situação, deve-se usar um `Lock` para proteger a parte crítica do código. No servidor deste trabalho, cada conexão foi tratada separadamente, sem a necessidade de compartilhar um contador entre os clientes.

Assim, o uso de threads é uma solução simples para permitir múltiplos acessos em um servidor de rede, principalmente quando o programa passa bastante tempo esperando mensagens dos clientes.

## Referências

[1] [Aula 01 — Abertura, diagnóstico e ambiente](https://howardroatti.github.io/sistemas-distribuidos-faesa/aulas/aula-01-abertura-diagnostico-ambiente.html)

[2] [Aula 02 — Modelos de arquitetura e sockets](https://howardroatti.github.io/sistemas-distribuidos-faesa/aulas/aula-02-modelos-arquitetura-sockets.html)

[3] [Aula 03 — Concorrência: um servidor para vários clientes](https://howardroatti.github.io/sistemas-distribuidos-faesa/aulas/aula-03-concorrencia-multiplos-clientes.html)
