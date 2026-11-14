"""As FERRAMENTAS: o que o agente consegue fazer no mundo (aqui, com arquivos da pasta trabalho/)."""
import os

PASTA = os.path.realpath("trabalho")


def caminho(nome):
    return os.path.join(PASTA, nome)


def ler(nome):
    with open(caminho(nome)) as f:
        return f.read()


def escrever(nome, texto):
    with open(caminho(nome), "w") as f:
        f.write(texto)
    return f"gravado: {nome}"


def acrescentar(nome, texto):
    with open(caminho(nome), "a") as f:
        f.write(texto + "\n")
    return f"acrescentado em {nome}: {texto}"


TODAS = {"ler": ler, "escrever": escrever, "acrescentar": acrescentar}

# o cardápio que o cérebro lê para saber o que pode pedir
CARDAPIO = [
    {"type": "function", "function": {"name": "ler", "description": "Lê um arquivo da pasta de trabalho.",
     "parameters": {"type": "object", "properties": {"nome": {"type": "string"}}, "required": ["nome"]}}},
    {"type": "function", "function": {"name": "escrever", "description": "Grava um arquivo na pasta de trabalho.",
     "parameters": {"type": "object", "properties": {"nome": {"type": "string"}, "texto": {"type": "string"}},
                    "required": ["nome", "texto"]}}},
]
