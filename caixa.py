"""A CAIXA: a rotina que recebe o pedido de qualquer canal e decide quem faz.
Pedido exato -> receita (sem cérebro). Pedido aberto -> cérebro, que pode pedir ferramentas."""
import json, os
import cerebro, ferramentas, receitas

MAX_RODADAS = 5


def atender(pedido, canal="terminal", mostrar=print):
    os.makedirs(ferramentas.PASTA, exist_ok=True)
    ferramentas.CANAL = canal
    mostrar(f"[canal {canal}] {pedido}")
    receita = receitas.procurar(pedido)
    if receita:                                        # é exato: a receita faz, o cérebro nem acorda
        mostrar(f"[receita {receita[0]}] sem cérebro")
        return receitas.executar(receita, receita[2])
    mostrar("[caixa] nenhuma receita serve: chamo o cérebro")
    lembrancas = "\n".join(f"- {m}" for m in ferramentas.memorias()) or "(nada ainda)"
    mostrar(f"[memória] {len(ferramentas.memorias())} fato(s) · [regras] regras.md")
    mensagens = [{"role": "system", "content": f"{open('regras.md').read()}\nO que você sabe do dono:\n{lembrancas}"},
                 {"role": "user", "content": pedido}]
    for rodada in range(MAX_RODADAS):
        msg = cerebro.pensar(mensagens, ferramentas.CARDAPIO)
        mensagens.append(msg)
        if not msg.get("tool_calls"):
            mostrar(f"[cérebro {cerebro.MODELO}] respondeu ({rodada + 1} rodada(s))")
            return msg.get("content", "")
        for chamada in msg["tool_calls"]:              # o cérebro pede, a caixa executa
            nome, args = chamada["function"]["name"], chamada["function"].get("arguments") or {}
            try:
                saida = ferramentas.TODAS[nome](**args)
            except Exception as erro:
                saida = f"erro: {erro}".replace(ferramentas.PASTA + os.sep, "")
            mostrar(f"[ferramenta {nome}] {json.dumps(args, ensure_ascii=False)} -> {' '.join(saida.split())[:70]}")
            mensagens.append({"role": "tool", "content": saida})
    return "Parei: cheguei ao limite de rodadas."
