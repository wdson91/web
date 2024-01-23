import pandas as pd

async def join_dmz():
    # Nomes dos arquivos
    arquivo1 = './precos_ingressos.txt'
    arquivo2 = 'precos_vmz_disney.txt'
    arquivo_combinado_json = 'precos_ingressos_combinado.json'

    # Lendo os dados dos arquivos em DataFrames
    df1 = pd.read_csv(arquivo1, sep='\t')
    df2 = pd.read_csv(arquivo2, sep='\t')

    # Concatenando os DataFrames
    df_combinado = pd.concat([df1, df2], ignore_index=True)

    # Convertendo 'Data_viagem' para datetime
    df_combinado['Data_viagem'] = pd.to_datetime(df_combinado['Data_viagem'])

    # Definindo a ordem personalizada para a coluna 'Parque'
    ordem_personalizada = [
        "1 Dia - Disney Básico Magic Kingdom",
        "1 Dia - Disney Básico Hollywood Studios",
        "1 Dia - Disney Básico Animal Kingdom",
        "1 Dia - Disney Básico Epcot",
        "2 Dias - Disney World Básico",
        "3 Dias - Disney World Básico",
        "4 Dias - Disney Promocional",
        "4 Dias - Disney World Básico",
        "5 Dias - Disney World Básico"
    ]

    # Aplicando a ordenação personalizada
    df_combinado['Parque'] = pd.Categorical(df_combinado['Parque'], categories=ordem_personalizada, ordered=True)

    # Ordenando o DataFrame primeiro por 'Data_viagem', depois por 'Parque'
    df_combinado.sort_values(by=['Data_viagem', 'Parque'], inplace=True)

    # Escrevendo o DataFrame combinado e ordenado em um arquivo JSON
    df_combinado.to_json(arquivo_combinado_json, orient='records', lines=True)

    print(f"Os arquivos {arquivo1} e {arquivo2} foram combinados e ordenados em {arquivo_combinado_json}.")

# Exemplo de como chamar a função join_dmz

