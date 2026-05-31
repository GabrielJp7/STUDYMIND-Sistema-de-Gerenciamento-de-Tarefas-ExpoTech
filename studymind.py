# =============================================================
#   STUDYMIND — Sistema de Gerenciamento de Tarefas
#   Banco de Dados: MySQL | Execução: Terminal
#   Requisito: pip install mysql-connector-python
# =============================================================

import mysql.connector
from datetime import datetime

# =============================================================
# CONFIGURAÇÃO DO BANCO
# =============================================================

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "root",   # <-- altere aqui
    "database": "studymind"
}

# Usuário logado na sessão atual
usuario_logado = None


# =============================================================
# FUNÇÕES AUXILIARES
# =============================================================

def conectar():
    """Abre e retorna uma conexão com o banco de dados."""
    return mysql.connector.connect(**DB_CONFIG)


def linha():
    print("-" * 50)


def cabecalho(titulo):
    linha()
    print(f"  {titulo}")
    linha()


def pausar():
    input("\nPressione ENTER para continuar...")


# =============================================================
# FUNÇÕES DE AUTENTICAÇÃO
# =============================================================

def registrar_usuario():
    cabecalho("NOVO CADASTRO")

    nome  = input("Nome: ").strip()
    email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()

    if not nome or not email or not senha:
        print("\n[ERRO] Todos os campos são obrigatórios.")
        pausar()
        return

    conn   = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO tb_usuarios (usu_nome, usu_email, usu_senha) VALUES (%s, %s, %s)",
            (nome, email, senha)
        )
        conn.commit()
        print("\n[OK] Cadastro realizado com sucesso!")

    except mysql.connector.errors.IntegrityError:
        print("\n[ERRO] Este e-mail já está cadastrado.")

    finally:
        cursor.close()
        conn.close()

    pausar()


def fazer_login():
    global usuario_logado
    cabecalho("LOGIN")

    email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()

    conn   = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM tb_usuarios WHERE usu_email = %s AND usu_senha = %s",
        (email, senha)
    )
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        usuario_logado = usuario
        print(f"\n[OK] Bem-vindo(a), {usuario['usu_nome']}!")
    else:
        print("\n[ERRO] E-mail ou senha incorretos.")

    pausar()


def fazer_logout():
    global usuario_logado
    usuario_logado = None
    print("\n[OK] Sessão encerrada.")
    pausar()


# =============================================================
# FUNÇÕES DE TAREFAS — CREATE
# =============================================================

def criar_tarefa():
    cabecalho("NOVA TAREFA")

    titulo = input("Título: ").strip()
    if not titulo:
        print("\n[ERRO] O título é obrigatório.")
        pausar()
        return

    descricao        = input("Descrição (opcional): ").strip()
    materia          = input("Matéria (opcional): ").strip()
    dificuldade      = input("Dificuldade 1-5 (opcional): ").strip()
    tempo_estimado   = input("Tempo estimado em minutos (opcional): ").strip()
    prazo            = input("Prazo (AAAA-MM-DD, opcional): ").strip()
    prioridade       = input("Prioridade 1-5 (opcional): ").strip()

    # Converte campos numéricos — aceita vazio
    dificuldade    = int(dificuldade)    if dificuldade.isdigit()    else None
    tempo_estimado = int(tempo_estimado) if tempo_estimado.isdigit() else None
    prioridade     = int(prioridade)     if prioridade.isdigit()     else None
    prazo          = prazo if prazo else None

    conn   = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO tb_tarefas
           (usuario_id, taf_titulo, taf_descricao, taf_materia,
            taf_dificuldade, taf_tempo_estimado, taf_prazo,
            taf_prioridade, taf_status, usu_id)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pendente', %s)""",
        (
            usuario_logado["usu_id"], titulo, descricao or None,
            materia or None, dificuldade, tempo_estimado,
            prazo, prioridade, usuario_logado["usu_id"]
        )
    )
    conn.commit()

    cursor.close()
    conn.close()

    print("\n[OK] Tarefa criada com sucesso!")
    pausar()


# =============================================================
# FUNÇÕES DE TAREFAS — READ
# =============================================================

def listar_tarefas(mostrar_todas=False):
    conn   = conectar()
    cursor = conn.cursor(dictionary=True)

    if mostrar_todas:
        cursor.execute(
            "SELECT * FROM tb_tarefas WHERE usu_id = %s ORDER BY taf_prioridade DESC, taf_prazo ASC",
            (usuario_logado["usu_id"],)
        )
    else:
        cursor.execute(
            "SELECT * FROM tb_tarefas WHERE usu_id = %s AND taf_status = 'pendente' ORDER BY taf_prioridade DESC, taf_prazo ASC",
            (usuario_logado["usu_id"],)
        )

    tarefas = cursor.fetchall()
    cursor.close()
    conn.close()

    return tarefas


