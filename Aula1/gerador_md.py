import os
import shutil
from cliente_tcp import gerar_tcp
from cliente_udp import gerar_udp

DIR_DESTINO = "/home/Zety/sd-2026-2/MD/"
os.makedirs(DIR_DESTINO, exist_ok=True)

print("Gerando 100 mensagens e logs TCP...")
tcp = gerar_tcp()

print("Gerando 100 mensagens e logs UDP...")
udp = gerar_udp()

caminho_md = os.path.join(DIR_DESTINO, "mensagens.md")

with open(caminho_md, "w", encoding="utf-8") as arquivo:
    arquivo.write("# Relatório de Logs: TCP e UDP (100 Mensagens)\n\n")
    
    arquivo.write("## TCP — 100 mensagens\n\n")
    for mensagem in tcp:
        arquivo.write(mensagem + "\n\n")
        
    arquivo.write("## UDP — 100 mensagens\n\n")
    for mensagem in udp:
        arquivo.write(mensagem + "\n\n")

# Copiar os arquivos de log gerados para o diretório de destino
for log_file in ["cliente_tcp.log", "cliente_udp.log"]:
    if os.path.exists(log_file):
        shutil.copy(log_file, os.path.join(DIR_DESTINO, log_file))

print()
print("================================")
print("CONCLUÍDO COM SUCESSO")
print("================================")
print(f"Diretório de destino: {DIR_DESTINO}")
print("TCP: 100 mensagens registradas")
print("UDP: 100 mensagens registradas")
print(f"Arquivo Markdown: {caminho_md}")
print("Arquivos de log TCP e UDP copiados para o diretório.")
print("================================")
