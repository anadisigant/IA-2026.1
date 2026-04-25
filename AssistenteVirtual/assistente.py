from flask import Flask, Response, request, send_from_directory
from nltk import word_tokenize, corpus
from inicializador_modelo import *
from threading import Thread
from transcritor import *
import sounddevice as sd
import soundfile as sf
import numpy as np
import secrets
import json
import os

import lampada
import tocador

CONFIGURACAO = "config.json"

LINGUAGEM = "portuguese"
TEMPO_GRAVACAO = 5
CAMINHO_AUDIO_FALAS = "temp"

ATUADORES = [
    {
        "nome": "lâmpada",
        "iniciar": lampada.iniciar,
        "atuar": lampada.atuar
    },
    {
        "nome": "tocador",
        "iniciar": tocador.iniciar,
        "atuar": tocador.atuar
    }
]

# Limiar de energia mínima para considerar que houve fala
LIMIAR_SILENCIO = 0.01

def iniciar_assistente(dispositivo):
    iniciado, processador, modelo = iniciar_modelo(MODELO, dispositivo)

    palavras_de_parada = set(corpus.stopwords.words(LINGUAGEM))
    
    with open(CONFIGURACAO, "r", encoding="utf-8") as arquivo_configuracao:
        configuracoes = json.load(arquivo_configuracao)
        acoes = configuracoes["acoes"]

    for atuador in ATUADORES:
        atuador["iniciar"]()

    # Garante que o diretório temporário existe
    os.makedirs(CAMINHO_AUDIO_FALAS, exist_ok=True)
        
    return iniciado, processador, modelo, palavras_de_parada, acoes

def capturar_fala():
    print("\n🎤 Fale alguma coisa...")

    fala = sd.rec(int(TEMPO_GRAVACAO * TAXA_AMOSTRAGEM), samplerate=TAXA_AMOSTRAGEM, channels=1, dtype='float32')
    sd.wait()

    print("✅ Fala capturada!")

    return fala

def detectar_silencio(fala):
    """Verifica se o áudio capturado é apenas silêncio/ruído de fundo."""
    energia = np.sqrt(np.mean(fala ** 2))
    print(f"   Energia do áudio: {energia:.6f} (limiar: {LIMIAR_SILENCIO})")
    return energia < LIMIAR_SILENCIO

def gravar_fala(fala):
    gravado, arquivo = False, f"{CAMINHO_AUDIO_FALAS}/{secrets.token_hex(16).lower()}.wav"

    try:
        sf.write(arquivo, fala, TAXA_AMOSTRAGEM)
        
        gravado = True
    except Exception as e:
        print(f"❌ Erro ao gravar fala: {e}")

    return gravado, arquivo

def limpar_arquivo(arquivo):
    """Remove o arquivo temporário de áudio após processamento."""
    try:
        if os.path.exists(arquivo):
            os.remove(arquivo)
    except Exception as e:
        print(f"⚠️ Erro ao limpar arquivo temporário: {e}")

def processar_transcricao(transcricao, palavras_de_parada):
    tokens = word_tokenize(transcricao)
    
    comando = []
    for token in tokens:
        if token not in palavras_de_parada:
            comando.append(token)

    return comando

def validar_comando(comando, acoes):
    valido, acao, objeto, local = False, None, None, None

    if len(comando) >= 2:
        acao = comando[0]   # ligar, desligar
        objeto = comando[1] # lâmpada, ventilador
        local = comando[2] if len(comando) >= 3 else None  # sala, cozinha, quarto

        for acao_configurada in acoes:
            if acao == acao_configurada["nome"]: # ligar
                if objeto in acao_configurada["dispositivos"]:
                    valido = True

                    break

    return valido, acao, objeto, local

def executar_comando(acao, objeto, local):
    for atuador in ATUADORES:
        atuacao = Thread(target=atuador["atuar"], args=[acao, objeto, local])
        atuacao.start()

if __name__ == "__main__":
    dispositivo = "cuda:0" if torch.cuda.is_available() else "cpu"

    iniciado, processador, modelo, palavras_de_parada, acoes = iniciar_assistente(dispositivo)
    if iniciado:
        print("\n🤖 Assistente Virtual iniciado com sucesso!")
        print(f"   Dispositivo: {dispositivo}")
        print(f"   Tempo de gravação: {TEMPO_GRAVACAO}s")
        print("   Pressione Ctrl+C para encerrar.\n")

        while True:
            try:
                fala = capturar_fala()

                # Verifica se houve fala real (não apenas silêncio)
                if detectar_silencio(fala):
                    print("🔇 Nenhuma fala detectada (silêncio). Tentando novamente...\n")
                    continue

                gravado, arquivo = gravar_fala(fala)
                if gravado:
                    print("📝 Inicializando transcrição...")
                    
                    fala_tensor, _ = torchaudio.load(arquivo)
                    transcricao = transcrever(dispositivo, fala_tensor.squeeze(), modelo, processador)
                    transcricao = transcricao.lower().strip()
                    print(f"💬 Você disse: \"{transcricao}\"")

                    # Limpa o arquivo temporário
                    limpar_arquivo(arquivo)

                    # Ignora transcrições vazias
                    if not transcricao or len(transcricao) < 2:
                        print("⚠️ Transcrição vazia ou muito curta. Tentando novamente...\n")
                        continue

                    comando = processar_transcricao(transcricao, palavras_de_parada)
                    print(f"🔧 Comando processado: {comando}")
                    
                    valido, acao, objeto, local = validar_comando(comando, acoes)
                    if valido:
                        print(f"✅ Executando: {acao} {objeto} {local or ''}")
                        executar_comando(acao, objeto, local)
                    else:
                        print("❌ Comando inválido ou não reconhecido.")
                    
                    print()  # Linha em branco para separar iterações

            except KeyboardInterrupt:
                print("\n\n👋 Assistente encerrado pelo usuário.")
                break
            except Exception as e:
                print(f"❌ Erro inesperado: {e}\n")
    else:
        print("❌ Erro ao iniciar o assistente!")