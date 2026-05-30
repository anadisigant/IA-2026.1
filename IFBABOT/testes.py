import unittest
from robo import *

class TesteSaudacoes(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.iniciado, cls.robo = iniciar()

    def testar_01_iniciado(self):
        self.assertTrue(self.iniciado)
        self.assertIsNotNone(self.robo)
        
    def testar_02_oi_ola(self):
        saudacoes = ["oi", "olá", "oi, tudo bem?", "como vai?", "olá, como vai?"]
        for saudacao in saudacoes:
            print(f"testando saudação: {saudacao}")
            
            
            confianca, resposta = get_resposta(self.robo, saudacao)
            self.assertEqual(confianca, 1.0)
            self.assertIn("Olá, sou o IFBABot, robô de atendimento do IFBA", resposta)
            
    def testar_03_bom_dia(self):
        saudacoes = ["Bom dia", "Oi, bom dia", "Olá, bom dia"]
        for saudacao in saudacoes:
            print(f"testando saudação: {saudacao}")
            
            
            confianca, resposta = get_resposta(self.robo, saudacao)
            self.assertEqual(confianca, 1.0)
            self.assertIn("Bom dia, sou o IFBABot, robô de atendimento do IFBA", resposta)
    
    def testar_04_variabilidades(self):
        saudacoes = ["ola", "Oi tudo bem", "tudo bem?"]
        for saudacao in saudacoes:
            print(f"testando saudação: {saudacao}")
            
            
            confianca, resposta = get_resposta(self.robo, saudacao)
            print(f"confianca = {confianca}, resposta = {resposta}")
            self.assertGreaterEqual(confianca, LIMIAR_ACEITACAO)
            self.assertIn("Olá, sou o IFBABot, robô de atendimento do IFBA", resposta)
    
    class TesteInformacoesBasicas(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
            cls.iniciado, cls.robo = iniciar()
        
        def testar_01_iniciado(self):
            self.assertTrue(self.iniciado)
            self.assertIsNotNone(self.robo)
            
        def testar_02_localizacao(self):
            perguntas = [
                "onde o ifba está localizado?",
                "onde fica o ifba?",
                "onde vocês funcionam?",
                "onde vocês estão localizados?"
            ]
            
            for pergunta in perguntas:
                print(f"testando pergunta: {pergunta}")
                
                confianca, resposta = get_resposta(self.robo, pergunta)
                self.assertEqual(confianca, 1.0)
                self.assertIsNotNone(resposta)
                self.assertIn("O IFBA fica localizado na Avenida Sérgio Vieira de Mello, 3150, Zabelê", resposta)

unittest.main()