def exibir_tarefas():
    cabecalho("MINHAS TAREFAS")

    print("1 - Somente pendentes")
    print("2 - Todas as tarefas")
    opcao = input("\nFiltro: ").strip()

    mostrar_todas = opcao == "2"
    tarefas = listar_tarefas(mostrar_todas)

    if not tarefas:
        print("\nNenhuma tarefa encontrada.")
        pausar()
        return

    linha()
    for t in tarefas:
        prazo = t["taf_prazo"] if t["taf_prazo"] else "Sem prazo"
        print(f"[{t['taf_id']}] {t['taf_titulo']}")
        print(f"     Matéria: {t['taf_materia'] or '-'} | Status: {t['taf_status']}")
        print(f"     Prioridade: {t['taf_prioridade'] or '-'} | Prazo: {prazo}")
        linha()

    pausar()


def detalhar_tarefa():
    cabecalho("DETALHE DA TAREFA")

    id_tarefa = input("ID da tarefa: ").strip()

    if not id_tarefa.isdigit():
        print("\n[ERRO] ID inválido.")
        pausar()
        return

    conn   = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM tb_tarefas WHERE taf_id = %s AND usu_id = %s",
        (int(id_tarefa), usuario_logado["usu_id"])
    )
    t = cursor.fetchone()
    cursor.close()
    conn.close()

    if not t:
        print("\n[ERRO] Tarefa não encontrada.")
        pausar()
        return

    linha()
    print(f"ID:              {t['taf_id']}")
    print(f"Título:          {t['taf_titulo']}")
    print(f"Descrição:       {t['taf_descricao'] or '-'}")
    print(f"Matéria:         {t['taf_materia'] or '-'}")
    print(f"Dificuldade:     {t['taf_dificuldade'] or '-'}")
    print(f"Tempo estimado:  {t['taf_tempo_estimado'] or '-'} min")
    print(f"Prazo:           {t['taf_prazo'] or 'Sem prazo'}")
    print(f"Prioridade:      {t['taf_prioridade'] or '-'}")
    print(f"Status:          {t['taf_status']}")
    print(f"Criada em:       {t['taf_data_criacao']}")
    linha()

    pausar()


# =============================================================
# FUNÇÕES DE TAREFAS — UPDATE
# =============================================================

def editar_tarefa():
    cabecalho("EDITAR TAREFA")

    tarefas = listar_tarefas(mostrar_todas=True)
    if not tarefas:
        print("\nVocê não possui tarefas cadastradas.")
        pausar()
        return

    for t in tarefas:
        print(f"[{t['taf_id']}] {t['taf_titulo']} — {t['taf_status']}")

    linha()
    id_tarefa = input("ID da tarefa a editar: ").strip()

    if not id_tarefa.isdigit():
        print("\n[ERRO] ID inválido.")
        pausar()
        return

    conn   = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM tb_tarefas WHERE taf_id = %s AND usu_id = %s",
        (int(id_tarefa), usuario_logado["usu_id"])
    )
    t = cursor.fetchone()
    cursor.close()
    conn.close()

    if not t:
        print("\n[ERRO] Tarefa não encontrada.")
        pausar()
        return

    print("\nDeixe em branco para manter o valor atual.\n")

    titulo         = input(f"Título [{t['taf_titulo']}]: ").strip()
    descricao      = input(f"Descrição [{t['taf_descricao'] or ''}]: ").strip()
    materia        = input(f"Matéria [{t['taf_materia'] or ''}]: ").strip()
    dificuldade    = input(f"Dificuldade [{t['taf_dificuldade'] or ''}]: ").strip()
    tempo_estimado = input(f"Tempo estimado [{t['taf_tempo_estimado'] or ''}]: ").strip()
    prazo          = input(f"Prazo [{t['taf_prazo'] or ''}]: ").strip()
    prioridade     = input(f"Prioridade [{t['taf_prioridade'] or ''}]: ").strip()
    print(f"Status atual: {t['taf_status']}")
    print("Opções de status: pendente | em andamento | concluida")
    status         = input("Novo status (ou ENTER para manter): ").strip()

    # Mantém valor atual se campo deixado em branco
    novo_titulo         = titulo         if titulo         else t["taf_titulo"]
    nova_descricao      = descricao      if descricao      else t["taf_descricao"]
    nova_materia        = materia        if materia        else t["taf_materia"]
    nova_dificuldade    = int(dificuldade)    if dificuldade.isdigit()    else t["taf_dificuldade"]
    novo_tempo_estimado = int(tempo_estimado) if tempo_estimado.isdigit() else t["taf_tempo_estimado"]
    novo_prazo          = prazo          if prazo          else t["taf_prazo"]
    nova_prioridade     = int(prioridade)     if prioridade.isdigit()     else t["taf_prioridade"]
    novo_status         = status         if status         else t["taf_status"]

    conn   = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """UPDATE tb_tarefas
           SET taf_titulo = %s, taf_descricao = %s, taf_materia = %s,
               taf_dificuldade = %s, taf_tempo_estimado = %s,
               taf_prazo = %s, taf_prioridade = %s, taf_status = %s
           WHERE taf_id = %s AND usu_id = %s""",
        (
            novo_titulo, nova_descricao, nova_materia,
            nova_dificuldade, novo_tempo_estimado,
            novo_prazo, nova_prioridade, novo_status,
            int(id_tarefa), usuario_logado["usu_id"]
        )
    )
    conn.commit()
    cursor.close()
    conn.close()

    # Se concluída, registra no histórico automaticamente
    if novo_status == "concluida" and t["taf_status"] != "concluida":
        registrar_historico(int(id_tarefa))

    print("\n[OK] Tarefa atualizada com sucesso!")
    pausar()


