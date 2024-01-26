import pandas as pd

# Lendo os dados dos arquivos JSON
with open('coleta_vmz_disney_26012024_1220.json', 'r', encoding='utf-8') as file:
    dados_json1 = pd.read_json(file)

with open('coleta_vmz_seaworld_26012024_1222.json', 'r', encoding='utf-8') as file:
    dados_json2 = pd.read_json(file)

# Combinando os DataFrames
# Se você quiser apenas concatená-los (um após o outro)
df_combinado = pd.concat([dados_json1, dados_json2])

# OU, se você quiser fazer um merge baseado em uma coluna comum, por exemplo 'Data_viagem'
# df_combinado = pd.merge(dados_json1, dados_json2, on='Data_viagem', how='outer')

# Salvando em um arquivo Excel
df_combinado.to_excel("dados_combinados.xlsx", index=False, engine='xlsxwriter')
