operacao = str(input("Digite a operação que deseja realizar (soma, subtração, multiplicação ou divisão): ").upper())
num1 = int(input("Digite o 1º número: "))
num2 = int(input("Digite o 2º número: "))

soma = num1 + num2
subtracao = num1 - num2
multiplicacao = num1 * num2
divisao = num1 / num2

if operacao == "SOMA":
    print("A soma dos números é:", soma)
elif operacao == "SUBTRAÇÃO":
    print("A subtração dos números é:", subtracao)
elif operacao == "MULTIPLICAÇÃO":
    print("A multiplicação dos números é:", multiplicacao)
elif operacao == "DIVISÃO":
    print("A divisão dos números é ", divisao)