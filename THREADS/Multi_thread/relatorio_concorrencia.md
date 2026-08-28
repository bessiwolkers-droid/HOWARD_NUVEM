## 1. Objetivo

O objetivo desta atividade foi criar um servidor TCP capaz de atender vários clientes ao mesmo tempo. Para isso, foi utilizada uma thread separada para cada cliente conectado.

O trabalho foi baseado no conteúdo da Aula 03, que apresenta o uso de threads para melhorar o atendimento de múltiplas conexões em um servidor.

## 2. Funcionamento do servidor

No arquivo `servidor_multithread.py`, o servidor cria um socket TCP e fica esperando novas conexões na porta `5000`.

Quando um cliente se conecta, o servidor cria uma nova thread para atender essa conexão. Essa thread fica responsável por receber as mensagens do cliente e devolver os mesmos dados, funcionando como um servidor de eco.

Depois de criar a thread, o programa principal volta imediatamente para o comando `accept()`. Dessa forma, ele pode aceitar novos clientes sem precisar esperar o cliente anterior terminar.

A parte principal do código funciona da seguinte maneira:

```python
while True:
    conexao, endereco = servidor.accept()
    thread = threading.Thread(
        target=atender_cliente,
        args=(conexao, endereco),
        daemon=True,
    )
    thread.start()
```

A opção `daemon=True` faz com que as threads sejam encerradas quando o programa principal for finalizado.

## 3. Atendimento dos clientes

Cada thread executa a função `atender_cliente`. Dentro dessa função, o servidor fica recebendo dados com `recv()` e enviando a resposta com `sendall()`.

Como cada conexão possui sua própria thread, os clientes podem ser atendidos de forma independente. Se um cliente demorar para enviar uma mensagem, os outros não precisam esperar por ele.

## 4. Cliente de carga

O arquivo `carga.py` foi utilizado para testar o servidor. Ele cria várias threads de teste, sendo uma para cada cliente. Cada cliente abre uma conexão, envia três mensagens e espera receber cada mensagem de volta.

Ao final da execução, o programa mostra o tempo total do teste, o tempo médio de atendimento e a quantidade de clientes concluídos.

## 5. Como executar

Abra um terminal dentro da pasta do projeto e inicie o servidor com o comando:

```bash
python3 servidor_multithread.py
```

Depois, abra outro terminal na mesma pasta e execute o teste com 10 clientes:

```bash
python3 carga.py 10
```

Também é possível aumentar a quantidade de clientes para 50:

```bash
python3 carga.py 50
```

O servidor pode ser encerrado usando `Ctrl+C`.

## 6. Resultado esperado

Durante a execução, o terminal do servidor deve mostrar várias conexões sendo aceitas. Cada conexão fica associada a uma thread diferente.

As mensagens dos clientes podem aparecer intercaladas no terminal, porque as threads trabalham de forma concorrente. No final do teste, todos os clientes devem receber as respostas do servidor.

Como as mensagens são pequenas e o teste é executado localmente, o tempo pode ser baixo. O principal objetivo do teste é mostrar que o servidor consegue continuar aceitando clientes enquanto outras threads ainda estão trabalhando.

## 7. Condição de corrida e `Lock`

Quando várias threads alteram a mesma variável, pode acontecer uma condição de corrida. Isso ocorre quando uma thread lê um valor antes de outra terminar de atualizá-lo, fazendo com que alguma alteração seja perdida.

Para evitar esse problema, pode-se usar um `Lock` na parte crítica do código:

```python
with lock:
    total += 1
```

No servidor desta atividade, cada thread trabalha principalmente com sua própria conexão, e não existe um contador compartilhado entre todos os clientes. Por isso, não foi necessário utilizar `Lock` no servidor de eco.

Se fosse criado um contador global para registrar a quantidade de mensagens recebidas, esse contador deveria ser protegido por uma trava.

## 8. Conclusão

O servidor multi-thread consegue atender vários clientes de forma concorrente. Para cada conexão recebida, uma nova thread é criada, enquanto o programa principal continua esperando novos clientes.

Essa organização evita que um cliente lento bloqueie completamente os outros. Apesar de usar mais recursos do que um servidor com apenas uma thread, essa solução é mais adequada para aplicações que precisam receber várias conexões ao mesmo tempo.

Com o teste de carga, foi possível verificar que os clientes conseguem se conectar, enviar mensagens e receber as respostas do servidor simultaneamente.

## Referência

Aula 03 — Concorrência: um servidor para vários clientes. Disponível em: https://howardroatti.github.io/sistemas-distribuidos-faesa/aulas/aula-03-concorrencia-multiplos-clientes.html