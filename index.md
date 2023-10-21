# 💻 Visão Geral
O LicitAl é um projeto da disciplina de Métodos de Desenvolvimento de Software, que visa automatizar a coleta de informações de licitações de todos os municípios de Alagoas a partir dos Diários Oficiais, além de disponibilizar as informações de forma facilitada para qualquer cidadão. Esse projeto é inspirado no projeto [Exoonero](https://exoonero.org/sobre/), porém com foco em valores gastos com licitações.
	

# 💡 Ideia e Incentivo
O LicitAl é uma ferramenta essencial para quem estuda, trabalha ou está envolvido com a Universidade de Brasília. Com informações atualizadas e confiáveis sobre dados públicos e facilita o acesso a importantes informações.

# 🚀 Como executar o projeto
## 🛠 Tecnologias e Pré-Requisitos

<p align="center">
    <img src="https://img.shields.io/badge/python-%230095D5.svg?&style=for-the-badge&logo=python&logoColor=white"/>
</p>


<p align="center">
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>



## ✔️ Instalando e executando

### Coletando e extraindo conjuntos de diários

O docker precisa estar corretamente configurado e o daemon em execução (necessário para rodar o apache tika).

O primeiro passo consistem em:

1. Coletar os diários da [AMA]() usando o [querido diário]()
1. Extrair o texto dos diários usando apache tika
1. Segmentar o diário da AMA() em diversos diários municipais usando o script `extrair_diarios.py`.

Por exemplo, para coletar e processar os diários entre 01/06/2022 e 31/12/2022, basta executar o seguinte comando.


	START_DATE=2022-01-06 END_DATE=2022-12-31 ./coletador.sh


Vale notar que um mesmo dia pode ter mais de um diário, pois existem edições extras. Isso é tratado com a adição de um número depois da data 

Essa execução irá gerar um conjunto de arquivos no diretório `/data/diarios`. Listamos 2 tipos de arquivos:

- `-extraido.txt`: versão texto do diário da AMA;
- `-resumo-extracao.json`: resultado da segmentação do diário da AMA em diferentes diários municipais.

Após a coleta, transformação em texto e segmentação do diário em diários, o próximo passo é dividir cada diário municipal em atos (ou ações executivas). Além disso, o script também processa o texto dos atos, por exemplo, realizando a identificação de valores gastos com licitações.

O script `extrair_atos.sh` processa todos os arquivos `-resumo-extracao.json`. Ele extrairá os atos de todos os diários municipais segmentados.


	./extrair_atos.sh


A execução desse script gerará um arquivo `-atos.json` para cada resumo de extração.

### Gerando base de dados para análise

Após realizar a extração dos atos dos diários municipais, basta executar:


	python3 criar_dataset_atos.py


Esse script irá processar todos os arquivos `-atos.json` e gerar o arquivo `df.zip` contendo um resumo de todos os dados necessários para análise.

Os arquivos de análise podem ser encontrados no diretório `analise`.

## Disponível na Gitpage
https://unb-mds.github.io/squad03-r2/

## 👨‍💻 Desenvolvedores

<table>
	<tr>
		<td align="center"><a href="https://github.com/M4RINH0"><img src="https://github.com/M4RINH0.png?size=460" width="100px;" alt=""/><br /><sub><b>Douglas</b></sub></a><br /><a href="https://github.com/M4RINH0"></a></td>
        <td align="center"><a href="https://github.com/joycedio"><img src="https://github.com/joycedio.png?size=460" width="100px;" alt=""/><br /><sub><b>Joyce</b></sub></a><br /><a href="https://github.com/joycedio"></a></td>
		<td align="center"><a href="https://github.com/omascara2"><img src="https://github.com/omascara2.png?size=460" width="100px;" alt=""/><br /><sub><b>Marco</b></sub></a><br /><a href="https://github.com/omascara2"></a></td>
		<td align="center"><a href="https://github.com/Paxxaglia"><img src="https://github.com/Paxxaglia.png?size=460" width="100px;" alt=""/><br /><sub><b>Iago</b></sub></a><br /><a href="https://github.com/Paxxaglia"></a></td>
		<td align="center"><a href="https://github.com/PedroHenrique061"><img src="https://github.com/PedroHenrique061.png?size=460" width="100px;" alt=""/><br /><sub><b>Pedro Henrique </b></sub></a><br /><a href="https://github.com/PedroHenrique061"></a></td>
        <td align="center"><a href="https://github.com/Sooties"><img src="https://github.com/Sooties.png?size=460" width="100px;" alt=""/><br /><sub><b>Diego</b></sub></a><br /><a href="https://github.com/Sooties"></a></td>
	</tr>
</table>

## 📝 Licença
Este projeto está licenciado sob os termos da licença 
[MIT](./LICENSE).
