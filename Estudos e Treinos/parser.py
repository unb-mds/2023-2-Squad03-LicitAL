import re

def parse_expression(expression):
    # Remove espaços em branco
    expression = expression.replace(" ", "")

    # Usando expressões regulares para dividir a expressão em números e operadores
    tokens = re.findall(r'(\d+|\+|-)', expression)

    stack = []
    result = 0
    operator = '+'

    for token in tokens:
        if token.isdigit():
            num = int(token)
            if operator == '+':
                result += num
            elif operator == '-':
                result -= num
        else:
            operator = token

    return result

# Exemplo de uso do parser
expressao = "10 + 5 - 3"
resultado = parse_expression(expressao)
print("Resultado:", resultado)