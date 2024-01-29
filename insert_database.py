import psycopg2
import pandas as pd
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
    
    conexao = psycopg2.connect(
    host="dpg-cmqhtt021fec739mbem0-a.oregon-postgres.render.com",
    database="teste_fgdc",
    user="teste_fgdc_user",
    password="LlMXotSjrzJIJzw9OaICXHtunOOymrqe"
)

    cursor = conexao.cursor()

    # Comando SQL para inserir dados
    sql = "INSERT INTO {} (data_hora_coleta, data_viagem, parque, preco) VALUES (%s, %s, %s, %s)".format(nome_banco)

    # Processar cada linha do DataFrame
    for _, row in df.iterrows():
        
        preco = row['Preco']
        if isinstance(preco, str) and preco.strip() == '-':
            preco = None  # Ou outro valor padrão se não permitir nulo
        else:
            try:
                preco = float(preco.replace('R$ ', '').replace(',', '.'))
            except ValueError:
                preco = None  # Ou outro valor padrão se não permitir nulo

        cursor.execute(sql, (row["Data_Hora_Coleta"], row["Data_viagem"], row["Parque"], preco))

    # Commit e fechar conexões
    conexao.commit()
    cursor.close()
    conexao.close()

def salvar_dados(df, diretorio, identificador, nome_banco):
    df['Data_Hora_Coleta'] = df['Data_Hora_Coleta'].apply(converter_data_hora)
    df['Data_Hora_Coleta'] = df['Data_Hora_Coleta'].dt.strftime('%Y-%m-%d %H:%M')
    df = df.sort_values(by=['Data_viagem', 'Parque'])

    # Aqui você pode optar por manter ou remover a parte de salvar em TXT e JSON
    # Se você quiser apenas inserir no banco, pode remover essas linhas

    # Inserir dados no banco de dados
    inserir_dados_no_banco(df, nome_banco)

    print(f'Dados inseridos no banco de dados: {nome_banco}')

# Exemplo de uso
# df = pd.read_csv('caminho_do_arquivo.csv')
# salvar_dados(df, 'diretorio', 'identificador', 'nome_do_banco')
