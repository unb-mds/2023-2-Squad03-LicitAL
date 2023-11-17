import sys
import json
import re

def extrair_valores(caminho_arquivo, resultado_json):
    try:
        # Extrai o mês e ano do nome do arquivo
        match_data = re.match(r'.*(\d{4}-\d{2}).*', caminho_arquivo)
        if match_data:
            mes_ano = match_data.group(1)
        else:
            mes_ano = "Desconhecido"

        # Lê o conteúdo do arquivo JSON
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            dados_json = json.load(arquivo)

        # Inicializa uma lista para armazenar os resultados
        resultados = []

        # Itera sobre os itens do JSON
        for item_json in dados_json:
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

            # Adiciona os resultados à lista
            resultados.append({
                "municipio": municipio,
                "valores_gastos": valor_total_cidade,
                "ano": int(mes_ano[:4]),
                "mes": int(mes_ano[5:])
            })

        # Salva os resultados no arquivo JSON
        with open(resultado_json, 'w', encoding='utf-8') as output_file:
            json.dump(resultados, output_file, ensure_ascii=False, indent=2)

    except json.JSONDecodeError:
        # Ignora linhas que não são JSON válido
        pass

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python extrator_valores.py <caminho_arquivo> <resultado_json>")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]
    resultado_json = sys.argv[2]
    extrair_valores(caminho_arquivo, resultado_json)
