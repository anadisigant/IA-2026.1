CADASTRO = {
    "descricao": "cadastro de pessoas",
    "autor": "Ana Disigant",
    "pessoas": [
        {
            "nome": "João da Silva",
            "profissao": "médico",
            "idade": 40,
        },
        {
            "nome": "Maria Oliveira",
            "profissao": "engenheira",
            "idade": 35,
        },
        {
            "nome": "Carlos Santos",
            "profissao": "professor",
            "idade": 50,
        }
    ]
}

if __name__ == "__main__":
    print(f"Descrição do cadastro: {CADASTRO['descricao']}")
    print(f"Autor do cadastro: {CADASTRO['autor']}")

    for pessoa in CADASTRO["pessoas"]:
        print(f"{pessoa['nome']} está cadastrado(a).")

    CADASTRO["versao"] = "1.0"
    print(f"Dicionário completo: {CADASTRO}")