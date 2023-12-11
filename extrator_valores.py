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

        # Lê o conteúdo do arquivo JSON de saída, se existir
        resultados_existente = []
        try:
            with open(resultado_json, 'r', encoding='utf-8') as arquivo_existente:
                resultados_existente = json.load(arquivo_existente)
        except FileNotFoundError:
            pass  # O arquivo ainda não existe, continuaremos com uma lista vazia

        # Lê o conteúdo do arquivo JSON de entrada
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            dados_json = json.load(arquivo)

        # Inicializa a lista de resultados para este arquivo
        resultados_arquivo = []

        # Itera sobre os itens do JSON
        for item_json in dados_json:
            # Converte a string JSON em um objeto Python (dicionário)
            data = json.loads(item_json)
            # Obtém o texto associado a cada cidade
            texto = data.get('texto', '')
            municipio = data['municipio']
            # Divide o texto em blocos usando "\nPublicado por:"
            blocos = re.split(r'\nPublicado por:', texto)

            # Itera sobre os blocos
            for bloco in blocos:
                # Verifica se o bloco contém palavras-chave relacionadas a licitações
                if any(palavra_chave in bloco for palavra_chave in ['EXTRATO DE CONTRATO']):
                    valor_total_cidade = 0.0
                    quantidade_licitacoes = 0
                    qtd_dispensa = 0  # Inicializa a contagem de "Dispensa de Licitação"
                    
                    valor_float = 0.0
                    matches = re.finditer(r'R\$\s?(\d{1,3}(?:\.\d{3})*(?:,\d{1,2})?)', bloco)
                    for match in matches:
                        valor_encontrado = match.group(1).replace('.', '').replace(',', '.')
                        valor_float = float(valor_encontrado)
                        valor_total_cidade += valor_float
                        quantidade_licitacoes += 1

                    # Verifica se o bloco contém "Dispensa de Licitação"
                    if 'Dispensa de Licitação' in bloco and valor_float > 50000:
                        qtd_dispensa += 1

                    resultado_existente = next((result for result in resultados_existente if result["municipio"] == municipio and result["ano"] == int(mes_ano[:4]) and result["mes"] == int(mes_ano[5:])), None)

                    if resultado_existente:
                        # Se já existe, atualiza o valor, a quantidade e a contagem de dispensa
                        resultado_existente["valores_gastos"] += valor_total_cidade
                        resultado_existente["quantidade_licitacoes"] += quantidade_licitacoes
                        resultado_existente["qtd_dispensa"] += qtd_dispensa
                    else:
                        # Adiciona um resultado à lista
                        resultados_existente.append({
                            "municipio": municipio,
                            "valores_gastos": valor_total_cidade,
                            "quantidade_licitacoes": quantidade_licitacoes,
                            "qtd_dispensa": qtd_dispensa,
                            "ano": int(mes_ano[:4]),
                            "mes": int(mes_ano[5:])
                        })

        # Adiciona os resultados deste arquivo aos resultados existentes
        resultados_existente.extend(resultados_arquivo)

        # Salva os resultados no arquivo JSON com formatação de duas casas decimais
        with open(resultado_json, 'w', encoding='utf-8') as output_file:
            json.dump(resultados_existente, output_file, ensure_ascii=False, indent=2, default=lambda x: round(x, 2))

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
