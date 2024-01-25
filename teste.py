import pandas as pd
import json

def ler_dados_json(arquivo):
    with open(arquivo, 'r') as file:
        return json.load(file)

# Função para processar os preços nos DataFrames
def processar_precos(df):
    df['Preco'] = df['Preco'].str.replace('R$ ', '').str.replace(',', '.').replace('-', pd.NA)
    df['Preco'] = pd.to_numeric(df['Preco'], errors='coerce')
    df['VP-A'] = df['Preco']
    df['VP-F'] = df['VP-A'] * (1 + 5.38 / 100)
    df['DIFERENÇA'] = df['VP-F'] - df['VP-A']
    df['DIFERENÇA (%)'] = (df['DIFERENÇA'] / df['VP-A']) * 100
    df['VP-A'] = df['VP-A'].map('R$ {:.2f}'.format, na_action='ignore')
    df['VP-F'] = df['VP-F'].map('R$ {:.2f}'.format, na_action='ignore')
    df['DIFERENÇA'] = df['DIFERENÇA'].map('R$ {:.2f}'.format, na_action='ignore')
    df['DIFERENÇA (%)'] = df['DIFERENÇA (%)'].map('{:.2f}%'.format, na_action='ignore')
    return df

# Carregar dados dos arquivos JSON
dados_vmz_disney = ler_dados_json('coleta_vmz_disney_25012024_1508.json')
dados_vmz_seaworld = ler_dados_json('coleta_vmz_seaworld_25012024_1509.json')
dados_voupra_disney = ler_dados_json('coleta_voupra_disney_25012024_1513.json')

# Converter para DataFrames
df_vmz_disney = pd.DataFrame(dados_vmz_disney)
df_vmz_seaworld = pd.DataFrame(dados_vmz_seaworld)
df_voupra_disney = pd.DataFrame(dados_voupra_disney)

# Processar os preços e calcular as diferenças
df_vmz_disney = processar_precos(df_vmz_disney)
df_vmz_seaworld = processar_precos(df_vmz_seaworld)
df_voupra_disney = processar_precos(df_voupra_disney)

# Exibir os DataFrames processados
print("Disney World Orlando (VMZ):")
print(df_vmz_disney)
print("\nSeaWorld Orlando (VMZ):")
print(df_vmz_seaworld)
print("\nDisney World Orlando (Voupra):")
print(df_voupra_disney)
