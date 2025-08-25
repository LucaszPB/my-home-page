# sections/Home.py
# Home melhorada: layout com componentes nativos do Streamlit (sem CSS),
# cards responsivos, cabeçalho com quick actions e download de CV.
# Navegação simples via st.session_state + query params.

import streamlit as st
from pathlib import Path

# ------------- Configurações iniciais -------------
st.set_page_config(
    page_title="Home - Meu Mini Site",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "page" not in st.session_state:
    st.session_state["page"] = "home"

def navigate_to(page_id: str):
    """Define a página atual e atualiza os query params, forçando rerender."""
    st.session_state["page"] = page_id
    try:
        # API atual (1.29+): st.query_params
        st.query_params.update({"page": page_id})
    except Exception:
        # Fallback se estiver usando versão antiga do Streamlit
        st.experimental_set_query_params(page=page_id)
    st.rerun()

# ------------- Cabeçalho / Hero -------------
left, right = st.columns([2, 3], gap="small")

with left:
    # Avatar (substitua pela sua imagem estática local se preferir)
    st.image(r"assets\avatar.png", width=180)

with right:
    st.title("Olá! Eu sou o Lucas 👋")
    st.markdown(
        """
        Olá! Sou **Lucas**, um engenheiro de dados e análises, apaixonado por **Fórmula 1**, **Macroeconomia**, **História** e **Tecnologia**. 🚀  
        Este site é um espaço onde compartilho um pouco dessas paixões: projetos, análises e, claro, o meu **Currículo**.  

        Vale lembrar: você pode encontrar ideias em diferentes estágios, alguns acertos, alguns erros, mas todos eles refletem algo essencial sobre mim:  
        a busca pela **evolução constante**. 
        """
    )

st.divider()

# ------------- Definição dos cards -------------
cards = [
    {
        "title": "Currículo",
        "desc": "Experiências, conquistas e formações — um panorama do meu lado profissional. Fique a vontade para explorar",
        "id": "curriculo",
        "emoji": "📄"
    },
    {
        "title": "Dados & Fórmula 1",
        "desc": "Projetos de dados com FastF1: standings, telemetria e análises comparativas.",
        "id": "dados_f1",
        "emoji": "📊🏁"
    },
    {
        "title": "Governança de Dados",
        "desc": "Padrões, papéis e qualidade de dados: bases confiáveis para decisões melhores.",
        "id": "governanca",
        "emoji": "🛡️"
    },
    {
        "title": "Análise Quantitativa",
        "desc": "(Em breve)",
        "id": "quant",
        "emoji": "📉📈"
    },
    {
        "title": "Macroeconomia",
        "desc": "Indicadores, regimes cambiais e leituras aplicadas ao mercado financeiro.",
        "id": "macro",
        "emoji": "📊🌍"
    }
]

# ------------- Renderização dos cards (3 por linha) -------------
def render_cards_grid(items, cols_per_row=3):
    row = []
    for i, card in enumerate(items, start=1):
        row.append(card)
        if i % cols_per_row == 0 or i == len(items):
            cols = st.columns(len(row), vertical_alignment="center")
            for c, card_data in zip(cols, row):
                with c:
                    with st.container(border=True):
                        st.markdown(f"### {card_data['emoji']} {card_data['title']}")
                        st.write(card_data["desc"])
                        # CTA primário
                        st.button(
                            f"Abrir {card_data['title']}",
                            key=f"btn_{card_data['id']}",
                            use_container_width=True,
                            on_click=navigate_to,
                            args=(card_data["id"],)
                        )
            row = []

render_cards_grid(cards, cols_per_row=3)



