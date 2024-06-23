# CLI para inicializar projeto Python

## Visão Geral

Este script facilita a inicialização de um projeto em Python ao automatizar algumas das etapas iniciais, incluindo:

- Criação de um ambiente virtual (`.venv`).
- Criação de um arquivo `README.md` vazio.
- Criação de um arquivo `.gitignore` para projetos Python.
- Inicialização de um repositório Git.

## Funcionalidades

- **Ambiente Virtual**: Configura um ambiente virtual na pasta do projeto para gerenciar dependências.
- **Arquivo `README.md`**: Cria um arquivo `README.md` vazio para seu projeto.
- **Arquivo `.gitignore`**: Baixa um arquivo `.gitignore` padrão para Python do GitHub ou cria um arquivo `.gitignore` básico se o download falhar.
- **Inicialização Git**: Cria um repositório Git na pasta do projeto e faz um commit inicial.

## Pré-requisitos
- Python 3.x instalado.
- Acesso à internet para baixar o arquivo `.gitignore` (opcional, mas recomendado).

## Como Usar

### Instalação

1. Clone este repositório para sua máquina local:
    ```
    git clone https://github.com/luizelias8/cli-inicializar-projeto-python.git
    cd cli-inicializar-projeto-python
    ```

2. Instale as dependências listadas no arquivo `requirements.txt` usando pip:
    ```
    pip install -r requirements.txt
    ```

### Execução

Para criar um projeto, execute o script fornecendo o nome do projeto como argumento:

    python cli_inicializar_projeto_python.py nome-do-projeto

Se você não fornecer um nome de projeto, o script utilizará o diretório atual:

    python cli_inicializar_projeto_python.py

### Argumentos

- `nome_projeto` (opcional): Nome do projeto. Se não for fornecido, o diretório atual será utilizado.
- `-v` ou `--version`: Exibe a versão do script.

### Exemplo

Para criar um projeto chamado `meu-projeto`:

    python cli_inicializar_projeto_python.py meu-projeto

## Autor

- [Luiz Elias](https://github.com/luizelias8)