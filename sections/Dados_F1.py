# pages/f1_ver_ham_analysis.py
# ======================================================================================
# Instalação rápida (execute no seu ambiente antes de rodar a página):
#   pip install fastf1 pandas pyarrow scikit-learn streamlit altair
# ======================================================================================
"""
Página Streamlit que consome os Parquets gerados por build_datasets_f1.py e apresenta:
- Standings 2021 (pilotos e construtores)
- Últimas 5 corridas: VER+HAM vs Outros
- Últimas 10 corridas: Duelos & Predição (modelo simples)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st
import altair as alt


# --------------------------------------------------------------------------------------
# Configuração básica
# --------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Análise F1 — VER vs HAM",
    page_icon="🏁",
    layout="wide",
)

# Guarda diretório de dados na sessão
if "data_dir" not in st.session_state:
    st.session_state["data_dir"] = "./data"


# --------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_parquet(path: str) -> Optional[pd.DataFrame]:
    p = Path(path)
    if p.exists():
        try:
            return pd.read_parquet(p)
        except Exception as e:
            st.warning(f"Falha ao carregar {p.name}: {e}")
            return None
    else:
        return None


def plot_points_bar(df: pd.DataFrame, label_col: str, points_col: str, title: str):
    """Gráfico de barras simples com Altair."""
    if df is None or df.empty or label_col not in df.columns or points_col not in df.columns:
        st.info("Dados insuficientes para o gráfico.")
        return
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(f"{points_col}:Q", title="Pontos"),
            y=alt.Y(f"{label_col}:N", sort="-x", title=""),
            tooltip=[label_col, points_col]
        )
        .properties(title=title, height=400)
    )
    st.altair_chart(chart, use_container_width=True)


def plot_group_comparison(df: pd.DataFrame, title: str):
    """Compara pontuação agregada Pair vs Others por corrida (barras lado a lado)."""
    if df is None or df.empty:
        st.info("Sem dados para comparação.")
        return

    cols_needed = ["race_name", "pair_points_sum", "others_points_sum"]
    if not all(c in df.columns for c in cols_needed):
        st.info("Colunas necessárias ausentes para o gráfico de comparação.")
        return

    melted = df[["race_name", "pair_points_sum", "others_points_sum"]].melt(
        id_vars="race_name",
        var_name="grupo",
        value_name="pontos"
    )
    # Renomeia para melhor leitura
    melted["grupo"] = melted["grupo"].map({
        "pair_points_sum": "VER+HAM",
        "others_points_sum": "Outros"
    })

    chart = (
        alt.Chart(melted)
        .mark_bar()
        .encode(
            x=alt.X("race_name:N", title="Corrida"),
            y=alt.Y("pontos:Q", title="Pontos"),
            color=alt.Color("grupo:N", title="Grupo"),
            tooltip=["race_name", "grupo", "pontos"]
        )
        .properties(title=title, height=400)
    )
    st.altair_chart(chart, use_container_width=True)


# --------------------------------------------------------------------------------------
# UI
# --------------------------------------------------------------------------------------
st.title("🏁 Análise F1 — Verstappen vs Hamilton")
st.caption(
    "Página baseada em dados do FastF1. "
    "Execute antes o ETL `build_datasets_f1.py` para gerar os arquivos Parquet em `./data/`."
)

with st.sidebar:
    st.header("Configurações")
    data_dir = st.text_input("Diretório dos datasets", value=st.session_state["data_dir"])
    st.session_state["data_dir"] = data_dir
    st.markdown("Seleção de ano (fixo = 2021 para standings).")
    year = st.selectbox("Ano (Standings)", options=[2021], index=0)
    st.markdown("---")
    st.markdown("Se algum arquivo estiver ausente, rode o script ETL e recarregue a página.")

# Caminhos
driver_path = os.path.join(st.session_state["data_dir"], "driver_standings_2021.parquet")
const_path = os.path.join(st.session_state["data_dir"], "constructor_standings_2021.parquet")
last5_path = os.path.join(st.session_state["data_dir"], "last5_ver_ham_vs_others.parquet")
feat_path = os.path.join(st.session_state["data_dir"], "last10_ver_ham_duel_features.parquet")
pred_path = os.path.join(st.session_state["data_dir"], "last10_ver_ham_duel_predictions.parquet")

# --------------------------------------------------------------------------------------
# Seção: Standings 2021
# --------------------------------------------------------------------------------------
st.subheader("📊 Standings 2021")
df_drv = load_parquet(driver_path)
df_con = load_parquet(const_path)

cols = st.columns(2)
with cols[0]:
    st.markdown("**Pilotos — Driver Standings**")
    if df_drv is not None:
        st.dataframe(df_drv.sort_values(by=[c for c in ["position", "points"] if c in df_drv.columns], ascending=[True, False] if "position" in df_drv.columns else False))
        # Gráfico de pontos por piloto
        label_col = "code" if "code" in df_drv.columns else ( "family_name" if "family_name" in df_drv.columns else None )
        if label_col and "points" in df_drv.columns:
            plot_points_bar(df_drv, label_col=label_col, points_col="points", title="Pontos por piloto (2021)")
    else:
        st.warning("Arquivo de pilotos não encontrado. Rode o ETL.")

with cols[1]:
    st.markdown("**Construtores — Constructor Standings**")
    if df_con is not None:
        st.dataframe(df_con.sort_values(by=[c for c in ["position", "points"] if c in df_con.columns], ascending=[True, False] if "position" in df_con.columns else False))
        # Gráfico de pontos por equipe
        label_col = "name" if "name" in df_con.columns else ( "constructor_id" if "constructor_id" in df_con.columns else None )
        if label_col and "points" in df_con.columns:
            plot_points_bar(df_con, label_col=label_col, points_col="points", title="Pontos por equipe (2021)")
    else:
        st.warning("Arquivo de construtores não encontrado. Rode o ETL.")

st.markdown("---")

# --------------------------------------------------------------------------------------
# Seção: Últimas 5 — VER+HAM vs Outros
# --------------------------------------------------------------------------------------
st.subheader("🧮 Últimas 5 corridas (2021): VER+HAM vs Outros")

df_last5 = load_parquet(last5_path)
if df_last5 is not None:
    # Tabela resumo por corrida
    show_cols = [c for c in [
        "year", "round", "race_name", "race_date",
        "pair_points_sum", "others_points_sum",
        "pair_final_pos_mean", "others_final_pos_mean",
        "pair_final_pos_median", "others_final_pos_median",
        "pair_fastest_count", "others_fastest_count"
    ] if c in df_last5.columns]

    st.dataframe(df_last5[show_cols].sort_values(by="round", ascending=True))

    # Gráfico de comparação de pontos
    plot_group_comparison(df_last5, title="Pontos agregados: VER+HAM vs Outros (por corrida)")

    # Destaques de fastest lap (se houver)
    if "pair_fastest_count" in df_last5.columns and "others_fastest_count" in df_last5.columns:
        fl_pair = int(df_last5["pair_fastest_count"].sum())
        fl_others = int(df_last5["others_fastest_count"].sum())
        st.info(f"Fastest Lap no período (somando corridas): **VER+HAM = {fl_pair}**, **Outros = {fl_others}**")
else:
    st.warning("Arquivo das últimas 5 corridas não encontrado. Rode o ETL.")

st.markdown("---")

# --------------------------------------------------------------------------------------
# Seção: Últimas 10 — Duelos & Predição
# --------------------------------------------------------------------------------------
st.subheader("🤖 Duelos (10 corridas) & Predição (antes da última)")

df_feat = load_parquet(feat_path)
df_pred = load_parquet(pred_path)

if df_feat is not None and not df_feat.empty:
    st.markdown("**Features do duelo (VER - HAM)**")
    view_cols = [c for c in df_feat.columns if c not in []]
    st.dataframe(df_feat[view_cols].sort_values(by="round"))

    # Linha do tempo simples de quem terminou à frente
    if "target_ver_beats_ham" in df_feat.columns:
        timeline = df_feat[["round", "race_name", "target_ver_beats_ham"]].copy()
        timeline["vencedor"] = timeline["target_ver_beats_ham"].map({1: "VER", 0: "HAM"})
        st.markdown("**Vencedor do duelo por corrida (1=VER, 0=HAM)**")
        st.dataframe(timeline.sort_values(by="round"))

else:
    st.warning("Features de duelo (últimas 10) não encontradas. Rode o ETL.")

if df_pred is not None and not df_pred.empty:
    st.markdown("**Predição na última corrida**")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Probabilidade VER vencer", f"{df_pred.iloc[0]['proba_ver']:.3f}")
    with c2:
        st.metric("Probabilidade HAM vencer", f"{df_pred.iloc[0]['proba_ham']:.3f}")

    met_cols = [c for c in ["accuracy_test", "auc_test"] if c in df_pred.columns]
    st.write("**Métricas (teste na última corrida):**")
    st.dataframe(df_pred[["race_name", "y_true", "y_pred"] + met_cols])

    st.caption("Obs.: AUC pode ficar indisponível por amostra de teste única; ver logs do ETL.")
else:
    st.warning("Predições não encontradas. Rode o ETL para gerar o arquivo de predições.")


# --------------------------------------------------------------------------------------
# Observações finais
# --------------------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "Observação: se alguns campos/telemetria não existirem para certas corridas, "
    "o ETL registra fallbacks nos logs e pode reduzir a robustez do modelo."
)
