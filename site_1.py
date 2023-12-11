import json
import os
import re

def cidades_json():
    # Certifique-se de que a pasta 'site' existe
    if not os.path.exists('site'):
        os.makedirs('site')

    # Carregar o JSON original
    with open('api.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Dicionário para armazenar os dados por município
    municipios = {}

    # Dicionário para armazenar os dados gerais
    geral = {
        "id": "geral",
        "detalhe": {}
    }

    # Iterar sobre cada item no JSON
    def remover_acentos_e_espacos(input_str):
        # Substituir espaços por hífen
        str_com_hifen = input_str.replace(" ", "-")
        # Utilizar expressões regulares para substituir acentos por suas letras correspondentes
        str_sem_acentos = re.sub(r'[áãâàä]', 'a', str_com_hifen, flags=re.IGNORECASE)
        str_sem_acentos = re.sub(r'[éêèë]', 'e', str_sem_acentos, flags=re.IGNORECASE)
        str_sem_acentos = re.sub(r'[íîìï]', 'i', str_sem_acentos, flags=re.IGNORECASE)
        str_sem_acentos = re.sub(r'[óõôòö]', 'o', str_sem_acentos, flags=re.IGNORECASE)
        str_sem_acentos = re.sub(r'[úûùü]', 'u', str_sem_acentos, flags=re.IGNORECASE)
        # Utilizar expressões regulares para remover outros caracteres especiais
        return re.sub(r'[^a-zA-Z0-9-]', '', str_sem_acentos)

    for item in data:
        # Obter o id do município (nome em minúsculas, sem espaços, sem acentos)
        id_municipio = remover_acentos_e_espacos(item["municipio"].lower())

        # Se o município ainda não está no dicionário, adicionar
        if id_municipio not in municipios:
            municipios[id_municipio] = {
                "id": id_municipio,
                "nome": item["municipio"],
                "detalhe": {},
                "resumo": {"valores_gastos": 0, "quantidade_licitacoes": 0, "qtd_dispensa": 0}  # Inicializar o resumo com valores_gastos como 0
            }

        # Adicionar os valores gastos ao município
        ano = str(item["ano"])
        if ano not in municipios[id_municipio]["detalhe"]:
            municipios[id_municipio]["detalhe"][ano] = {
                "resumo": {"valores_gastos": 0, "quantidade_licitacoes": 0, "qtd_dispensa": 0},  # Inicializar o resumo do ano com valores_gastos como 0
            }

        municipios[id_municipio]["detalhe"][str(item["ano"])][str(item["mes"])] = {
            "valores_gastos": item["valores_gastos"],
            "quantidade_licitacoes": item["quantidade_licitacoes"],
            "qtd_dispensa": item["qtd_dispensa"]
        }

        # Adicionar os valores gastos ao resumo do ano
        municipios[id_municipio]["detalhe"][ano]["resumo"]["valores_gastos"] += item["valores_gastos"]
        municipios[id_municipio]["detalhe"][ano]["resumo"]["quantidade_licitacoes"] += item["quantidade_licitacoes"]
        municipios[id_municipio]["detalhe"][ano]["resumo"]["qtd_dispensa"] += item["qtd_dispensa"]


        # Adicionar os valores gastos ao resumo
        municipios[id_municipio]["resumo"]["valores_gastos"] += item["valores_gastos"]
        municipios[id_municipio]["resumo"]["quantidade_licitacoes"] += item["quantidade_licitacoes"]
        municipios[id_municipio]["resumo"]["qtd_dispensa"] += item["qtd_dispensa"]

        # Adicionar os valores gastos ao resumo geral
        if ano not in geral["detalhe"]:
            geral["detalhe"][ano] = {
                "resumo": {"valores_gastos": 0, "quantidade_licitacoes": 0, "qtd_dispensa": 0}
            }
        geral["detalhe"][ano]["resumo"]["valores_gastos"] += item["valores_gastos"]
        geral["detalhe"][ano]["resumo"]["quantidade_licitacoes"] += item["quantidade_licitacoes"]
        geral["detalhe"][ano]["resumo"]["qtd_dispensa"] += item["qtd_dispensa"]

        # Adicionar os valores gastos de cada mês ao geral
        mes = str(item["mes"])
        if mes not in geral["detalhe"][ano]:
            geral["detalhe"][ano][mes] = {"valores_gastos": 0, "quantidade_licitacoes": 0, "qtd_dispensa": 0}
        geral["detalhe"][ano][mes]["valores_gastos"] += item["valores_gastos"]
        geral["detalhe"][ano][mes]["quantidade_licitacoes"] += item["quantidade_licitacoes"]
        geral["detalhe"][ano][mes]["qtd_dispensa"] += item["qtd_dispensa"]

        ranking_dispensas = {}

        # Iterar sobre os municípios para coletar dados para o ranking
        for id_municipio, municipio in municipios.items():
            # Adicione o município ao ranking com o número de dispensas de licitações
            ranking_dispensas[id_municipio] = {
                "nome": municipio["nome"],
                "num": municipio["resumo"]["qtd_dispensa"]
            }

        # Ordene o ranking com base no número de dispensas de licitações
        ranking_dispensas = dict(sorted(ranking_dispensas.items(), key=lambda x: x[1]["num"], reverse=True))

        # Limitar o ranking aos primeiros 5 e agrupar o restante como "Outros"
        ranking_limitado = {}
        outros_total = 0
        for idx, (municipio_id, dados) in enumerate(ranking_dispensas.items(), start=1):
            if idx <= 5:
                ranking_limitado[str(idx)] = {
                    "nome": dados["nome"],
                    "num": dados["num"]
                }

        # Adicionar o ranking ao arquivo geral
        geral["ranking_dispensas"] = ranking_limitado

    # Salvar cada município em um arquivo separado na pasta 'site'
    for id_municipio, municipio in municipios.items():
        with open(os.path.join('site', f'{id_municipio}.json'), 'w', encoding='utf-8') as f:
            json.dump(municipio, f, ensure_ascii=False, indent= 2)

    # Salvar os dados gerais em um arquivo na pasta 'site'
    with open(os.path.join('site', 'geral.json'), 'w', encoding='utf-8') as f:
        json.dump(geral, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    cidades_json()
