import json

# Seu JSON original
original_json = "api.json"

# Função para criar o JSON desejado para uma cidade específica
def criar_json_cidade(municipio):
    id_cidade = municipio["municipio"].lower().replace(" ", "-")
    nome_cidade = municipio["municipio"]
    
    json_cidade = {
        "id": id_cidade,
        "nome": nome_cidade,
        "detalhe": {}
    }

    # Adiciona cada ano e mês ao detalhe
    for dado in original_json:
        if dado["municipio"] == nome_cidade:
            ano = str(dado["ano"])
            mes = str(dado["mes"])
            if ano not in json_cidade["detalhe"]:
                json_cidade["detalhe"][ano] = {}
            json_cidade["detalhe"][ano][mes] = {
                "valor_gasto": dado["valores_gastos"]
            }

    # Adiciona o resumo total
    resumo_total = {
        "valor_gasto": 0
    }

    for ano, meses in json_cidade["detalhe"].items():
        for mes, detalhe in meses.items():
            resumo_total["valor_gasto"] += detalhe["valor_gasto"]

    json_cidade["detalhe"]["resumo"] = resumo_total

    return json_cidade

# Lista para armazenar os JSONs finais de cada cidade
jsons_cidades = []

# Dicionário para armazenar a soma total de valores para cada mês
soma_total_mes = {}

# Percorre cada cidade no JSON original
for cidade in original_json:
    json_cidade = criar_json_cidade(cidade)
    jsons_cidades.append(json_cidade)

    # Adiciona os valores ao dicionário de soma total
    for ano, meses in json_cidade["detalhe"].items():
        for mes, detalhe in meses.items():
            if mes not in soma_total_mes:
                soma_total_mes[mes] = {"valor_gasto": 0}
            soma_total_mes[mes]["valor_gasto"] += detalhe["valor_gasto"]

# Adiciona o resumo total geral
resumo_total_geral = {
    "valor_gasto": 0
}

for mes, detalhe in soma_total_mes.items():
    resumo_total_geral["valor_gasto"] += detalhe["valor_gasto"]

soma_total_mes["resumo"] = resumo_total_geral

# Salva os JSONs individuais em arquivos
for json_cidade in jsons_cidades:
    id_cidade = json_cidade["id"]
    with open(f"{id_cidade}.json", "w") as file:
        json.dump(json_cidade, file, indent=2)

# Salva o arquivo geral
with open("geral.json", "w") as file:
    json.dump(soma_total_mes, file, indent=2)
