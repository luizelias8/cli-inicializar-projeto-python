from argparse import ArgumentParser
import os
import subprocess
import requests
import sys
import configparser

__version__ = '2.0.1'

def obter_caminho_preferencias():
    if hasattr(sys, 'frozen'):
        # Se o script está congelado (por exemplo, com PyInstaller), usa o diretório do executável
        caminho_base = os.path.dirname(sys.executable)
    else:
        # Se não está congelado, usa o diretório do script Python
        caminho_base = os.path.dirname(os.path.abspath(__file__))

    # Retorna o caminho completo para preferencias.ini
    return os.path.join(caminho_base, 'preferencias.ini')

def ler_preferencias():
    config = configparser.ConfigParser()
    caminho_preferencias = obter_caminho_preferencias()
    config.read(caminho_preferencias)

    # Leitura das preferências do arquivo ini
    preferencias = {
        'readme': config.getboolean('preferencias', 'readme', fallback=True),
        'git': config.getboolean('preferencias', 'git', fallback=True),
        'venv': config.getboolean('preferencias', 'venv', fallback=True)
    }

    return preferencias

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
    preferencias = ler_preferencias()

    pasta_projeto = os.path.abspath(diretorio)
    os.makedirs(pasta_projeto, exist_ok=True)

    # Criação do README.md se a preferência for 'on'
    if preferencias['readme']:
        caminho_readme = os.path.join(pasta_projeto, 'README.md')
        with open(caminho_readme, 'w') as arquivo_readme:
            pass # Cria o arquivo README.md vazio
        print('README.md criado.')
    else:
        print('readme não habilitado. README.md não será gerado.')

    # Inicialização do Git se a preferência for 'on'
    if preferencias['git']:
        # Tentativa de download do .gitignore do GitHub
        if not download_gitignore(pasta_projeto):
            # Se o download falhar, cria um .gitignore básico manualmente
            caminho_gitignore = os.path.join(pasta_projeto, '.gitignore')
            with open(caminho_gitignore, 'w') as arquivo_gitignore:
                arquivo_gitignore.write('\n'.join(['.venv', '__pycache__']))
            print('Criado .gitignore básico manualmente')

        comandos_git = [
            ['git', '-C', pasta_projeto, 'init'],
            ['git', '-C', pasta_projeto, 'add', '.gitignore']
        ]

        # Adiciona o README.md se a preferência for 'on'
        if preferencias['readme']:
            comandos_git.append(['git', '-C', pasta_projeto, 'add', 'README.md'])

        # Faz o commit inicial
        comandos_git.append(['git', '-C', pasta_projeto, 'commit', '-m', 'Commit inicial'])

        for comando in comandos_git:
            try:
                subprocess.run(comando, check=True, timeout=60)
                print(f"Comando Git '{' '.join(comando)}' executado com sucesso.")
            except subprocess.SubprocessError as e:
                print(f"Falha ao executar o comando Git.\n{e}")
    else:
        print('git não habilitado. .gitignore não será gerado.')

    # Criação do ambiente virtual se a preferência for 'on'
    if preferencias['venv']:
        comando_venv = [
            'python',
            '-m',
            'venv',
            os.path.join(pasta_projeto, '.venv')
        ]
        try:
            subprocess.run(comando_venv, check=True, timeout=60)
            print('Ambiente virtual criado.')
        except subprocess.SubprocessError as e:
            print(f'Falha ao criar o ambiente virtual.\n{e}')

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