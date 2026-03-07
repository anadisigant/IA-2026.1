from nltk import word_tokenize, corpus
from nltk.corpus import floresta
from nltk.stem import RSLPStemmer

LINGUAGEM = 'portuguese'
TEXTO = "A verdadeira generosidade para com o futuro consiste em dar tudo ao presente." #Albert Camus

def iniciar():
    palavras_de_parada = set(corpus.stopwords.words(LINGUAGEM))

    classificacoes = {}
    for expressao, classificacao in floresta.tagged_words():
        classificacoes[expressao] = classificacao
    return palavras_de_parada, classificacoes

def tokenizar(texto):
    tokens = word_tokenize(texto, language=LINGUAGEM)
    return tokens

def imprimir(tokens):
    for token in tokens:
        print(token)

def eliminar_palavras_de_parada(tokens, palavras_de_parada):
    tokens_filtrados = []
    for token in tokens:
        if token.lower() not in palavras_de_parada:
            tokens_filtrados.append(token)
    return tokens_filtrados

def classificar_gramaticalmente(tokens, classificacoes):
    tokens_classificados = {}
    for token in tokens:
        classificacao = classificacoes[token]
        if classificacao == None:
            classificacao = "Token não classificado"
        tokens_classificados[token] = classificacao
    return tokens_classificados

def estemizar(tokens):
    raizes_de_tokens = {}
    estemizador = RSLPStemmer()
    for token in tokens:
        raiz = estemizador.stem(token)
        raizes_de_tokens[token] = raiz
    return raizes_de_tokens

if __name__ == "__main__":
    palavras_de_parada, classificacoes = iniciar()

    tokens = tokenizar(TEXTO)
    print(tokens)
    tokens = eliminar_palavras_de_parada(tokens, palavras_de_parada)
    # imprimir(tokens)
    tokens_classificados = classificar_gramaticalmente(tokens, classificacoes)
    # for token, classificacao in tokens.items():
    #    print(f"{token}: {classificacao}")
    print(tokens_classificados)
    raizes_de_tokens = estemizar(tokens)
    print(raizes_de_tokens)