import json
import re

# Caminho do arquivo JSON
caminho_arquivo = r'data/diarios/2023-01-09-1-resumo-extracao.json'

# Extrai o mês e ano do nome do arquivo
match_data = re.match(r'.*(\d{4}-\d{2}).*', caminho_arquivo)
if match_data:
    mes_ano = match_data.group(1)
else:
    mes_ano = "Desconhecido"

# Lê o conteúdo do arquivo JSON
with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    dados_json = json.load(arquivo)

# Inicializa um dicionário para armazenar os valores por cidade
valores_por_cidade = {}

# Itera sobre os itens do JSON
for item_json in dados_json:
    try:
        # Converte a string JSON em um objeto Python (dicionário)
        data = json.loads(item_json)

        # Obtém o município de cada item
        municipio = data['municipio']

        # Obtém o texto associado a cada cidade
        texto = data['texto']

        # Inicializa uma variável para armazenar o valor total da cidade
        valor_total_cidade = 0.0

        # Procura por valores no formato "R$ X.XXX,XX" ou "R$ XX.XXX,XX" ou ...
        matches = re.finditer(r'R\$\s?(\d{1,3}(?:\.\d{3})*(?:,\d{1,2})?)', texto)
        for match in matches:
            valor_encontrado = match.group(1).replace('.', '').replace(',', '.')
            valor_float = float(valor_encontrado)

            # Soma o valor ao total da cidade
            valor_total_cidade += valor_float

        # Adiciona o valor total da cidade ao dicionário global
        valores_por_cidade[municipio] = valor_total_cidade

    except json.JSONDecodeError:
        # Ignora linhas que não são JSON válido
        pass

# Exibe os valores por cidade e o mês/ano
print(f"Mês/Ano: {mes_ano}")
for municipio, valor_total in valores_por_cidade.items():
    print(f"Município: {municipio}")
    print(f"Valor total: R$ {valor_total:,.2f}")
    print("=" * 50)
