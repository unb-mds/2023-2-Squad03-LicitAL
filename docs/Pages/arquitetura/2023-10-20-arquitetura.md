## Histórico de Versões

| Data       | Versão | Alteração                                 | Autor                                      |
|------------|--------|------------------------------------------|--------------------------------------------|
| 20/10/2023 | 0.1    | Abertura do documento de Arquitetura    | [Joyce Dionizio](https://github.com/joycedio)  |

## 1. Introdução
### 1.1 Finalidade
Este documento tem como finalidade apresentar a arquitetura do projeto LicitAl, destacando a estrutura arquitetural do projeto e as decisões relacionadas a ela. O projeto LicitAl é voltado para a extração e manipulação de dados de licitações de diários oficiais, com um front-end desenvolvido em Angular e um processo de extração e manipulação de dados em Python, com o uso de Docker.

### 1.2 Escopo
Esta documentação abrange as tecnologias utilizadas, a arquitetura geral do projeto LicitAl, os componentes-chave e as decisões de design que direcionam o desenvolvimento.

## 2. Tecnologias
### 2.1 Angular
[![Angular](https://img.shields.io/badge/Angular-%23DD0031.svg?&style=for-the-badge&logo=angular&logoColor=white)](https://angular.io/)

O front-end do projeto LicitAl é desenvolvido em Angular. O Angular é um framework de código aberto desenvolvido pelo Google que facilita a criação de aplicativos web dinâmicos e ricos em recursos. A escolha do Angular se deve à sua capacidade de criar interfaces de usuário interativas e escaláveis.

### 2.2 Python
[![Python](https://img.shields.io/badge/python-%230095D5.svg?&style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

A parte de extração e manipulação de dados das licitações é realizada em Python. Python é uma linguagem de programação amplamente usada, especialmente para tarefas de processamento de dados. A escolha do Python permite uma manipulação eficaz e ágil dos dados dos diários oficiais.

### 2.3 Docker
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

O Docker é utilizado para criar e gerenciar contêineres, garantindo um ambiente consistente para a execução do processo de extração de dados. Isso simplifica o gerenciamento de dependências e facilita a implantação em diferentes ambientes.

## 3. Arquitetura
### 3.1 Arquitetura Geral
A arquitetura do projeto LicitAl é composta por três componentes principais: o front-end em Angular, o back-end em Python (com Docker) e a infraestrutura de armazenamento de dados. Eles funcionam juntos para permitir a extração, manipulação e apresentação de informações de licitações.

#### 3.1.1 Front-end em Angular
O front-end em Angular é a interface de usuário que permite aos usuários interagirem com o sistema. Ele fornece a capacidade de visualizar, pesquisar e analisar os dados de licitações. A comunicação entre o front-end e o back-end é realizada por meio de APIs.

#### 3.1.2 Back-end em Python com Docker
O back-end em Python é responsável pela extração e manipulação de dados dos diários oficiais das licitações. O uso de contêineres Docker ajuda a garantir a consistência do ambiente de execução. Este componente é dividido em duas partes:
- **Extração de Dados:** Este módulo é responsável por coletar informações dos diários oficiais, realizar análises e extrair os dados relevantes de licitações.
- **Manipulação de Dados:** Após a extração, os dados passam por um processo de limpeza, transformação e enriquecimento para melhorar a qualidade e a utilidade das informações.

#### 3.1.3 Infraestrutura de Armazenamento de Dados
A infraestrutura de armazenamento de dados é composta por um banco de dados ou repositório onde as informações extraídas e processadas são armazenadas. Isso permite que os dados sejam acessados de forma eficiente pelo front-end e outras partes do sistema.

### 3.2 Componentes de Arquitetura
A arquitetura do projeto LicitAl segue os princípios de modularidade e separação de responsabilidades. Os componentes-chave incluem:

- **Front-end em Angular:** Este componente consiste em componentes, módulos e serviços do Angular que lidam com a interface do usuário e a comunicação com o back-end.

- **Back-end em Python:** Dividido em módulos de Extração de Dados e Manipulação de Dados, este componente utiliza bibliotecas Python para realizar a extração e manipulação dos dados das licitações. O uso de contêineres Docker ajuda a garantir um ambiente controlado.

- **APIs de Comunicação:** O front-end se comunica com o back-end por meio de APIs RESTful para enviar solicitações e receber dados.

- **Banco de Dados/Repositório:** Este componente armazena os dados processados das licitações, permitindo que sejam consultados e apresentados ao usuário.

### 3.3 Fluxo de Dados
O fluxo de dados no projeto LicitAl segue a seguinte sequência:

1. O front-end em Angular envia solicitações para o back-end por meio de APIs.

2. O back-end em Python, usando Docker, recebe as solicitações e realiza a extração e manipulação dos dados dos diários oficiais.

3. Os dados processados são armazenados no banco de dados ou repositório.

4. O front-end acessa o banco de dados para recuperar os dados processados e apresentá-los aos usuários.

## 4. Conclusão
A arquitetura do projeto LicitAl foi projetada para extrair e manipular eficientemente os dados de licitações de diários oficiais, proporcionando uma interface de usuário amigável. A combinação do front-end em Angular, do back-end em Python com Docker e da infraestrutura de armazenamento de dados cria um sistema completo e funcional. Esta arquitetura modular permite escalabilidade e manutenção facilitadas à medida que o projeto evolui.