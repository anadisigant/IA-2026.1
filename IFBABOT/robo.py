from chatterbot import ChatBot
import time

NOME_ROBO = "IFBA.Bot"
LIMIAR_ACEITACAO = 0.75

time.clock = time.time

def iniciar():
    iniciado, robo = False, None

    try:
        robo = ChatBot(NOME_ROBO, read_only=True)

        iniciado = True
    except Exception as e:
        print(f"erro iniciando robô: {e}")

    return iniciado, robo

def get_resposta(robo, mensagem):
    resposta = robo.get_response(mensagem.lower())

    return resposta.confidence, resposta.text

if __name__ == "__main__":
    iniciado, robo = iniciar()
    if iniciado:
        while True:
            mensagem = input("👤 ")

            confianca, resposta = get_resposta(robo, mensagem)
            if confianca >= LIMIAR_ACEITACAO:
                print(f"🤖 {resposta}, confiança = {confianca}")
            else:
                # enviar pergunta não respondida para o log

                print("🤖 não sei responder esta pergunta, por favor, pergunte outra coisa ou reformule sua pergunta")