# =============================================================
# FUNÇÕES DE TAREFAS — DELETE
# =============================================================

def excluir_tarefa():
    cabecalho("EXCLUIR TAREFA")

    tarefas = listar_tarefas(mostrar_todas=True)
    if not tarefas:
        print("\nVocê não possui tarefas cadastradas.")
        pausar()
        return

    for t in tarefas:
        print(f"[{t['taf_id']}] {t['taf_titulo']} — {t['taf_status']}")

    linha()
    id_tarefa = input("ID da tarefa a excluir: ").strip()

    if not id_tarefa.isdigit():
        print("\n[ERRO] ID inválido.")
        pausar()
        return

    confirmacao = input(f"\nTem certeza que deseja excluir a tarefa {id_tarefa}? (s/n): ").strip().lower()

    if confirmacao != "s":
        print("\n[CANCELADO] Nenhuma tarefa foi excluída.")
        pausar()
        return

    conn   = conectar()
    cursor = conn.cursor()

    # Remove histórico vinculado antes de excluir a tarefa
    cursor.execute("DELETE FROM tb_historico WHERE taf_id = %s", (int(id_tarefa),))

    cursor.execute(
        "DELETE FROM tb_tarefas WHERE taf_id = %s AND usu_id = %s",
        (int(id_tarefa), usuario_logado["usu_id"])
    )
    linhas_afetadas = cursor.rowcount
    conn.commit()

    cursor.close()
    conn.close()

    if linhas_afetadas > 0:
        print("\n[OK] Tarefa excluída com sucesso!")
    else:
        print("\n[ERRO] Tarefa não encontrada.")

    pausar()


# =============================================================
# FUNÇÕES DE HISTÓRICO
# =============================================================

def registrar_historico(id_tarefa):
    tempo = input("Tempo real gasto (em minutos, opcional): ").strip()
    tempo_real = int(tempo) if tempo.isdigit() else None

    conn   = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tb_historico (hist_tarefa_id, hist_tempo_real, taf_id) VALUES (%s, %s, %s)",
        (id_tarefa, tempo_real, id_tarefa)
    )
    conn.commit()
    cursor.close()
    conn.close()

    print("[OK] Tarefa registrada no histórico!")


def ver_historico():
    cabecalho("HISTÓRICO DE TAREFAS CONCLUÍDAS")

    conn   = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """SELECT h.hist_id, t.taf_titulo, h.hist_data_conclusao, h.hist_tempo_real
           FROM tb_historico h
           JOIN tb_tarefas t ON t.taf_id = h.taf_id
           WHERE t.usu_id = %s
           ORDER BY h.hist_data_conclusao DESC""",
        (usuario_logado["usu_id"],)
    )
    registros = cursor.fetchall()
    cursor.close()
    conn.close()

    if not registros:
        print("\nNenhuma tarefa concluída ainda.")
        pausar()
        return

    linha()
    for r in registros:
        tempo = f"{r['hist_tempo_real']} min" if r["hist_tempo_real"] else "-"
        print(f"[{r['hist_id']}] {r['taf_titulo']}")
        print(f"     Concluída em: {r['hist_data_conclusao']} | Tempo real: {tempo}")
        linha()

    pausar()


# =============================================================
# MENUS
# =============================================================

def menu_tarefas():
    while True:
        cabecalho(f"TAREFAS — {usuario_logado['usu_nome']}")
        print("1 - Criar nova tarefa")
        print("2 - Listar tarefas")
        print("3 - Detalhar tarefa")
        print("4 - Editar tarefa")
        print("5 - Excluir tarefa")
        print("6 - Ver histórico")
        print("0 - Voltar")
        linha()

        opcao = input("Opção: ").strip()

        if opcao == "1":
            criar_tarefa()
        elif opcao == "2":
            exibir_tarefas()
        elif opcao == "3":
            detalhar_tarefa()
        elif opcao == "4":
            editar_tarefa()
        elif opcao == "5":
            excluir_tarefa()
        elif opcao == "6":
            ver_historico()
        elif opcao == "0":
            break
        else:
            print("\n[ERRO] Opção inválida.")
            pausar()


def menu_principal():
    while True:
        cabecalho("STUDYMIND — Sistema de Tarefas")
        print("1 - Login")
        print("2 - Cadastrar-se")
        print("0 - Sair")
        linha()

        opcao = input("Opção: ").strip()

        if opcao == "1":
            fazer_login()
            if usuario_logado:
                menu_tarefas()
                fazer_logout()
        elif opcao == "2":
            registrar_usuario()
        elif opcao == "0":
            print("\nAté logo!\n")
            break
        else:
            print("\n[ERRO] Opção inválida.")
            pausar()


# =============================================================
# PONTO DE ENTRADA
# =============================================================

menu_principal()
