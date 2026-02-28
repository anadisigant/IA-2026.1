def somar(a, b):
    resultado = a + b
    return resultado

def somar_multiplicar(numero_a, numero_b):
    soma = numero_a + numero_b
    multiplicacao = numero_a * numero_b
    return soma, multiplicacao

resultado = somar(3, 20)
print("O resultado da soma é", resultado)

soma, multiplicacao = somar_multiplicar(39, 2)
print("Resultado da soma é", soma)
print("Resultado da multiplicação é", multiplicacao)

_, multiplicacao = somar_multiplicar(39, 2)
print(f"Resultado da multiplicação é: {multiplicacao}")

def subtrair(a, b):
    subtracao = a - b
    return subtracao 