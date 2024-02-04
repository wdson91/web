import sys
sys.path.insert(0, get_directories())
from imports import *
from insert_database import inserir_dados_no_banco


inserir_dados_no_banco('df', 'vmz_seaworld')

print('teste')