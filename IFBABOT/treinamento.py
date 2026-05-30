from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json

NOME_ROBO = "IFBA.Bot"

import time
time.clock = time.time

ARQUIVOS_CONVERSAS = [
    "conversas/informacoes_basicas.json",
    "conversas/saudacoes.json",
    "conversas/sistemas_de_informacao.json"
]

def iniciar():
    iniciado, robo, treinador = False, None, None

    try:
        robo = ChatBot(NOME_ROBO)
        treinador = ListTrainer(robo)

        iniciado = True
    except Exception as e:
        print(f"erro iniciando robô: {e}")

    return iniciado, robo, treinador

def carregar_conversas():
    carregadas, conversas = False, []

    for arquivo_conversas in ARQUIVOS_CONVERSAS:
        try:
            with open(arquivo_conversas, "r", encoding="utf-8") as arquivo:
                treinamento = json.load(arquivo)
                conversas.append(treinamento["conversas"])

                arquivo.close()

            carregadas = True
        except Exception as e:
            print(f"erro carregando conversas: {e}")

    return carregadas, conversas

def treinar(treinador, conversas):
    for conversa in conversas:
        for mensagens_resposta in conversa:
            mensagens = mensagens_resposta["mensagens"]
            resposta = mensagens_resposta["resposta"]

            for mensagem in mensagens:
                print(f"treinando a mensagem '{mensagem}' + resposta '{resposta}'")
                treinador.train([mensagem.lower(), resposta])

if __name__ == "__main__":
    iniciado, robo, treinador = iniciar()
    if iniciado:
        carregadas, conversas = carregar_conversas()
        if carregadas:
            treinar(treinador, conversas)
