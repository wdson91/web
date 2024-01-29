import psycopg2



def criar_tabela(conexao, nome_tabela):
    cursor = conexao.cursor()
    sql = f"""
    CREATE TABLE IF NOT EXISTS {nome_tabela} (
        id SERIAL PRIMARY KEY,
        data_hora_coleta TIMESTAMP,
        data_viagem DATE,
        parque VARCHAR(255),
        preco NUMERIC(10, 2)
    );
    """
    cursor.execute(sql)
    conexao.commit()
    cursor.close()
# Conectar ao banco de dados
conexao = psycopg2.connect(
    host="dpg-cmqhtt021fec739mbem0-a.oregon-postgres.render.com",
    database="teste_fgdc",
    user="teste_fgdc_user",
    password="LlMXotSjrzJIJzw9OaICXHtunOOymrqe"
)
# Nomes das tabelas a serem criadas
nomes_tabelas = ["vmz_disney", "vmz_seaworld", "vmz_universal", "voupra_disney", "voupra_seaworld", "voupra_universal"]

# Criar cada tabela
for nome_tabela in nomes_tabelas:
    criar_tabela(conexao, nome_tabela)

# Fechar a conexão com o banco de dados
conexao.close()

