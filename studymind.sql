CREATE DATABASE studymind;

USE studymind;

CREATE TABLE tb_usuarios (
    usu_id INT AUTO_INCREMENT PRIMARY KEY,
    usu_nome VARCHAR(100) NOT NULL,
    usu_email VARCHAR(150) NOT NULL UNIQUE,
    usu_senha VARCHAR(255) NOT NULL
);

CREATE TABLE tb_tarefas (
    taf_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    taf_titulo VARCHAR(200) NOT NULL,
    taf_descricao TEXT,
    taf_materia VARCHAR(100),
    taf_dificuldade INT,
    taf_tempo_estimado INT,
    taf_prazo DATE,
    taf_prioridade INT,
    taf_status VARCHAR(50) DEFAULT 'pendente',
    taf_data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usu_id INT,
    
    FOREIGN KEY (usu_id) REFERENCES tb_usuarios (usu_id)
);

CREATE TABLE tb_historico (
    hist_id INT AUTO_INCREMENT PRIMARY KEY,
    hist_tarefa_id INT NOT NULL,
    hist_data_conclusao DATETIME DEFAULT CURRENT_TIMESTAMP,
    hist_tempo_real INT,
    taf_id INT,
    
    FOREIGN KEY (taf_id) REFERENCES tb_tarefas(taf_id)
);
