import streamlit as st

# Home.py
# Tela inicial (home) para um mini-site em Streamlit.
# Gera uma introdução, lista de habilidades e "cards"/botões que direcionam para outras páginas.
# Para navegação simples usa st.session_state + query params.
# Salve como sections/Home.py e importe/exiba conforme seu fluxo de aplicação.


# --- Configurações iniciais ---
st.set_page_config(page_title="Home - Meu Mini Site", layout="wide", initial_sidebar_state="collapsed")

if "page" not in st.session_state:
    st.session_state["page"] = "home"

def navigate_to(page_id: str):
    """
    Define a página atual e atualiza query params.
    Chama experimental_rerun para refletir a mudança imediatamente.
    """
    st.session_state["page"] = page_id
    st.experimental_set_query_params(page=page_id)
    st.experimental_rerun()

# --- Estilo simples para "cards" ---
# Para esse estilo de Card

CARD_STYLE = """
<style>
:root {
    --card-bg: #ffffff;
    --card-border: rgba(0,0,0,0.06);
    --card-shadow: 0 6px 18px rgba(15,23,42,0.06);
    --card-text: #0f172a;
    --muted: #334155;
    --accent: linear-gradient(135deg,#60a5fa33 0%, #7c3aed22 100%);
}
/* Ajustes para modo escuro — mantém boa legibilidade sem branco sobre branco */
@media (prefers-color-scheme: dark) {
    :root {
        --card-bg: rgba(20,23,29,0.6);
        --card-border: rgba(255,255,255,0.06);
        --card-shadow: 0 8px 22px rgba(2,6,23,0.6);
        --card-text: #e6eef8;
        --muted: #cbd5e1;
        --accent: linear-gradient(135deg,#2563eb44 0%, #7c3aed44 100%);
    }
}

.card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    padding: 18px;
    border-radius: 12px;
    box-shadow: var(--card-shadow);
    min-height: 170px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 150ms ease, box-shadow 150ms ease, border-color 150ms ease;
    color: var(--card-text);
    overflow: hidden;
    backdrop-filter: blur(6px);
}

.card h3 {
    margin: 0 0 8px 0;
    font-size: 1.05rem;
    line-height: 1.2;
}

.card p {
    margin: 0;
    color: var(--muted);
    font-size: 0.95rem;
}

/* Pequeno bloco para emoji/acento */
.card .emoji {
    width: 36px;
    height: 36px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    background: var(--accent);
    font-size: 1.1rem;
    color: inherit;
}

/* Hover / foco mais visível em fundos claros e escuros */
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 14px 36px rgba(2,6,23,0.12);
    border-color: rgba(99,102,241,0.22);
}

/* Badges e CTA */
.skill-badge {
    display: inline-block;
    background: rgba(99,102,241,0.08);
    padding: 6px 10px;
    border-radius: 999px;
    margin: 4px 6px 4px 0;
    color: var(--card-text);
    font-size: 0.85rem;
    border: 1px solid rgba(99,102,241,0.08);
}

.cta {
    margin-top: 12px;
    display: flex;
    gap: 8px;
    align-items: center;
}

.card small {
    color: var(--muted);
}

/* Mobile tweaks */
@media (max-width: 600px) {
    .card { min-height: 140px; padding: 14px; }
    .card h3 { font-size: 1rem; }
}
</style>
"""

st.markdown(CARD_STYLE, unsafe_allow_html=True)

# --- Cabeçalho / Introdução ---
col1, col2 = st.columns([2, 3])
with col1:
    st.image("https://placehold.co/240x240?text=Avatar", width=180)
with col2:
    st.title("Olá — Bem-vindo(a) ao meu Mini Site")
    st.write(
        "Sou um Engenheiro no mundo se aventurando no mundo de dados e financeiro."
        "Aqui você encontrará minha expriência, minahs habilidades, e um pouco dos meus hobbys e projetos pessoais.(E claro alguns erros que vou cometendo no caminho hahaha :D)"
    )
    st.write("Se quiser navegar, use os cards abaixo ou a barra lateral.")

# --- Cards de navegação ---
st.subheader("Navegação rápida")
cards = [
    {"title": "Currículo", "desc": "Veja minhas experiencias, e conhecer sobre meu lado profissional.", "id": "curriculo", "emoji": "📄"},
    {"title": "Dados e Formula 1", "desc": "Essa sessao é onde eu encontro minahs habilidades e meus hobbys, como grande fâ de formula 1, e engneherio no mundo de dados ", "id": "dados_f1", "emoji": "🏁"},
    {"title": "Governança de Dados e Estrutura de dados", "desc": "Em um mundo onde temos diversos projetos, que envolvem ia e inumeroas pessoas criando projetos comaprtilhando informações, é nescessário uma boa organização dos dados padronizações e definições de papaeis muito bem definidos", "id": "governanca", "emoji": "🛡️"},
        {"title": "Analise quantitativa", "desc": "Projetos relevantes, repositórios e demos.", "id": "projetos", "emoji": "🧰"},
    {"title": "Analise quantitativa", "desc": "Projetos relevantes, repositórios e demos.", "id": "projetos", "emoji": "🧰"},    
        {"title": "Macroecônomia", "desc": "Vamos conversar? Me envie uma mensagem.", "id": "contato", "emoji": "✉️"},
    {"title": "Analise Fundamentalista", "desc": "Vamos conversar? Me envie uma mensagem.", "id": "contato", "emoji": "✉️"},

]


cols = st.columns(len(cards))
for c, card in zip(cols, cards):
    with c:
        st.markdown(
            f"<div class='card'><h3>{card['emoji']} {card['title']}</h3>"
            f"<p>{card['desc']}</p></div>",
            unsafe_allow_html=True,
        )
        # Botão para navegar
        if st.button(f"Abrir {card['title']}", key=f"btn_{card['id']}"):
            navigate_to(card["id"])


# --- Exibir página atual (apenas informativo) ---
st.caption(f"Página atual no estado: {st.session_state.get('page')}")

