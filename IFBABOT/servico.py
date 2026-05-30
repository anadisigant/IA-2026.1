from flask import Flask, Response
from robo import *
import json

iniciado, robo = iniciar()
servico = Flask(NOME_ROBO)

@servico.get("/")
def get_info():
    return json.dumps({
        "nome": NOME_ROBO,
        "descricao": "Robô de atendimento do IFBA, campus Vitória da Conquista, Bahia"
    })

@servico.get("/resposta/<string:mensagem>")
def get_resposta(mensagem):
    print(f"recebida mensagem: {mensagem}")
    
    resposta = robo.get_response(mensagem)
    resposta = {
        "resposta": resposta.text,
        "confianca": resposta.confidence
    }

    return Response(json.dumps(resposta), status=200, mimetype="application/json")

if __name__ == "__main__":
    servico.run(host="0.0.0.0", port=7_000)