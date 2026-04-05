from flask import Flask, Response, request, send_from_directory
from nltk import word_tokenize, corpus
from inicializador_modelo import *
from threading import Thread
from transcritor import *
import sounddevice as sd
import soundfile as sf
import secrets
import json
import os

LINGUAGEM = "portuguese"
TEMPO_GRAVACAO = 5
CAMINHO_AUDIO_FALAS = "IA-2026.1/AssistenteVirtual/temp"

def iniciar_assistente(dispositivo):
    iniciado, processador, modelo = iniciar_modelo(MODELO, dispositivo)

    palavras_de_parada = set(corpus.stopwords.words(LINGUAGEM))

    return iniciado, processador, modelo, palavras_de_parada

def capturar_fala():
    print("fale alguma coisa...")

    fala = sd.rec(int(TEMPO_GRAVACAO * TAXA_AMOSTRAGEM), samplerate=TAXA_AMOSTRAGEM, channels=1)
    sd.wait()

    print("fala capturada!")

    return fala

def gravar_fala(fala):
    gravado, arquivo = False, f"{CAMINHO_AUDIO_FALAS}/{secrets.token_hex(32).lower()}.wav"

    try:
        sf.write(arquivo, fala, TAXA_AMOSTRAGEM)
        gravado = True
    except Exception as e:
        print(f"Erro ao gravar fala: {e}")

    return gravado, arquivo

if __name__ == "__main__":
    dispositivo = "cuda:0" if torch.cuda_is_avaible() else "cpu"

    iniciado, processador, modelo, palavra_de_parada = iniciar_assistente(dispositivo)

    if iniciado:
        fala = capturar_fala()
        gravado, arquivo = gravar_fala(fala)
        if gravado:
            print("Inicializando transcrição...")
            fala, _ = torchaudio.load(arquivo)
            transcricao = transcrever(dispositivo, fala.squeeze(), modelo, processador)
            print(f"Você disse: {transcricao}")
    else:
        print("Erro ao iniciar o assistente!")