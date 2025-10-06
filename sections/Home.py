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
    st.title("Ola! Eu sou o Lucas")
    st.write(
        "Ola! Sou um engenheiro mecanico no mundo financeiro, com experiencia em dados "
        "e analises, apaixonado por Formula 1, Macroeconomia, Mercado Financeiro e "
        "Tecnologia. Este site e um espaco onde compartilho um pouco dessas paixoes: "
        "projetos, analises e, claro, o meu Curriculo. A ideia e mostrar ideias em "
        "diferentes estagios e a busca pela evolucao constante."
    )

st.divider()

cards = [
    {
        "title": "Curriculo",
        "desc": "Essa página apresenta o meu currículo de maneira online e diferente do tradicional. Use os botões no canto esquerdo da página e navegue por outras seções.",
        "id": "curriculo",
        "emoji": ":page_facing_up:",
    },
    {
        "title": "Dados & Formula 1",
        "desc": "Projetos de dados com FastF1: standings, telemetria e analises comparativas.",
        "id": "dados_f1",
        "emoji": ":bar_chart: :checkered_flag:",
    },
    {
        "title": "Governanca de Dados",
        "desc": "Padroes, papeis e qualidade de dados para decisao baseada em informacao confiavel.",
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

st.subheader("Escolha uma trilha para explorar")
cards_per_row = 2
for start in range(0, len(cards), cards_per_row):
    row = cards[start : start + cards_per_row]
    columns = st.columns(len(row), gap="large")
    for column, card in zip(columns, row):
        with column:
            with st.container(border=True):
                st.markdown(f"### {card['emoji']}  {card['title']}")
                st.write(card["desc"])
                
