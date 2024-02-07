import psycopg2
import pandas as pd
from datetime import datetime, timedelta
from create_database import criar_database
# Conectar ao banco de dados

def converter_data_hora(data_hora_str):
    formatos = ['%Y%m%d_%H%M%S.%f', '%Y-%m-%d %H:%M.%f','%Y-%m-%d %H:%M:%S.%f']  # Adicione mais formatos conforme necessário
    for formato in formatos:
        try:
            return pd.to_datetime(data_hora_str, format=formato)
        except (ValueError, TypeError):
            continue
    raise ValueError(f"Data e hora não reconhecidas: {data_hora_str}")


def inserir_dados_no_banco(df, nome_banco):
    
    # conexao = psycopg2.connect(
    # host="dpg-cmqhtt021fec739mbem0-a.oregon-postgres.render.com",
    # database="teste_fgdc",
    # user="teste_fgdc_user",
    # password="LlMXotSjrzJIJzw9OaICXHtunOOymrqe"
    # )


    conexao = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="Voupra2024st"
    )

    cursor = conexao.cursor()

    
    criar_database()

    # Comando SQL para inserir dados
    sql = "INSERT INTO {} (data_coleta, hora_coleta, data_viagem, parque, preco) VALUES (%s, %s, %s, %s, %s)".format(nome_banco)

    for _, row in df.iterrows():
        
        # Tratamento do preço
        preco_texto = row['Preco']
        
        if isinstance(preco_texto, str) and preco_texto.strip() == '-':
            preco = None  # Ou outro valor padrão se não permitir nulo
        else:
            try:
                preco = float(preco_texto)
            except ValueError:
                preco = None  # Ou outro valor padrão se não permitir nulo


        # Executar a inserção
        data_hora_atual = datetime.now()
        cursor.execute(sql, (row["Data_Coleta"], data_hora_atual.strftime("%H:%M"), row["Data_viagem"], row["Parque"], preco))
    
    # Commit e fechar conexões
    conexao.commit()
    cursor.close()
    conexao.close()
