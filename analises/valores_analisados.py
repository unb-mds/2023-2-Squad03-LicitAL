import pandas as pd
import zipfile

# Download do arquivo zip
url = "https://github.com/unb-mds/2023-2-Squad03/raw/main/valores_licitacoes.zip"
nome_arquivo = "valores_licitacoes.zip"
df_arquivo = "valores_licitacoes.json"

import urllib.request
urllib.request.urlretrieve(url, nome_arquivo)

# Descompactar o arquivo
with zipfile.ZipFile(nome_arquivo, 'r') as zip_ref:
    zip_ref.extractall()

# Ler o arquivo JSON resultante
df = pd.read_json(df_arquivo)

# Realizar as operações desejadas com o DataFrame
print(df.shape)
print(df.head())
print("\n## Total de municípios: " + str(df["municipio"].nunique()))


print("\n## Total de valores de licitações: " + str(sum(df["valores_licitacoes"].apply(len))))

print("\n## Total de Valores de Licitações por mês\n")
print(df.groupby(["ano", "mes"])["valores_licitacoes"].apply(lambda x: sum(map(len, x))).reset_index(name="count"))


media_valores_licitacoes = df.groupby(["ano", "mes"])["valores_licitacoes"].apply(
    lambda x: sum(map(len, x)) / len(x)).reset_index(name="media_valores_licitacoes")

print("\n## Média de Valores de Licitações por Município e Mês\n")
print(media_valores_licitacoes)


print("\n## Top 10 Municípios com maior gasto\n")
print(df.groupby(["municipio"])["cod"].count().sort_values(ascending=False).head(10))
