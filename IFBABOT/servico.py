from robo import *
from flask import Flask
import json

iniciado, robo = iniciar()
servico = Flask(NOME_ROBO)

@servico.get("/")
def get_info():
    return json.dumps({
        "nome": NOME_ROBO,
        "descricao": "Robô de atendimento do IFBA, campus Vitória da Conquista"
    })
    
if __name__ == "__main__":
    servico.run(host="0.0.0.0", port=5000)