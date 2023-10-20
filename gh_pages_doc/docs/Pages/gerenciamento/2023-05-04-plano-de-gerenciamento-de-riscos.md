---
excerpt: ""
---
## Histórico de versões

| Data       | Versão | Descrição                      | Autor(es) |
| :--------: | :----: | :----------------------------: | :-------: |
| 04/05/2023 |  0.1   |  Criação do plano de riscos    | [Thiago Freitas](https://github.com/thiagorfreitas)|
| 06/05/2023 |  0.2   |  Atualizações no plano de riscos    | [Thiago Freitas](https://github.com/thiagorfreitas)|

## 1. Introdução
O Plano de Gerenciamento de Riscos fornece informações sobre papéis e responsabilidades relativas aos riscos e descreve as categorias de risco que podem ser expressas como uma estrutura analítica dos riscos.

## 2. Objetivo
O objetivo do Plano de Gerenciamento de Riscos é documentar os riscos associados ao projeto e as ações a serem tomadas para que eles sejam mitigados ou contingenciada.

## 3. Riscos

### 3.1. Risco Técnico

| Tipo         | Descrição                                                                                                       |
|--------------|-----------------------------------------------------------------------------------------------------------------|
| Requisitos   | Riscos gerados pela falta de mapeamento e elicitação de requisitos                                                      |
| Tecnologias  | Riscos gerados pela tecnologia usada                                                                            |
| Complexidade | Riscos gerados pela falta de conhecimento e pela forma na qual a equipe de desenvolvimento se adapta a tecnologia escolhida |
| Qualidade    | Riscos decorrentes da qualidade do produto final                                                                |

### 3.2. Risco de Gerenciamento

| Tipo         | Descrição                                                                                    |
|--------------|----------------------------------------------------------------------------------------------|
| Estimativa   | Riscos que podem afetar o tempo de produção do projeto                                       |
| Controle     | Riscos relacionados ao controle de atividades                                                |
| Planejamento | Riscos relacionados ao planejamento de confecção do projeto                                  |
| Comunicação  | Riscos relacionados às atividades e meio de comunicação, como ruídos ou falta de comunicação da equipe |

### 3.3. Risco Organizacional

| Tipo         | Descrição                                                                                                                                  |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Recursos     | Riscos gerados pela falta de recursos humanos e/ou tecnológicos, como perda ou defeitos em equipamentos ou membros que abandonam o projeto.|
| Priorização  | Riscos gerados pela má aplicação da técnica moscow na escolha de histórias de usuários na Sprint                                           |
| Dependências | Riscos que podem afetar a evolução do projeto                                                                                              |

### 3.4. Risco Externo

| Tipo         | Descrição                                                                                                |
|--------------|----------------------------------------------------------------------------------------------------------|
| Greve na UnB | Risco gerado pela paralisação de atividades na UnB                                                       |

## 4. Identificação dos Riscos

| ID   | Se                                                                      | por conta                                                          | o impacto será                                                                                         | Categoria EAR          |
|------|-------------------------------------------------------------------------|--------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|------------------------|
| RN01 | O projeto não atender os requisitos                                       | de falhas no levantamento de requisitos e na validação constante | atraso na entrega do produto e necessidade de redefinição dos requisitos                                 | Requisitos             |
| RN02 | A tecnologia usada apresentar problemas                                   | do seu proprietário                                                | atraso na entrega do produto e necessidade de troca de tecnologia equivalente                          | Tecnologias            |
| RN03 | Os arquitetos não conseguirem planejar e garantir a execução da arquitetura | da falta de conhecimento das tecnologias do projeto                | dificuldade na organização e atraso no desenvolvimento                          | Complexidade           |
| RN04 | A equipe de desenvolvimento não se adaptar às tecnologias escolhidas      | da falta de conhecimento das tecnologias do projeto                | atraso na entrega do produto ou falha total da entrega                                                 | Complexidade           |
| RN05 | Houverem dificuldades em realizar testes                                  | da falta de conhecimento                                           | atraso na entrega das histórias planejadas                                                             | Complexidade           |
| RN06 | O produto final estiver em baixa qualidade                                | da falhas da equipe de desenvolvimento                             | refazer todo o produto e necessidade de replanejamento                                                 | Qualidade              |
| RN07 | As atividades não forem concretizadas no prazo                            | da falta de integração da equipe de desenvolvimento                | atraso na baseline do projeto                                                                          | Estimativa/Dependência |
| RN08 | Houver histórias de usuário mal definidas                                 | de falta elicitação de requisitos de forma adequada                | atraso na entrega do produto e necessidade de redefinição das histórias                                | Estimativa             |
| RN09 | Houver Sprint mal planejada                                               | de histórias mal planejadas                                        | atraso na entrega do produto, dificuldade na compreensão das histórias e necessidade de replanejamento | Estimativa/Priorização |
| RN10 | Houver mudança no escopo                                                  | da falha no planejamento                                           | atraso e necessidade de replanejamento ou projeto não ser concluído a tempo                            | Planejamento           |
| RN11 | Houver falta de comunicação na equipe                                     | da não utilização dos meios de comunicação definidos               | dificuldade no gerenciamento da equipe por parte do Scrum Master e falta de alinhamento das equipes    | Comunicação            |
| RN12 | Houver problemas na comunicação da equipe                                 | do número de membros                                               | dificuldade no gerenciamento da equipe por parte do Scrum Master e falta de alinhamento das equipes    | Comunicação            |
| RN13 | Membros da equipe abandonarem o projeto                                   | da desmotivação, sobrecarga causadas ou não pela pandemia          | sobrecarga entre os membros restantes e necessidade de replanejamento                                  | Recursos/Pandemia               |
| RN14 | Houver perda ou defeitos em equipamentos                                  | de mal uso ou acidentes                                            | atraso na entrega do projeto e necessidade de replanejamento                                           | Recursos               |
| RN15 | Houver o cancelamento do projeto                                          | de falta de interesse do cliente                                   | interrupção do projeto                                                                                      | Cliente                |
| RN16 | A qualidade do software não corresponder às expectativas do cliente       | de má implementação                                                | descontentamento do Cliente e possibilidade de cancelamento do projeto                                 | Cliente/Qualidade      |
| RN17 | Houver greve na UnB                                                       | de orientações de assembleias do corpo docente ou estudantil       | interrupção do projeto                                                                                 | Greve na UnB           |

## 5. Interpretação

| ID   | Impacto | Probabilidade | Avaliação | Contingência  | Mitigação    |
|------|---------|---------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RN01 | Crítico | Muito Alta    | 25        | Revalidar todos os requisitos com o Product Owner e com o cliente, e aplicar validação constante nos requisitos levantados                                                   | Realizar constantes reuniões entre os membros da equipe, com o cliente e pesquisas necessárias para obtenção de conhecimento e compreensão sobre o escopo do projeto |
| RN02 | Crítico | Baixa         | 10        | Trocar para uma tecnologia equivalente                                                       | Escolher uma tecnologia com melhor suporte                                                                                                                       |
| RN03 | Crítico | Média         | 15        | Realizar a mudança na Arquitetura do projeto buscando outras tecnologias capazes de solucionar os problemas ocorridos                                                                   | Buscar conhecimento com outros alunos, professores, pessoas de fora da comunidade universitária, novas pesquisas e/ou cogitar a mudança de tecnologias               |
| RN04 | Crítico  | Alta         | 20        | Indicar treinamentos para a equipe de desenvolvimento sobre a tecnologia escolhida                                                                                                      | Estabelecer treinamentos constantes sobre a tecnologia escolhida                                                                                                     |
| RN05 | Crítico | Alta          | 20        | Indicar treinamentos para a equipe de desenvolvimento sobre testes                                                                                                                      | Estabelecer treinamentos constantes sobre testes                                                                                                                     |
| RN06 | Grande  | Alta          | 16        | Procurar ajuda de alunos, professores, pessoas de fora do ambiente universitário e aumentar a carga de estudos                                                                          | Realização de pesquisas constantes e consultoria com outros alunos, professores e pessoas de fora do ambiente universitário                                          |
| RN07 | Grande  | Alta          | 16        | Procurar ajuda de alunos, professores, pessoas de fora do ambiente universitário e aumentar a carga de estudos, por parte do Arquiteto                                                  | Realização de pesquisas constantes e consultoria com outros alunos, professores e pessoas de fora do ambiente universitário, por parte do Arquiteto                  |
| RN08 | Crítico | Muito Alta    | 25        | Realizar refatoração de código, testes e validação com o cliente                                                                                                                        | Realizar treinamentos de todas as tecnologias utilizadas, garantir a realização de testes, boas práticas de programação e validação com o cliente                    |
| RN09 | Crítico | Alta          | 20        | Realizar a entrega na próxima Sprint como dívida técnica e, talvez, realocá-la para uma dupla com mais facilidade com a tecnologia                                                      | Planejar as atividades e dividi-las nas sprints com base nos pesos e dificuldade definida no planning poker                                                          |
| RN10 | Grande  | Muito alta    | 20        | Realizar um replanejamento das histórias para que entrem em conformidade com os requisitos                                                                                              | Realizar constantes reuniões entre os membros da equipe, com o cliente e pesquisas necessárias para obtenção de conhecimento e compreensão sobre o escopo do projeto |
| RN11 | Grande  | Alta          | 16        | Realizar replanejamento da sprint utilizando a priorização do backlog do produto pela técnica moscow                                                                                    | Montar o backlog da sprint utilizando a priorização do backlog do produto pela técnica moscow                                                                       |
| RN12 | Crítico | Baixa         | 10        | Redefinir o quanto antes as mudanças de escopo                                                                                                                                          | Manter sempre a comunicação com o cliente                                                                                                                            |
| RN13 | Crítico | Muito alta    | 25        | Reafirmar a necessidade de um alto grau de comunicação e promover as mudanças necessárias, desde realização de daily meetings mais objetivas a mudanças de ferramentas para comunicação | Criando o Plano de comunicação em que a equipe demonstre comum acordo                                                                                                |
| RN14 | Crítico | Muito alta    | 25        | Reafirmar a necessidade de um alto grau de comunicação e promover as mudanças necessárias, desde realização de daily meetings mais objetivas a mudanças de ferramentas para comunicação | Criando o Plano de comunicação em que a equipe demonstre comum acordo                                                                                                |
| RN15 | Grande  | Muito alta    | 20        | Realocar as tarefas entre os membros presentes                                                                                                                                          | Conversar com a equipe a fim de reafirmar a importância do projeto para que a equipe o priorize                                                                      |
| RN16 | Grande  | Média         | 12        | Realocar as tarefas entre os membros com equipamentos que funcionam                                                                                                                     | Incentivar a manutenção recorrente e o cuidado com equipamentos                                                                                                                 |
| RN17 | Crítico | Muito Baixa   | 5         | Oferecer a melhor possibilidade de produto para o cliente                                                                                                                               | Manter comunicação constante com o cliente                                                                                                                     |
| RN19 | Crítico | Alta          | 20        | Realizar refatoração de código, testes e validação com o cliente                                                                                                                        | Realizar treinamentos de todas as tecnologias utilizadas, garantir a realização de testes, boas práticas de programação e validação com o cliente                    |
| RN19 | Crítico | Muito Baixa   | 5         | Aceitar o risco                                                                                                                                                                         | -                                                                                                                                                                    |

### 5.1. Tabela de Probabilidade

| Probabilidade | Intervalo     | Peso |
|---------------|---------------|------|
| Muito Baixa   | menor que 10% | 1    |
| Baixa         | de 10% a 25%  | 2    |
| Média         | de 25% a 50%  | 3    |
| Alta          | de 50% a 75%  | 4    |
| Muito Alta    | maior que 75% | 5    |

### 5.2. Tabela de Impacto

| Impacto        | Descrição                                            | Peso |
|----------------|------------------------------------------------------|------|
| Insignificante | Impacto insignificante para o andamento do projeto   | 1    |
| Pequeno        | Impacto com pouca influência no andamento do projeto | 2    |
| Médio          | Impacto notável para o andamento do projeto          | 3    |
| Grande         | Impacto grave para o andamento do projeto            | 4    |
| Crítico        | Impacto crítico para o andamento do projeto          | 5    |

### 5.3. Avaliação dos Riscos
A avaliação dos riscos é feita multiplicando o peso da probabilidade pelo peso do impacto.

| Impacto/Probabilidade | Muito Baixa | Baixa | Média | Alta | Muito Alta |
|-----------------------|-------------|-------|-------|------|------------|
| Insignificante        | 1           | 2     | 3     | 4    | 5          |
| Pequeno               | 2           | 4     | 6     | 8    | 10         |
| Médio                 | 3           | 6     | 9     | 12   | 15         |
| Grande                | 4           | 8     | 12    | 16   | 20         |
| Crítico               | 5           | 10    | 15    | 20   | 25         |

## 6. Referências

PMI (2017), UM GUIA DO CONHECIMENTO EM GERENCIAMENTO DE PROJETOS (GUIA PMBOK®), 6ª Ed. Acesso em: 04 de maio de 2023.

BRASIL, Brasil; Ada - Plano de Gerenciamento de Riscos. Disponível em: https://fga-eps-mds.github.io/2019.1-ADA/#/docs/project/risk_management_plan. Acesso em: 04 de maio de 2023.

VILARINS, Augusto; FRANÇA, Emanoel; SOARES, Ingrid. GamesBI - Riscos. Disponível em: https://fga-eps-mds.github.io/2018.2-GamesBI/viabilidade/riscos.html. Acesso em: 04 de maio de 2023.
