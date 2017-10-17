# FeederinhoBot
O FeederinhoBot é um Bot do telegram feito em Python ao qual é fornecido um Arquivo com links RSS (lista.txt) e posts versionados via SQLite3.

## Requisitos

* Python3
* PIP
* python3-virtualenv
* SQLite3

## Passos da Instalação para Debian/Ubuntu

1. Instale o PIP que é o instalador de pacotes do python3

    Baixe o arquivo get-pip.py que é um arquivo instalador executado pelo Python. O arquivo se encontra no link https://bootstrap.pypa.io/get-pip.py.
O arquivo pode ser baixado de forma direta e rápida utilizando o comando wget -c. A opção -c tem a função de continuar o download em caso de perda de conexão.

    ```
    wget -c https://bootstrap.pypa.io/get-pip.py

    sudo python3 get-pip.py
    ```

2. Instale o construtor de ambiente virtual
    ```
    sudo apt-get install python3-virtualenv python3-venv
    ```
3. Crie o ambiente virtual
    ```
    pyvenv /caminho/para/o/ambiente/virtual

    ```    
    E depois entre no diretório
     ```
     cd  /caminho/para/o/ambiente/virtual

     ```
4. Clone o repositório do projeto do github
    ```
    git clone https://github.com/culturagovbr/FeederinhoBot.git feedero

    ```

5. Ative o ambiente virtual
    ```
    source /caminho/para/o/ambiente/virtual/bin/activate

    ```
    E depois entre no diretório do projeto
     ```
     cd  /caminho/para/o/ambiente/virtual/snc/

     ```

6. Instale as dependências python do projeto
    ```
    pip3 install -r requirements.txt
    ```

7. Execute a aplicação (É preciso ter o ambiente virtual ativado)
    ```
    python3 feed.py runservice

    ```
## Configuração do Temporizador

Atualmente o código possui um Temporizador para atualizar à cada 4 minutos, caso deseje modificar, encontra-se na linha
```
time.sleep(240)
```
