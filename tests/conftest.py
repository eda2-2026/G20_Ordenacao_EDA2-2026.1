import sys
import os

# Adiciona o diretório raiz do projeto (uma pasta acima da 'tests') ao PYTHONPATH.
# Isso garante que o Python encontre os arquivos 'models.py', 'utils.py' e a pasta 'sorting',
# não importando de onde você execute o comando pytest (terminal, VS Code, etc).
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
