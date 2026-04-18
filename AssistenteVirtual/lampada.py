def iniciar():
    print("Lâmpada iniciada")
    
def atuar(acao, objeto, local):
    if acao in ["ligar", "acender"] and objeto == "lâmpada":
        print(f"Ligando a lâmpada em {local}")
    elif acao in ["desligar", "apagar"] and objeto == "lâmpada":
        print(f"Desligando a lâmpada em {local}")
    else:
        print("Comando de lâmpada não reconhecido")