DOCUMENTAÇÃO DO BANCO DE DADOS – STUDYMIND

1. Introdução

O StudyMind é um sistema desenvolvido para auxiliar estudantes na organização e gerenciamento de seus estudos. O sistema permite o cadastro de usuários, criação de tarefas acadêmicas e acompanhamento do histórico de atividades concluídas.

O banco de dados foi desenvolvido utilizando MySQL e tem como objetivo armazenar informações de forma estruturada e segura, garantindo o relacionamento entre usuários, tarefas e histórico de estudos.

---

2. Objetivo do Banco de Dados

O banco de dados do StudyMind foi criado para:

* Armazenar dados dos usuários cadastrados;
* Registrar tarefas de estudo;
* Controlar prazos e prioridades das atividades;
* Armazenar o histórico das tarefas concluídas;
* Permitir o acompanhamento da produtividade dos estudantes.

---

3. Estrutura do Banco de Dados

O banco de dados recebe o nome de:

studymind

Após sua criação, são utilizadas três tabelas principais:

* tb_usuarios
* tb_tarefas
* tb_historico

---

4. Tabela tb_usuarios

Descrição

A tabela tb_usuarios é responsável por armazenar as informações dos usuários cadastrados no sistema.

Campos

| Campo     | Tipo         | Descrição                      |
| --------- | ------------ | ------------------------------ |
| usu_id    | INT          | Identificador único do usuário |
| usu_nome  | VARCHAR(100) | Nome do usuário                |
| usu_email | VARCHAR(150) | Endereço de e-mail             |
| usu_senha | VARCHAR(255) | Senha do usuário               |

Características

* A chave primária é o campo usu_id.
* O campo usu_id é auto incrementado.
* O campo usu_email possui restrição UNIQUE para impedir e-mails duplicados.
* Todos os campos são obrigatórios.

---

5. Tabela tb_tarefas

Descrição

A tabela tb_tarefas é responsável por armazenar as tarefas de estudo cadastradas pelos usuários.

Campos

| Campo              | Tipo         | Descrição                 |
| ------------------ | ------------ | ------------------------- |
| taf_id             | INT          | Identificador da tarefa   |
| usuario_id         | INT          | Identificação do usuário  |
| taf_titulo         | VARCHAR(200) | Título da tarefa          |
| taf_descricao      | TEXT         | Descrição da tarefa       |
| taf_materia        | VARCHAR(100) | Matéria relacionada       |
| taf_dificuldade    | INT          | Nível de dificuldade      |
| taf_tempo_estimado | INT          | Tempo estimado em minutos |
| taf_prazo          | DATE         | Data limite da tarefa     |
| taf_prioridade     | INT          | Nível de prioridade       |
| taf_status         | VARCHAR(50)  | Status da tarefa          |
| taf_data_criacao   | TIMESTAMP    | Data de criação           |
| usu_id             | INT          | Chave estrangeira         |

Características

* A chave primária é taf_id.
* O campo taf_status possui valor padrão "pendente".
* O campo taf_data_criacao recebe automaticamente a data e hora de criação da tarefa.

Relacionamento

A tabela tb_tarefas possui uma chave estrangeira que referencia a tabela tb_usuarios.

Cada usuário pode possuir várias tarefas cadastradas.

---

6. Tabela tb_historico

Descrição

A tabela tb_historico registra informações sobre tarefas concluídas pelos usuários.

Campos

| Campo               | Tipo     | Descrição                  |
| ------------------- | -------- | -------------------------- |
| hist_id             | INT      | Identificador do histórico |
| hist_tarefa_id      | INT      | Identificador da tarefa    |
| hist_data_conclusao | DATETIME | Data de conclusão          |
| hist_tempo_real     | INT      | Tempo gasto na atividade   |
| taf_id              | INT      | Chave estrangeira          |

Características

* A chave primária é hist_id.
* A data de conclusão é preenchida automaticamente.
* O histórico está vinculado a uma tarefa específica.

Relacionamento

A tabela tb_historico possui uma chave estrangeira que referencia a tabela tb_tarefas.

Cada tarefa pode possuir registros relacionados ao seu histórico de conclusão.

---

7. Relacionamentos do Banco de Dados

### Usuário → Tarefa

Um usuário pode cadastrar várias tarefas.

Relacionamento: 1:N (Um para Muitos)

### Tarefa → Histórico

Uma tarefa pode possuir registros de histórico.

Relacionamento: 1:N (Um para Muitos)

---

8. Regras de Negócio

* Um usuário deve possuir e-mail único.
* Uma tarefa deve estar associada a um usuário.
* Toda tarefa possui um status.
* O sistema registra automaticamente a data de criação da tarefa.
* O sistema registra automaticamente a data de conclusão da tarefa no histórico.

---

9. Conclusão

O banco de dados do StudyMind foi projetado para oferecer suporte ao gerenciamento de estudos, permitindo o cadastro de usuários, controle de tarefas e armazenamento do histórico de atividades realizadas.

Sua estrutura garante organização, integridade dos dados e possibilita futuras expansões do sistema, como relatórios de desempenho, estatísticas de produtividade e acompanhamento de metas de estudo.
