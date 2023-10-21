---
excerpt: ""
---

Este documento estará repleto de dados que sustentarão o propósito, o contexto e a visão geral do produto, permitindo assim o entendimento do escopo do projeto.
Assim, será explicado o problema evidenciado, a oportunidade encontrada, a descrição dos principais envolvidos, uma possível solução, suas principais funcionalidades e seus requisitos, para assim obter uma melhor compreensão do escopo e diminuir os riscos.


## Histórico de versões

| Data | Versão | Descrição | Autor(es) |
| :--: | :----: | :-------: | :-------: |
|05/05/2023|0.1|Criação da primeira versão|[Arthur Gabriel](https://github.com/ArthurGabrieel)|
|06/05/2023|0.2|Atualizações na Organização da Equipe|[Thiago Freitas](https://github.com/thiagorfreitas)|


## **1. Introdução**

### 1.1 Finalidade

  Este documento tem como objetivo demonstrar as características do desenvolvimento da aplicação em questão. Além disso, visa auxiliar no contexto em que a ferramenta se aplica.
  O objetivo deste artigo será definir o problema, os perfis das partes interessadas e do usuário, o campo de negócio no qual a iniciativa será inserida, além de requisitos, recursos e especificações do sistema em pauta.


### 1.2 Escopo

  Esse projeto tem como público-alvo os alunos da Universidade de Brasília que desejam ter informações atualizadas e precisas sobre seus direitos e o que fazer em situações atipicas, além de dicas sobre como lidar com situações comuns no ambiente universitário, assim solucionando diversas dúvidas que os estudantes possam vir a ter durante a graduação.


### 1.4 Definições, Acrônimos e Abreviações

  Estarão listadas neste tópico definições, acrônimos e abreviações para garantir uma maior proximidade para com o leitor e o público interessado no projeto.

| Sigla/Termo/Acrônimo | Definição                              |
| :------------------- | :------------------------------------- |
| MDS                  | Métodos de Desenvolvimento de Software |
| FGA                  | Faculdade do Gama                      |
| UNB                  | Universidade de Brasília               |

### 1.5 Referências

Documento de Visão: A estrutura de tópicos do documento de visão. IBM. Disponível em: https://www.ibm.com/docs/pt-br/elm/6.0.5?topic=requirements-vision-document. Acesso em: 05 de maio de 2023;

Documento de Visão. kalkuli. Disponível em: https://fga-eps-mds.github.io/2018.2-Kalkuli/docs/docVisao. Acesso em: 05 de maio de 2023;

Documento de Visão. Acacia. Disponível em: https://fga-eps-mds.github.io/2019.2-Acacia/#/vision_document?id=_5-recursos-do-produto. Acesso em: 05 de maio de 2023;

Documento de Visão. Aix. Disponível em: https://fga-eps-mds.github.io/2019.1-Aix/projeto/2019/03/29/documento-de-visao/. Acesso em: 05 de maio de 2023;

### 1.6 Visão Geral

  Desta forma, a ideia principal deste documento de visão é fornecer de maneira objetiva e organizada os assuntos que tangem à problemática inicial.
  As informações serão organizadas em tópicos referentes aos seguintes temas, como modelos de exemplo: o detalhamento dos perfis interessados, as funcionalidades principais da ferramenta a ser produzida bem como características técnicas do produto.


## **2. Posicionamento**

### 2.1 Oportunidade de negócios

  Com o aumento da complexidade das normas e regulamentações acadêmicas, muitos estudantes enfrentam dificuldades para entender seus direitos e deveres dentro da universidade. Além disso, a falta de clareza e de informações confiáveis pode prejudicar a comunicação entre a instituição e os alunos.
  Nesse contexto, o projeto visa facilitar o acesso à informação e ajudar os estudantes a compreender melhor seus direitos e obrigações na universidade. Por meio de uma interface intuitiva e de fácil uso, o aplicativo oferecerá uma vasta gama de informações atualizadas e confiáveis, abrangendo desde a estrutura administrativa da instituição até os direitos e deveres dos alunos em relação a questões como matrícula, bolsas e assistência estudantil.
  
### 2.2 Descrição do problema

| O problema é                                                                                  | que afeta       | cujo impacto é                                                                                                                         | uma boa solução seria                                                    |
| --------------------------------------------------------------------------------------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Dificuldade para encontrar informações essenciais para os discentes.  | Estudantes da UNB.| A falta de informações básicas.   | Ofertar informações atualizadas e para os discentes de modo simples e claro. |

### 2.3 Descrição de Posição do Produto

  Como um guia de referência para estudantes universitários, o aplicativo tem como objetivo fornecer informações claras e acessíveis sobre os direitos e benefícios dos alunos dentro da instituição. Com uma interface fácil de usar, o aplicativo ajuda a evitar a confusão e o desconhecimento sobre os diversos aspectos da vida acadêmica, como processos administrativos, regulamentos e prazos. O Guia UnB busca ser um recurso confiável para estudantes que precisam de respostas rápidas e precisas para suas dúvidas e preocupações, permitindo que se concentrem em seus estudos e objetivos acadêmicos.


| Para    | que                                                                                                                           | o produto       | que                                                | diferente de | nosso produto                                             |
| ------- | ----------------------------------------------------------------------------------------------------------------------------- | --------------- | -------------------------------------------------- | ------------ | --------------------------------------------------------- |
| Pessoas físicas | tem dificuldade em encontrar informações verdadeiras. | é um aplicativo para evitar a desinformação. | auxilia na redução das principais questões. |site UNB que apresenta dados de forma pouco intuitiva.  | mostra informações de forma clara e intuitiva.|

## **3. Descrição dos Envolvidos e dos Usuários**

### 3.1 Resumo dos Envolvidos

| Nome                          | Descrição                                                            | Responsabilidade                                                                                                                        |
| :---------------------------- | :------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| Equipe de Desenvolvimento     | Estudantes do curso de Engenharia de Software das disciplina de MDS | Contribuir ativamente com o desenvolvimento e implementação do software citado neste documento                                          |
| Equipe de Gestão do Projeto   | Estudantes do curso de Engenharia de Software das disciplinas de MDS | Gerenciar tempo, escopo, riscos, tomadas de decisões para garantir a viabilidade do projeto e garantir a aplicação dos princípios ágeis |
| Equipe de avaliação e suporte | Professor e monitores da disciplina de MDS                     | Auxiliar a equipe ao longo do desenvolvimento do projeto                                                                                |

### 3.2 Resumo dos Usuários

| Nome            | Descrição                                                               | Responsabilidade                                                                             |
| :-------------- | :---------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- |
| Pessoas físicas | Pessoas que querem informações sobre UNB de forma clara e intuitiva. | Utilizar o sistema e sufruir de suas funcionalidades |

### 3.3 Ambiente do Usuário

Os usuários poderão utilizar o aplicativo baixando ele na loja de aplicativos do celular.

### 3.4 Perfis dos Envolvidos

#### 3.4.1 Equipe avaliação e suporte

| Representantes    | Descrição                                                     | Tipo                                     | Responsabilidades                                                                                                                                                                               | Critério de sucesso                                                                                                             | Envolvimento |
| ----------------- | ------------------------------------------------------------- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| Profa. Carla | Equipe responsável pela avaliação e direcionamento do projeto | Professora e coach do grupo da disciplina | Direcionar e dar suporte a equipe de desenvolvimento e gestão, na disciplina MDS, quanto ao desenvolvimento do projeto | A entrega do projeto juntamente com uma documentação coerente estabelecida, a partir das orientações dadas ao longo do semestre | Alto         |
| Erick Levy | Equipe responsável pela avaliação e direcionamento do projeto | Monitor do grupo da disciplina | Direcionar e dar suporte a equipe de desenvolvimento e gestão, na disciplina MDS, quanto ao desenvolvimento do projeto | A entrega do projeto juntamente com uma documentação coerente estabelecida, a partir das orientações dadas ao longo do semestre | Alto         |


#### 3.4.2 Equipe de Desenvolvimento e Gestão do Projeto

| Papel  |  Descrição  |
| ----- | -------------------- |
| Scrum Master | [Thiago Freitas](https://github.com/thiagorfreitas) |
| Product Owner | [Lucas Avelar](https://github.com/LucasAvelar2711) |
| Arquiteto de Software | [Arthur Gabriel](https://github.com/ArthurGabrieel)|
| Desenvolvedor | [Alexandre Beck](https://github.com/zzzBECK), [Igor Ribeiro](https://github.com/igor-ribeir0) e [Genilson Silva](https://github.com/GenilsonJrs)|

### 3.5 Perfis dos Usuários

| Representante            | Descrição                                                               | Tipo                                                               | Responsabilidade                                                                             | Critério de sucesso                                                                             | Envolvimento                                                                             |
| :-------------- | :---------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- |
| Discentes da UNB interessadas por informações | Pessoas que querem informações sobre UNB de forma clara e intuitiva. |  Usuários desinformados  | Além de utilizar o programa e usufruir de suas funcionalidades, o usuário deve alertar sobre possíveis falhas ou informações faltantes | Circulação de informações e o reconhecimento do auxílio do aplicativo | Discentes da UNB interessadas por informações | Médio |

#### **3.6 Principais Necessidades dos Usuários ou dos Envolvidos**

##### 3.6.1 Necessidades dos envolvidos

| Necessidade            | Prioridade                                                               | Solução Atual                                                               | Solução Proposta                                                                             |
| :-------------- | :---------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- |
| Ferramenta que auxilie na circulação de informações | Ser acessível |  Sites, Blogs, Redes Sociais  | Uma forma flexível, confiável, simples, direta e menos trabalhosa de auxílio à informação |

#### **3.7 Alternativas e concorrências**

### 3.7.1 Site UnB

O próprio site da UnB possui uma seção de perguntas frequentes, porém não é muito intuitivo e não possui uma interface amigável. Além disso, o site não é muito acessível, pois possui uma linguagem muito técnica e não é muito fácil de encontrar.

## **4. Visão geral do Produto**

### 4.1 Perspectiva do Produto

O objetivo do aplicativo em questão é aumentar a circulação de informações verídicas e viabilizar que elas sejam de fácil e rápido acesso, além de serem constantemente atualizadas. Sem o aplicativo, essas informações são disponibilizadas em vários meios de telecomunicação, porém muitas vezes as informações se perdem, elas ainda não são acessíveis a todos e nem sempre corretas e/ou atualizadas.

### 4.2 Resumo das capacidades

As capacidades do produto vão de encontro com as necessidades do público em geral que tem anseio por informações fáceis, atuais e verídicas sobre os seus direitos e discentes que ainda não possuem conhecimento sobre as informações mais comuns que devem ter acesso. Assim, o aplicativo será capaz de ofertar informações relacionadas a esta realidade. Por fim, todos esses recursos foram pensados para que o aplicativo seja capaz de estar sempre auxiliando o utilizador no tocante a barrar informações falsas ou a falta delas.

## **5. Recursos do Produto**

### 5.1 Interação

O aplicativo oferece uma interface interativa e intuitiva para o usuário acessar informações sobre a UNB.

### 5.2 Informação

O aplicativo oferece uma ampla gama de informações confiáveis sobre a UNB, incluindo regulamentos, processos administrativos, direitos e benefícios dos alunos.

