# app.py
# -------------------------------------------------------------
# App principal do portfólio (Streamlit) com SIDEBAR estilizada
# usando streamlit-option-menu.
# Estrutura esperada:
#   /sections/Home.py, Curriculo.py, Dados_F1.py, Macro_economia.py,
#            Valuation.py, Governanca_dados.py, Analise_quant.py
# -------------------------------------------------------------
import importlib
import streamlit as st
from streamlit_option_menu import option_menu

# 1) Configuração básica da página
st.set_page_config(
    page_title="L.P.B. — Portfólio | Lucas Brito",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2) Sidebar — agora com option_menu
with st.sidebar:
    st.title("📌 Menu")
    st.markdown("Navegue pelas seções do meu portfólio e me conheça:")
    st.divider()

    page = option_menu(
        menu_title="",
        options=[
            "Home",
            "Currículo",
            "Dados & F1",
            "Governança de Dados",
            "Macro Economia",
            "Valuation (Em Breve)",
            "Análise Quant",
        ],
        icons=[
            "house",
            "file-earmark-text",
            "car-front",
            "database",      
            "bar-chart-line",
            "currency-dollar",
            "graph-up-arrow"
        ], 
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
    )

# 3) Cabeçalho geral
st.markdown("# L.P.B. — Portfólio")

# 4) Roteamento simples: mapeia o texto do menu para o módulo em /sections
routes = {
    "Home": "sections.Home",
    "Currículo": "sections.Curriculo",
    "Dados & F1": "sections.Dados_F1",
    "Governança de Dados": "sections.Governanca_dados",
    "Macro Economia": "sections.Macro_economia",
    "Valuation": "sections.Valuation",
    "Análise Quant": "sections.Analise_quant",
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
st.caption(f"🧭 Página atual: {page or 'Home'}")
st.caption("© 2025 Lucas Pereira Brito — App Streamlit.")
