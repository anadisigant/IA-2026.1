from embedador import *

BICHOS_PARA_TESTES = [
    {
      "tipo": "cachorro",
      "imagem": "imagens/cachorro_teste.png"
    },
    {
        "tipo": "gato preto",
        "imagem": "imagens/gato_preto_teste.png"
    },
    {
        "tipo": "gato branco",
        "imagem": "imagens/gato_branco_teste.png" 
    }
]

def reconhecer(bicho, embedador, conexao_bd):
    reconhecido, tipo_bicho = False, None
    
    processada, embedding = processar(bicho["imagem"], embedador)
    if processada:
        try:
            colecao = conexao_bd.get_collection(NOME_BANCO)
            conversao = converter_embedding(embedding.embeddings[0].embedding)
            
            resultado = colecao.query(query_embeddings=[conversao], n_results=1)
            
            tipo_bicho = resultado["metadatas"][0][0]
            reconhecido = True
            
        except Exception as e:
            print(f"Erro ao processar a imagem: {e}")
    
    return reconhecido, tipo_bicho

if __name__ == "__main__":
    iniciado, embedador, conexao_bd = iniciar()
    if iniciado:
        for bicho in BICHOS_PARA_TESTES:
            reconhecido, tipo_reconhecido = reconhecer(bicho, embedador, conexao_bd)
            if reconhecido:
                print(f"Provável bicho reconhecido: {tipo_reconhecido}")
                print(f"Bicho esperado: {bicho['tipo']}")