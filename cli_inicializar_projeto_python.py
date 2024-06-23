from argparse import ArgumentParser
import os
import subprocess
import requests

__version__ = '1.2.0'

def download_gitignore(pasta_destino):
    url_gitignore = 'https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore'
    resposta = requests.get(url_gitignore)
    if resposta.status_code == 200:
        with open(os.path.join(pasta_destino, '.gitignore'), 'wb') as arquivo:
            arquivo.write(resposta.content)
        print('Arquivo .gitignore baixado e salvo com sucesso.')
        return True
    else:
        print(f'Falha ao baixar o arquivo .gitignore. Código de status: {resposta.status_code}')
        return False

def criar_projeto(diretorio):
    pasta_projeto = os.path.abspath(diretorio)
    os.makedirs(pasta_projeto, exist_ok=True)

    caminho_readme = os.path.join(pasta_projeto, 'README.md')
    with open(caminho_readme, 'w') as arquivo_readme:
        pass # Cria o arquivo README.md vazio

    # Tentativa de download do .gitignore do GitHub
    if not download_gitignore(pasta_projeto):
        # Se o download falhar, cria um .gitignore básico manualmente
        caminho_gitignore = os.path.join(pasta_projeto, '.gitignore')
        with open(caminho_gitignore, 'w') as arquivo_gitignore:
            arquivo_gitignore.write('\n'.join(['.venv', '__pycache__']))
        print('Criado .gitignore básico manualmente')

    comandos = [
        [
            'python',
            '-m',
            'venv',
            os.path.join(pasta_projeto, '.venv')
        ],
        ['git', '-C', pasta_projeto, 'init'],
        ['git', '-C', pasta_projeto, 'add', '.'],
        ['git', '-C', pasta_projeto, 'commit', '-m', 'Commit inicial']
    ]
    for comando in comandos:
        try:
            subprocess.run(comando, check=True, timeout=60)
        except FileNotFoundError as e:
            print(
                f'O comando {comando} falhou porque o processo '
                f'nao pode ser encontrado.\n{e}'
            )
        except subprocess.CalledProcessError as e:
            print(
                f'O comando {comando} falhou porque o processo '
                f'nao retornou um codigo de retorno bem-sucedido.\n{e}'
            )
        except subprocess.TimeoutExpired as e:
            print(f'O comando {comando} expirou o tempo.\n{e}')

def main():
    parser = ArgumentParser(description='Inicializa um projeto Python com ambiente virtual, readme e Git.')
    parser.add_argument('nome_projeto', type=str, nargs='?', help='Nome do projeto')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')

    args = parser.parse_args()

    if args.nome_projeto:
        criar_projeto(args.nome_projeto)
    else:
        print('Nenhum nome de projeto fornecido, usando o diretório atual.')
        criar_projeto(os.getcwd())

if __name__ == '__main__':
    main()