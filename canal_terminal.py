"""CANAL terminal: o pedido chega pela linha de comando.  Uso: python3 canal_terminal.py "seu pedido" """
import sys
import caixa

print(caixa.atender(" ".join(sys.argv[1:]), canal="terminal"))
