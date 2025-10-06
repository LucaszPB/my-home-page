# streamlit run em_breve.py
import streamlit as st
import time
import random

st.set_page_config(page_title="Em breve", page_icon="⏳", layout="wide")

# Estado
if "tentativas" not in st.session_state:
    st.session_state.tentativas = 0

MAX_TENTATIVAS = 4

st.title("🚧 Opa! Esta sessão deu ruim (por enquanto) 😅")

# Botão (trava após 4)
botao_travado = st.session_state.tentativas >= MAX_TENTATIVAS
btn_label = "Tentar desbloquear 🔓" if not botao_travado else "Botão travado 🔒"

col1, col2 = st.columns([1.2, 1])
with col1:
    clicou = st.button(btn_label, use_container_width=True, disabled=botao_travado)
with col2:
    st.metric("Tentativas", st.session_state.tentativas)

# Área fixa para mensagem SEMPRE abaixo do botão
msg_area = st.container()

# Processa clique (até 4 loops)
if clicou and not botao_travado:
    with st.spinner("Consultando a IA… e chamando os duendes da nuvem…"):
        time.sleep(0.3)
    st.session_state.tentativas += 1

# Mensagens por tentativa (4 loops), depois trava e mostra "quebrou"
mensagens = [
    "❌ **Não foi dessa vez.** Essa opção bugou aqui… tente outra do lado!",
    "⚙️ **Ainda estou fazendo…** prometo que vai ficar bom assim que o GPT 6 sair.",
    "🧱 **Ainda estou fazendo… ainda!** (sim, continuo fazendo 🙃)",
    "🕹️ **Mini-jogo do Desbloqueio:** você quase conseguiu, mas… ainda estou fazendo.",
]
feedbacks = [
    "🧃 Derrubei meu suco no teclado. Tenta de novo!",
    "🧠 A IA disse: *quase!*",
    "🧩 Peça faltando detectada.",
    "🛰️ Erro 202 — Aceito, mas processando…",
]

# Decide qual texto mostrar (sempre abaixo do botão)
with msg_area:
    if st.session_state.tentativas == 0:
        st.info("👉 Aperte o botão para tentar desbloquear. Se der errado, tente outra página 😉")
    elif st.session_state.tentativas < MAX_TENTATIVAS:
        idx = st.session_state.tentativas - 1
        st.markdown(mensagens[idx])
        st.caption(random.choice(feedbacks))
    else:
        st.error("💥 **Ah não, você quebrou…** Brincadeira! 😄 Ainda estou fazendo. Explore as outras páginas por enquanto.")

# Barrinha simbólica discreta
progresso = min(st.session_state.tentativas, MAX_TENTATIVAS) / MAX_TENTATIVAS
st.progress(int(progresso * 100), text="Carregando o futuro… (versão humana quase IA)")

st.divider()
st.markdown("👉 **Dica:** pode navegar pelas outras páginas enquanto isso. Obrigado pela paciência! 🙏")
