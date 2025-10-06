"""Home page layout built only with native Streamlit components."""

import streamlit as st


if "page" not in st.session_state:
    st.session_state["page"] = "home"


def navigate_to(page_id: str) -> None:
    """Update current page and refresh the app."""
    st.session_state["page"] = page_id
    try:
        st.query_params.update({"page": page_id})
    except Exception:  # st.query_params is available only on recent Streamlit versions
        st.experimental_set_query_params(page=page_id)
    st.rerun()


left, right = st.columns([2, 3], gap="small")
with left:
    st.image("assets/avatar.png", width=180)
with right:
    st.title("Olá! Eu me chamo Lucas")
    st.write(
        "Sou um engenheiro mecânico no mundo financeiro, com experiência em dados "
        "e análises, apaixonado por Macroeconomia, Mercado Financeiro, Dados, Fórmula 1 e "
        "Tecnologia. Este site é um espaço onde compartilho um pouco dessas paixões: "
        "projetos, análises e, claro, o meu Currículo. A ideia é mostrar ideias em "
        "diferentes estágios e a busca pela evolução constante."
    )

st.divider()

cards = [
    {
        "title": "Currículo",
        "desc": "Essa página apresenta o meu currículo de maneira online e diferente do tradicional. Use os botões no canto esquerdo da página e navegue por outras seções.",
        "id": "curriculo",
        "emoji": ":page_facing_up:",
    },
    {
        "title": "Dados & Fórmula 1 (Em Breve)",
        "desc": "Em breve, esta seção apresentará projetos de dados relacionados à Fórmula 1, utilizando a biblioteca FastF1 para análises de standings, telemetria e comparações.",
        "id": "dados_f1",
        "emoji": ":bar_chart: :checkered_flag:",
    },
    {
        "title": "Governança de Dados",
        "desc": "Essa página apresenta um overview de dados geral com arquitetura, governança e boas práticas que aprendi e observo ao longo da minha jornada.",
        "id": "governanca",
        "emoji": ":shield:",
    },
    {
        "title": "Macroeconomia",
        "desc": "Indicadores, regimes cambiais e leituras aplicadas ao mercado financeiro.",
        "id": "macro",
        "emoji": ":bar_chart: :earth_americas:",
    },
]

st.subheader("Temas para explorar. Utilize o menu no canto esquerdo da página.")
cards_per_row = 2
for start in range(0, len(cards), cards_per_row):
    row = cards[start : start + cards_per_row]
    columns = st.columns(len(row), gap="large")
    for column, card in zip(columns, row):
        with column:
            with st.container(border=True):
                st.markdown(f"### {card['emoji']}  {card['title']}")
                st.write(card["desc"])
                
