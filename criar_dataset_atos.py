import json
import glob
import os.path
import zipfile
import re

# Função para extrair valores de licitações do texto do ato
def extrair_valores(texto_ato):
    valores_licitacoes = re.findall(r"R\$\s?[\d\.,]+", texto_ato)  # Expressão regular para encontrar valores de licitações
    return valores_licitacoes

records = []
for path in glob.glob("data/diarios/*-atos.json"):
    with open(path) as json_file:
        diarios = json.load(json_file)
        for diario in diarios:
            diario = json.loads(diario)
            data_quebrada = diario["data_publicacao"].split("-")
            for ato in diario["atos"]:
                ato = json.loads(ato)

                valores_licitacoes = extrair_valores(ato["texto"])  # Extrai valores de licitações do texto do ato

                # Adicionando campos para facilitar a análise.
                record = {}
                record["municipio"] = diario["id"]
                record["cod"] = ato["cod"]
                record["valores_licitacoes"] = valores_licitacoes
                record["ano"] = int(data_quebrada[0])
                record["mes"] = int(data_quebrada[1])
                record["dia"] = int(data_quebrada[2])
                records.append(record)

with zipfile.ZipFile("valores_licitacoes.zip", "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
    df_json = json.dumps(records, indent=2, default=str, ensure_ascii=False)
    zip_file.writestr("valores_licitacoes.json", df_json)
    zip_file.testzip()
