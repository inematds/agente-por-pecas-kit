"""A CAIXA: a rotina que recebe o pedido de qualquer canal, chama o cérebro e devolve o resultado."""
import cerebro


def atender(pedido, canal="terminal", mostrar=print):
    mostrar(f"[canal {canal}] {pedido}")
    mensagens = [{"role": "system", "content": "Você é um assistente. Responda em português, curto."},
                 {"role": "user", "content": pedido}]
    resposta = cerebro.pensar(mensagens).get("content", "")
    mostrar(f"[cérebro {cerebro.MODELO}] respondeu")
    return resposta
