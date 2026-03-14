from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC #t do gp-t
import torchaudio
import torch

MODELO = "lgris/wav2vec2-large-xlsr-open-brazilian-portuguese-v2"
AUDIOS = {
    "../audios/audio1.wav"
    "../audios/audio2.wav"
}
TAXA_AMOSTRAGEM = 16_000

def iniciar(modelo, dispositivo = "gpu"):
    iniciado, processador, modelo = False, None, None
    
    try:
        processador = Wav2Vec2Processor.from_pretrained(modelo)
        modelo = Wav2Vec2ForCTC.from_pretrained(modelo).to(dispositivo)

        iniciado = True
    except Exception as e:
        print(f"Erro inicilizando o modelo: {str(e)}")

    return iniciado, processador, modelo

def carregar_fala(audio, fala):
    audio, amostragem = torchaudio.load(audio)
    # verifica se áudio tem mais de um canal (se é estereo)
    if audio.shape[0] > 1:
        #sendo estereo, converte para mono fazendo a média dos canais
        audio = torch.mean(audio, dim=0, keepdim=True) 
    #cria um adaptador de amostragem para garantir que o áudio esteja na taxa de amostragem esperada pelo modelo
    adaptador_amostragem = torchaudio.transforms.Resample(orig_freq=amostragem, new_freq=TAXA_AMOSTRAGEM)
    #degrada a qualidade do áudio para a taxa de amostragem esperada pelo modelo
    audio = adaptador_amostragem(audio)
    
    return audio.squeeze()

if __name__ == "__main__":
    iniciado, processador, modelo = iniciar(MODELO)
    if iniciado:
        print(f"O modelo {MODELO} iniciado com sucesso")

        for audio in AUDIOS:
            fala = carregar_fala(audio)