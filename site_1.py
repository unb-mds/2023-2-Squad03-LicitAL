import json
import os


# Certifique-se de que a pasta 'site' existe
if not os.path.exists('site'):
    os.makedirs('site')

# Carregar o JSON original
with open('api.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Dicionário para armazenar os dados por município
municipios = {}

# Iterar sobre cada item no JSON
for item in data:
    # Obter o id do município (nome em minúsculas e sem espaços)
    id_municipio = item["municipio"].lower().replace(" ", "-")

    # Se o município ainda não está no dicionário, adicionar
    if id_municipio not in municipios:
        municipios[id_municipio] = {
            "id": id_municipio,
            "nome": item["municipio"],
            "detalhe": {},
            "resumo": {"valores_gastos": 0}  # Inicializar o resumo com valores_gastos como 0
        }

    # Adicionar os valores gastos ao município
    if str(item["ano"]) not in municipios[id_municipio]["detalhe"]:
        municipios[id_municipio]["detalhe"][str(item["ano"])] = {}

    municipios[id_municipio]["detalhe"][str(item["ano"])][str(item["mes"])] = {
        "valores_gastos": item["valores_gastos"]
    }

    # Adicionar os valores gastos ao resumo
    municipios[id_municipio]["resumo"]["valores_gastos"] += item["valores_gastos"]

# Salvar cada município em um arquivo separado na pasta 'site'
for id_municipio, municipio in municipios.items():
    with open(os.path.join('site', f'{id_municipio}.json'), 'w', encoding='utf-8') as f:
        json.dump(municipio, f, ensure_ascii=False, indent= 2)