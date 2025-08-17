# app.py
# -------------------------------------------------------------
# App principal do portfólio (Streamlit) com SIDEBAR somente
# com componentes prontos do Streamlit (sem CSS).
# Estrutura esperada:
#   /sections/Home.py, Curriculo.py, Dados_F1.py, Macro_economia.py,
#            Valuation.py, Governanca_dados.py, Analise_quant.py
# -------------------------------------------------------------
  git config --global user.email "brito.luucas@hotmail.com"
  git config --global user.name "Lucas Pereira Brito"


import importlib
import streamlit as st

# 1) Configuração básica da página
st.set_page_config(
    page_title="EconomiX — Portfólio | Lucas Brito",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2) Sidebar — apenas componentes nativos do Streamlit
with st.sidebar:
    st.title("Main Menu")        # título simples
    st.divider()                 # separador nativo

    # Radio para navegação entre páginas (com emojis para dar identidade visual)
    page = st.radio(
        label="Navegação",
        options=[
            "🏠 Home",
            "📄 Currículo",
            "🏎️ Dados & F1",
            "📊 Macro Economia",
            "💰 Valuation",
            "🗂️ Governança de Dados",
            "🧪 Análise Quant",
        ],
        index=0,
    )

# 3) Conteúdo principal — cabeçalho geral (pode ser removido se a Home já exibir)
st.markdown("# EconomiX — Portfólio")

# 4) Roteamento simples: mapeia o texto do menu para o módulo em /sections
routes = {
    "🏠 Home": "sections.Home",
    "📄 Currículo": "sections.Curriculo",
    "🏎️ Dados & F1": "sections.Dados_F1",
    "📊 Macro Economia": "sections.Macro_economia",
    "💰 Valuation": "sections.Valuation",
    "🗂️ Governança de Dados": "sections.Governanca_dados",
    "🧪 Análise Quant": "sections.Analise_quant",
}

module_path = routes.get(page)

# 5) Carrega e executa o módulo correspondente
if module_path:
    try:
        mod = importlib.import_module(module_path)
        importlib.reload(mod)  # reexecuta o top-level da página selecionada
    except ModuleNotFoundError as e:
        st.error(f"Página não encontrada: `{module_path}`. Verifique se o arquivo existe em `/sections/`.")
        st.exception(e)
    except Exception as e:
        st.error("Ocorreu um erro ao carregar a página selecionada.")
        st.exception(e)

# 6) Rodapé simples
st.divider()
st.caption("© 2025 Lucas Pereira Brito — App Streamlit. Sidebar apenas com componentes nativos.")
