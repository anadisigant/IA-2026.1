import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import ImageEmbedder, ImageEmbedderOptions, RunningMode

import chromadb as db

MODELO = "modelos/mobilenet_v3_large.tflite"

NOME_BANCO = "bichos"
CAMINHO_BANCO = "banco"

GATOS_BRANCOS = [
    "imagens/gato_branco1.png", 
    "imagens/gato_branco2.png"
]

GATOS_PRETOS = [
    "imagens/gato_preto1.png", 
    "imagens/gato_preto2.png"
]

CACHORROS = [
    "imagens/cachorro1.png", 
    "imagens/cachorro2.png"
]

def iniciar():
    iniciado, embedador, conexao_bd = False, None, None

    try:
        configuracoes = ImageEmbedderOptions(base_options=BaseOptions(model_asset_path=MODELO), running_mode=RunningMode.IMAGE)
        embedador = ImageEmbedder.create_from_options(configuracoes)

        conexao_bd = db.PersistentClient(path=CAMINHO_BANCO)

        iniciado = True
    except Exception as e:
        print(f"erro iniciando o embedador: {e}")

    return iniciado, embedador, conexao_bd

def processar(imagem, embedador):
    processada, embedding = False, None

    try:
        imagem = mp.Image.create_from_file(imagem)
        embedding = embedador.embed(imagem)

        processada = True
    except Exception as e:
        print(f"erro processando imagem: {e}")

    return processada, embedding

def processar_bichos(imagens, embedador):
    processados, embeddings = False, []

    for imagem in imagens:
        processada, embedding = processar(imagem, embedador)
        if processada:
            embeddings.append(embedding)

    processados = len(imagens) == len(embeddings)

    return processados, embeddings

def converter_embedding(embedding):
    conversao = []

    for valor in embedding:
        conversao.append(int(valor))

    return conversao

def gravar_embeddings(tipo_bicho, embeddings, conexao_bd):
    gravados = False

    try:
        colecao = conexao_bd.get_or_create_collection(NOME_BANCO)

        for id, embedding in enumerate(embeddings):
            conversao = converter_embedding(embedding.embeddings[0].embedding)

            colecao.add(embeddings=[conversao], metadatas=[{"bicho": tipo_bicho}], ids=[f"{tipo_bicho}_{str(id + 1)}"])

        gravados = True
    except Exception as e:
        print(f"erro gravando embeddings: {e}")

    return gravados

if __name__ == "__main__":
    iniciado, embedador, conexao_bd = iniciar()
    if iniciado:
        processados, embeddings = processar_bichos(GATOS_BRANCOS, embedador)
        if processados:
            gravados = gravar_embeddings("gatos brancos", embeddings, conexao_bd)
            if gravados:
                print("embeddings de gatos brancos gravados")

        processados, embeddings = processar_bichos(GATOS_PRETOS, embedador)
        if processados:
            gravados = gravar_embeddings("gatos pretos", embeddings, conexao_bd)
            if gravados:
                print("embeddings de gatos pretos gravados")

        processados, embeddings = processar_bichos(CACHORROS, embedador)
        if processados:
            gravados = gravar_embeddings("cachorros", embeddings, conexao_bd)
            if gravados:
                print("embeddings de cachorros gravados")                                