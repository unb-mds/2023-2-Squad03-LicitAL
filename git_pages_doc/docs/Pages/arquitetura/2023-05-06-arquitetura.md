## Histórico de revisão

  |Data|Versão|Alteração|Autor|  
  |----|------|---------|-----|  
  |06/05/2023|0.1|Abertura do documento de Arquitetura|[Thiago Freitas](https://github.com/thiagorfreitas)|
  |19/05/2023|0.2|Adicionando o firebase|[Arthur Gabriel](https://github.com/ArthurGabrieel)|
  
## 1. Introdução
## 1.1 Finalidade
Este documento tem como finalidade apresentar a arquitetura do projeto GuiaUnB, de forma que fique de fácil entedimento a estrututra arquitetural do projeto, e sejam mostradas todas as decisões relacionadas a ela.
  
## 1.2 Escopo
Essa documentação engloba as funções visadas pelo projeto, além das tecnologias usadas, seu diagrama de relações e casos de uso. Engloba também algumas outras informações técnicas como características de desempenho e qualidade. O projeto é desenvolvido por alunos da UNB-FGA, na disciplina MDS.

## 2 Tecnologias
### 2.1 Flutter
<center>
<figure>
  <img width="300" src="https://storage.googleapis.com/cms-storage-bucket/847ae81f5430402216fd.svg" />
</figure>
</center>

O aplicativo GuiaUnB será construído utilizando o Flutter, um framework popular para desenvolvimento de aplicativos móveis. O Flutter foi escolhido por permitir a geração da aplicação para ambas as plataformas móveis mais populares - Android e iOS - e por ser uma ferramenta de fácil uso para implementação. A escolha foi feita pelos tecnologistas, que consideraram o Flutter a melhor opção para atender às necessidades do projeto.
  
### 2.2 Dart
<center>
<figure>
  <img width="100" src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Dart-logo.png" />
</figure>
</center>

Dart é a linguagem de programação utilizada pelo Flutter. Sendo assim, ela será utilizada para o desenvolvimento do GuiaUnB. O Dart é uma linguagem moderna e fácil de aprender, o que contribui para a eficiência no desenvolvimento de aplicativos móveis com o Flutter. Além disso, o Dart oferece uma performance de execução excepcional, o que é fundamental para garantir um bom desempenho do aplicativo.

### 2.3 Firebase
<center>
<figure>
  <img width="100" src="https://firebase.google.com/static/images/brand-guidelines/logo-logomark.png?hl=pt-br" />
</figure>
</center>

O Firebase é uma plataforma de desenvolvimento de aplicativos móveis e web oferecida pela Google. Ele inclui uma variedade de serviços, como banco de dados em tempo real, autenticação de usuários, hospedagem web, armazenamento em nuvem, notificações em tempo real, análise de dados, monitoramento de desempenho e funções na nuvem. Com essas ferramentas, os desenvolvedores podem criar aplicativos escaláveis, colaborativos e eficientes, aproveitando recursos prontos para uso e reduzindo a necessidade de gerenciar infraestrutura complexa.

# 3. Arquitetura Escolhida
## 3.1 Clean Architecture em Flutter
### 3.1.1 O que é Clean Architecture?
Clean Architecture é um padrão de arquitetura de software proposto por Robert C. Martin (também conhecido como Uncle Bob). A ideia central do padrão é separar o código em camadas bem definidas, onde cada camada tem uma responsabilidade específica e as dependências são invertidas. Isso torna o código mais modular, testável e fácil de manter.

### 3.1.2 As camadas da Clean Architecture são:

- Interface do Usuário: Camada responsável pela interação com o usuário. Aqui estão os widgets do Flutter que representam a interface gráfica da aplicação.

- Casos de Uso: Camada responsável por implementar as regras de negócio da aplicação. Essa camada usa as classes da camada de Infraestrutura para buscar e salvar dados.

- Regras de Negócio: Camada responsável por definir as regras de negócio da aplicação. Aqui estão as classes que implementam as validações e cálculos específicos da sua aplicação.

- Infraestrutura: Camada responsável por implementar as funcionalidades de baixo nível, como acesso a banco de dados e serviços web.

### 3.1.3 Por que usar Clean Architecture em Flutter?
A utilização da Clean Architecture em Flutter pode trazer diversos benefícios para a sua aplicação, dentre eles:

- Modularidade: A separação do código em camadas bem definidas facilita a manutenção e evolução da aplicação.

- Testabilidade: A separação do código em camadas bem definidas facilita a criação de testes automatizados.

- Reutilização de código: A separação do código em camadas bem definidas permite que as mesmas classes possam ser reutilizadas em diferentes projetos.

- Flexibilidade: A separação do código em camadas bem definidas permite que as camadas possam ser trocadas ou substituídas sem afetar as outras camadas.

### 3.1.4 Como utilizar Clean Architecture em Flutter?
Para utilizar a Clean Architecture em Flutter, você pode seguir os seguintes passos:

1. Defina as camadas da sua aplicação: Crie uma pasta para cada camada da Clean Architecture na sua estrutura de projeto.

2. Crie interfaces abstratas: Crie as interfaces abstratas que definem os contratos entre as camadas. Por exemplo, você pode criar uma interface abstrata para representar o repositório de dados que define os métodos que a camada de Casos de Uso pode chamar para acessar os dados.

3. Implemente as camadas: Crie as implementações concretas das interfaces abstratas em cada camada. Por exemplo, você pode criar uma implementação do repositório que utiliza uma API REST para buscar dados.

4. Injete as dependências: Utilize um mecanismo de injeção de dependências para injetar as dependências das classes em cada camada da sua aplicação. Existem diversas bibliotecas de injeção de dependências disponíveis para Flutter, como o Provider e o GetIt.

5. Crie widgets do Flutter para a camada de Interface do Usuário: Crie os widgets responsáveis pela interface do usuário da sua aplicação, injetando as dependências necessárias utilizando o mecanismo de injeção de dependências escolhido.

6. Utilize a arquitetura em cada tela da sua aplicação: Ao criar cada tela da sua aplicação, utilize as classes da camada de Casos de Uso para implementar as regras de negócio da tela, utilizando as classes da camada de Infraestrutura para buscar e salvar dados.

7. Teste a aplicação: Utilize testes automatizados para garantir o correto funcionamento da sua aplicação. Utilize testes unitários para testar as classes individualmente e testes de integração para testar as camadas em conjunto.

8. Evolua a aplicação: Com a separação do código em camadas bem definidas, fica mais fácil evoluir a aplicação de forma incremental, adicionando novas funcionalidades em cada camada sem afetar as outras camadas.

# 4. Conclusão
Clean Architecture é uma abordagem de arquitetura de software que pode trazer diversos benefícios para a sua aplicação Flutter, como modularidade, testabilidade, reutilização de código e flexibilidade. Ao utilizar Clean Architecture em sua aplicação, você pode separar o código em camadas bem definidas, cada uma com uma responsabilidade específica, facilitando a manutenção e evolução da aplicação. Utilize um mecanismo de injeção de dependências para injetar as dependências das classes em cada camada e utilize testes automatizados para garantir o correto funcionamento da sua aplicação.
