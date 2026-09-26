
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from pypdf import PdfWriter

# =========================
# CONFIGURAÇÕES
# =========================

arquivos_selecionados = []
pasta_destino = None

COR_FUNDO = "#F3F5F9"
COR_BRANCO = "#FFFFFF"
COR_PRIMARIA = "#2563EB"
COR_PRIMARIA_HOVER = "#1D4ED8"
COR_TEXTO = "#1E293B"
COR_SECUNDARIA = "#64748B"
COR_PERIGO = "#DC2626"
COR_BORDA = "#E2E8F0"


# =========================
# FUNÇÕES
# =========================

def atualizar_lista():
    """Atualiza a lista de documentos na interface."""
    lista_arquivos.delete(0, tk.END)

    for arquivo in arquivos_selecionados:
        lista_arquivos.insert(tk.END, Path(arquivo).name)

    atualizar_status()


def atualizar_status():
    """Atualiza a quantidade de PDFs selecionados."""
    quantidade = len(arquivos_selecionados)

    if quantidade == 0:
        label_status.config(text="Nenhum documento selecionado")
    elif quantidade == 1:
        label_status.config(text="1 documento selecionado")
    else:
        label_status.config(
            text=f"{quantidade} documentos selecionados"
        )


def selecionar_pdfs():
    """Seleciona vários arquivos PDF."""
    arquivos = filedialog.askopenfilenames(
        title="Selecione os documentos PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )

    for arquivo in arquivos:
        if arquivo not in arquivos_selecionados:
            arquivos_selecionados.append(arquivo)

    atualizar_lista()


def remover_pdf():
    """Remove apenas o documento selecionado."""
    selecao = lista_arquivos.curselection()

    if not selecao:
        messagebox.showwarning(
            "Atenção",
            "Selecione um documento para remover."
        )
        return

    indice = selecao[0]
    arquivos_selecionados.pop(indice)

    atualizar_lista()


def limpar_tudo():
    """Remove todos os documentos da lista."""
    if not arquivos_selecionados:
        messagebox.showinfo(
            "Lista vazia",
            "Não há documentos para limpar."
        )
        return

    confirmar = messagebox.askyesno(
        "Limpar todos os documentos",
        "Deseja remover todos os PDFs da lista?\n\n"
        "Os arquivos originais não serão apagados."
    )

    if confirmar:
        arquivos_selecionados.clear()
        atualizar_lista()


def mover_pdf(direcao):
    """Move o documento selecionado para cima ou para baixo."""
    selecao = lista_arquivos.curselection()

    if not selecao:
        messagebox.showwarning(
            "Atenção",
            "Selecione um documento para mover."
        )
        return

    indice = selecao[0]
    novo_indice = indice + direcao

    if novo_indice < 0 or novo_indice >= len(arquivos_selecionados):
        return

    arquivos_selecionados[indice], arquivos_selecionados[novo_indice] = (
        arquivos_selecionados[novo_indice],
        arquivos_selecionados[indice]
    )

    atualizar_lista()
    lista_arquivos.selection_set(novo_indice)
    lista_arquivos.activate(novo_indice)


def escolher_pasta():
    """Escolhe a pasta onde o PDF final será salvo."""
    global pasta_destino

    pasta = filedialog.askdirectory(
        title="Escolha a pasta de destino"
    )

    if pasta:
        pasta_destino = Path(pasta)
        label_pasta.config(
            text=str(pasta_destino),
            foreground=COR_TEXTO
        )


def juntar_pdfs():
    """Junta os documentos selecionados em um único PDF."""
    if len(arquivos_selecionados) < 2:
        messagebox.showwarning(
            "Atenção",
            "Selecione pelo menos dois PDFs para juntar."
        )
        return

    nome = entrada_nome.get().strip()

    if not nome:
        messagebox.showwarning(
            "Atenção",
            "Digite o nome do arquivo final."
        )
        entrada_nome.focus_set()
        return

    if any(c in nome for c in '<>:"/\\|?*'):
        messagebox.showwarning(
            "Nome inválido",
            "O nome contém caracteres não permitidos."
        )
        return

    if nome.endswith(".") or nome.endswith(" "):
        messagebox.showwarning(
            "Nome inválido",
            "O nome não pode terminar com ponto ou espaço."
        )
        return

    if not nome.lower().endswith(".pdf"):
        nome += ".pdf"

    if pasta_destino is None:
        messagebox.showwarning(
            "Atenção",
            "Escolha a pasta de destino."
        )
        return

    caminho_saida = pasta_destino / nome

    # Evitar substituir um dos arquivos de origem
    caminhos_origem = {
        Path(arquivo).resolve()
        for arquivo in arquivos_selecionados
    }

    if caminho_saida.resolve() in caminhos_origem:
        messagebox.showerror(
            "Destino inválido",
            "O arquivo final não pode substituir um dos PDFs originais."
        )
        return

    if caminho_saida.exists():
        confirmar = messagebox.askyesno(
            "Arquivo existente",
            "Já existe um arquivo com esse nome.\n"
            "Deseja substituí-lo?"
        )

        if not confirmar:
            return

    escritor = PdfWriter()

    try:
        for arquivo in arquivos_selecionados:
            escritor.append(arquivo)

        with open(caminho_saida, "wb") as pdf_final:
            escritor.write(pdf_final)

        messagebox.showinfo(
            "Sucesso",
            f"PDF criado com sucesso!\n\n{caminho_saida}"
        )

        label_status.config(
            text="PDF criado com sucesso!",
            foreground="#15803D"
        )

    except Exception as erro:
        messagebox.showerror(
            "Erro ao juntar PDFs",
            f"Não foi possível criar o documento:\n\n{erro}"
        )

    finally:
        escritor.close()


# =========================
# JANELA PRINCIPAL
# =========================

janela = tk.Tk()
janela.title("Juntador de PDFs")
janela.geometry("800x900")
janela.minsize(720, 800)
janela.configure(bg=COR_FUNDO)

# Estilo dos componentes ttk
estilo = ttk.Style()
estilo.theme_use("clam")

estilo.configure(
    "TFrame",
    background=COR_FUNDO
)

estilo.configure(
    "Card.TFrame",
    background=COR_BRANCO
)

estilo.configure(
    "TLabel",
    background=COR_FUNDO,
    foreground=COR_TEXTO,
    font=("Segoe UI", 10)
)

estilo.configure(
    "Titulo.TLabel",
    background=COR_FUNDO,
    foreground=COR_TEXTO,
    font=("Segoe UI", 22, "bold")
)

estilo.configure(
    "Subtitulo.TLabel",
    background=COR_FUNDO,
    foreground=COR_SECUNDARIA,
    font=("Segoe UI", 10)
)

estilo.configure(
    "Card.TLabel",
    background=COR_BRANCO,
    foreground=COR_TEXTO,
    font=("Segoe UI", 10)
)

estilo.configure(
    "CardTitulo.TLabel",
    background=COR_BRANCO,
    foreground=COR_TEXTO,
    font=("Segoe UI", 12, "bold")
)

estilo.configure(
    "Status.TLabel",
    background=COR_BRANCO,
    foreground=COR_SECUNDARIA,
    font=("Segoe UI", 9)
)

estilo.configure(
    "TButton",
    font=("Segoe UI", 10),
    padding=(12, 9),
    background="#E8EEF8",
    foreground=COR_TEXTO,
    borderwidth=0
)

estilo.map(
    "TButton",
    background=[("active", "#D8E3F4")]
)

estilo.configure(
    "Primario.TButton",
    background=COR_PRIMARIA,
    foreground="#FFFFFF",
    font=("Segoe UI", 11, "bold"),
    padding=(15, 12)
)

estilo.map(
    "Primario.TButton",
    background=[
        ("active", COR_PRIMARIA_HOVER),
        ("disabled", "#94A3B8")
    ],
    foreground=[("disabled", "#FFFFFF")]
)

estilo.configure(
    "Perigo.TButton",
    background="#FEE2E2",
    foreground=COR_PERIGO,
    padding=(12, 9)
)

estilo.map(
    "Perigo.TButton",
    background=[("active", "#FECACA")]
)

estilo.configure(
    "TEntry",
    padding=9,
    font=("Segoe UI", 11)
)

estilo.configure(
    "TScrollbar",
    background="#CBD5E1",
    troughcolor=COR_BRANCO,
    borderwidth=0,
    arrowsize=14
)


# =========================
# CABEÇALHO
# =========================

cabecalho = ttk.Frame(janela)
cabecalho.pack(fill="x", padx=30, pady=(25, 18))

ttk.Label(
    cabecalho,
    text="Juntador de PDFs",
    style="Titulo.TLabel"
).pack(anchor="w")

ttk.Label(
    cabecalho,
    text="Selecione, organize e reúna seus documentos em um único arquivo.",
    style="Subtitulo.TLabel"
).pack(anchor="w", pady=(5, 0))


# =========================
# CARD DE DOCUMENTOS
# =========================

card_documentos = ttk.Frame(
    janela,
    style="Card.TFrame",
    padding=20
)
card_documentos.pack(fill="both", expand=True, padx=30, pady=(0, 15))

ttk.Label(
    card_documentos,
    text="Documentos selecionados",
    style="CardTitulo.TLabel"
).pack(anchor="w")

ttk.Label(
    card_documentos,
    text="A ordem da lista será a ordem das páginas no PDF final.",
    style="Card.TLabel"
).pack(anchor="w", pady=(5, 12))

# Área da lista e barra de rolagem
area_lista = ttk.Frame(
    card_documentos,
    style="Card.TFrame"
)
area_lista.pack(fill="both", expand=True)

lista_arquivos = tk.Listbox(
    area_lista,
    font=("Segoe UI", 10),
    bg=COR_BRANCO,
    fg=COR_TEXTO,
    selectbackground=COR_PRIMARIA,
    selectforeground="#FFFFFF",
    activestyle="none",
    relief="solid",
    bd=1,
    highlightthickness=0,
    selectmode=tk.SINGLE
)
lista_arquivos.pack(side="left", fill="both", expand=True)

barra_rolagem = ttk.Scrollbar(
    area_lista,
    orient="vertical",
    command=lista_arquivos.yview
)
barra_rolagem.pack(side="right", fill="y")

lista_arquivos.config(
    yscrollcommand=barra_rolagem.set
)

# Contador
label_status = ttk.Label(
    card_documentos,
    text="Nenhum documento selecionado",
    style="Status.TLabel"
)
label_status.pack(anchor="w", pady=(10, 12))

# Botões de documentos
linha_botoes = ttk.Frame(
    card_documentos,
    style="Card.TFrame"
)
linha_botoes.pack(fill="x")

ttk.Button(
    linha_botoes,
    text="+ Selecionar PDFs",
    command=selecionar_pdfs
).pack(side="left", padx=(0, 6))

ttk.Button(
    linha_botoes,
    text="Remover",
    command=remover_pdf
).pack(side="left", padx=6)

ttk.Button(
    linha_botoes,
    text="Limpar tudo",
    command=limpar_tudo,
    style="Perigo.TButton"
).pack(side="right")


# =========================
# CARD DE ORGANIZAÇÃO
# =========================

card_organizacao = ttk.Frame(
    janela,
    style="Card.TFrame",
    padding=20
)
card_organizacao.pack(fill="x", padx=30, pady=(0, 15))

ttk.Label(
    card_organizacao,
    text="Organizar documentos",
    style="CardTitulo.TLabel"
).pack(anchor="w", pady=(0, 10))

linha_organizacao = ttk.Frame(
    card_organizacao,
    style="Card.TFrame"
)
linha_organizacao.pack(fill="x")

ttk.Button(
    linha_organizacao,
    text="↑ Mover para cima",
    command=lambda: mover_pdf(-1)
).pack(side="left", padx=(0, 8))

ttk.Button(
    linha_organizacao,
    text="↓ Mover para baixo",
    command=lambda: mover_pdf(1)
).pack(side="left")


# =========================
# CARD DE SAÍDA
# =========================

card_saida = ttk.Frame(
    janela,
    style="Card.TFrame",
    padding=20
)
card_saida.pack(fill="x", padx=30, pady=(0, 25))

ttk.Label(
    card_saida,
    text="Arquivo final",
    style="CardTitulo.TLabel"
).pack(anchor="w", pady=(0, 10))

ttk.Label(
    card_saida,
    text="Nome do documento",
    style="Card.TLabel"
).pack(anchor="w")

entrada_nome = ttk.Entry(card_saida)
entrada_nome.pack(fill="x", pady=(5, 12))

ttk.Button(
    card_saida,
    text="Escolher pasta de destino",
    command=escolher_pasta
).pack(anchor="w")

label_pasta = ttk.Label(
    card_saida,
    text="Nenhuma pasta selecionada",
    style="Status.TLabel",
    wraplength=680
)
label_pasta.pack(anchor="w", pady=(8, 15))

ttk.Button(
    card_saida,
    text="Juntar PDFs",
    command=juntar_pdfs,
    style="Primario.TButton"
).pack(fill="x")

# Iniciar a interface
janela.mainloop()
