import pygame

MUSICA = "Beautiful.mp3"

def iniciar():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(MUSICA)
    
    print("Tocador iniciado")
    
def atuar(acao, objeto, local):
    if acao in ["tocar"] and objeto in {"musica", "som"}:
        print(f"Tocando {objeto} em {local}")
        pygame.mixer.music.play()
    elif acao in ["parar"] and objeto in {"musica", "som"}:
        print(f"Parando {objeto} em {local}")
        pygame.mixer.music.stop()
    else:
        print("Comando de tocador não reconhecido")