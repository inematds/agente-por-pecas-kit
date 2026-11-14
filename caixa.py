"""A CAIXA: a rotina que recebe o pedido de qualquer canal e decide quem faz.
Pedido exato -> receita (sem cérebro). Pedido aberto -> cérebro, que pode pedir ferramentas."""
import json, os
import cerebro, ferramentas, receitas

MAX_RODADAS = 5


def atender(pedido, canal="terminal", mostrar=print):
    os.makedirs(ferramentas.PASTA, exist_ok=True)
    mostrar(f"[canal {canal}] {pedido}")
    receita = receitas.procurar(pedido)
    if receita:                                        # é exato: a receita faz, o cérebro nem acorda
        mostrar(f"[receita {receita[0]}] sem cérebro")
        return receitas.executar(receita, receita[2])
    mostrar("[caixa] nenhuma receita serve: chamo o cérebro")
    mensagens = [{"role": "system", "content": "Você é um assistente. Responda em português, curto. "
                  "Use as ferramentas para ler e gravar arquivos da pasta de trabalho."},
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
                saida = f"erro: {erro}"
            mostrar(f"[ferramenta {nome}] {json.dumps(args, ensure_ascii=False)} -> {' '.join(saida.split())[:70]}")
            mensagens.append({"role": "tool", "content": saida})
    return "Parei: cheguei ao limite de rodadas."
