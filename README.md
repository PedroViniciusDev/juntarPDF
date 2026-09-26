# Juntador de PDFs

Aplicativo desktop desenvolvido em Python com Tkinter para reunir vários
arquivos PDF em um único documento, permitindo escolher a ordem, o nome
e a pasta de destino.

## Funcionalidades

-   Selecionar vários arquivos PDF de uma vez.
-   Visualizar a lista de documentos selecionados.
-   Remover um documento ou limpar a lista.
-   Alterar manualmente a ordem dos PDFs antes da junção.
-   Definir o nome do arquivo final.
-   Escolher a pasta de destino.
-   Avisar antes de substituir um arquivo que já existe.
-   Impedir que o arquivo final substitua um dos PDFs de origem.
-   Preservar os arquivos originais.

## Tecnologias

-   **Python** --- linguagem de programação.
-   **Tkinter / ttk** --- interface gráfica.
-   **pypdf** --- leitura e junção de arquivos PDF.
-   **pathlib** --- manipulação de caminhos e nomes de arquivos.
-   **PyInstaller** --- geração do executável para Windows.

## Requisitos para executar pelo código

-   Python 3.13 ou versão compatível.
-   Tkinter, normalmente incluído na instalação do Python para Windows.
-   Biblioteca `pypdf`.

## Instalação e execução pelo código

Abra o terminal na pasta do projeto e instale a dependência:

``` powershell
python -m pip install pypdf
```

Execute o programa:

``` powershell
python main.py
```

> Se o arquivo principal tiver outro nome, substitua `main.py` pelo nome
> correto.

## Gerar o executável (.exe)

É possível gerar o executável sem ativar um ambiente virtual, desde que
o Python esteja instalado e disponível no terminal.

1.  Instale o PyInstaller:

    ``` powershell
    python -m pip install pyinstaller
    ```

2.  Na pasta do projeto, execute:

    ``` powershell
    python -m PyInstaller --onefile --windowed --name JuntadorPDF main.py
    ```

3.  Ao terminar, o executável estará em:

    ``` text
    dist/JuntadorPDF.exe
    ```

-   `--onefile`: gera um único arquivo executável.
-   `--windowed`: abre o aplicativo sem uma janela de terminal.
-   `--name JuntadorPDF`: define o nome do executável.

> O comando acima considera que o arquivo principal se chama `main.py`.
> Ajuste o nome se necessário.

## Como usar

1.  Clique em **Selecionar PDFs** e escolha os documentos que deseja
    juntar.
2.  Use **Mover para cima** e **Mover para baixo** para organizar a
    ordem.
3.  Remova arquivos indesejados, se necessário.
4.  Digite o nome do documento final.
5.  Escolha a pasta onde o arquivo será salvo.
6.  Clique em **Juntar PDFs**.

A ordem dos arquivos na lista determina a ordem das páginas no PDF
final. O programa não apaga nem modifica os PDFs de origem.

## Estrutura esperada

``` text
JuntarPDF/
├── main.py
├── README.md
└── dist/
    └── JuntadorPDF.exe
```

A pasta `dist/` é criada pelo PyInstaller durante a geração do
executável.

## Publicação no GitHub

Antes de publicar, confira se o projeto não contém documentos PDF
pessoais, dados confidenciais, senhas ou outros arquivos que não devam
ser públicos. Evite enviar a pasta `.venv/` e arquivos temporários de
compilação.

## Licença

Nenhuma licença foi definida neste repositório. Se o projeto for
publicado para reutilização por outras pessoas, considere adicionar uma
licença apropriada.
