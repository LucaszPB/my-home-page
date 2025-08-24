#
"""
Codigo desenvolido por lucas pereira brito 15/08/2025
"""

import streamlit as st
from pathlib import Path

# ---------- Cabeçalho ----------
st.markdown("## 📄 Currículo Online")
st.divider()


def _resolve_pdf():
    # 1) Caminho quando o app é executado a partir do root do repositório
    p1 = Path("assets/cv_lucas_pereira_brito_2025.pdf")
    # 2) Caminho relativo a este arquivo (caso execução mude o CWD)
    p2 = Path(__file__).resolve().parents[1] / "assets" / "cv_lucas_pereira_brito_2025.pdf"
    return p1 if p1.exists() else p2

pdf_path = _resolve_pdf()

# ---------- Nome + Dados (curto) ----------
# 
st.markdown(
    """
## *Lucas Pereira Brito*
*Data Analyst SR*
""")

# Criando colunas
col1, col2 = st.columns([2,2])
with col1:
    st.markdown("📍 São Paulo, SP")
    st.markdown("📱 +55 11 95203-7792")
with col2:
    st.markdown("📧 [brito.luucas@hotmail.com](mailto:brito.luucas@hotmail.com)")
    st.markdown("🔗 [linkedin.com/in/lucaspereirabrito](https://www.linkedin.com/in/lucaspereirabrito)")


st.divider()

# ---------- Apresentação (Resumo) ----------
st.markdown("### 🧑🏻 Apresentação")
st.markdown(
    """
Engenheiro apaixonado por dados e analytics, com mais de **5 anos de experiência** no setor financeiro.

Atuei em **pipelines de dados**, **governança**, **modelos preditivos**, **IA generativa** e **speech analytics** para clientes *PF* e *PJ*.

Tenho experiência em *observability, governança, qualidade e performance de dados*. Utilizando ferramentas de Data Quality, estrutura de Data Governance e Responsible AI para garantir que os projetos tenham o máximo de valor agregado e estejam de acordo com.

Possuo *sólido conhecimento de negócio, especialmente em **produtos bancários** , **crédito**,**CX em Interacoes B2C e B2B**, e gosto de **transformar dados em soluções de valor**.

Sou movido pela *paixão por dados* e pelo desejo de *contribuir para o mercado financeiro, explorando áreas como **crédito, **mesa quantitativa* e *assets* — sempre usando dados para gerar *produtividade* e *busca por transformar dados em valor*.
""".strip()
)

st.divider()

# ---------- Experiências (primeiro bloco após apresentação) ----------
st.markdown("### 💼 Experiências Profissionais")
1
# Experiência atual
st.markdown("🏦 *Itaú Unibanco — Data Analyst SR*  \n*04/2024 – Presente*")
with st.expander("Detalhes da experiência", expanded=True):
    st.markdown(
        """
- Consolidei *visão única de carteira PJ* (CNPJ, segmento, produtos, limite vs utilização*) utilizada em rituais executivos do comercial PJ (resultados: LAIR, ROE).
- *Co-liderança* na transição de bases analíticas *on-prem (SAS, SQL) → AWS (Glue, Athena, S3)*, padronizando queries e pipelines para preservar séries históricas relevantes ao time comercial.
- *Liderança em IA Generativa* na comunidade de ferramentas do time comercial PJ.
- *Mentoria de novos analistas* em práticas de análise de dados, governança e qualidade, promovendo uma cultura de dados sólida.
- *Desenvolvimento de dashboards* para monitoramento de performance comercial, utilizando *AWS QuickSight*.
- *Uso de agile(Scrum)* em projetos, priorizando entregas de alto impacto e alinhamento com stakeholders.
        """.strip()
    )

# Experiência anterior
st.markdown("🏦 *Itaú Unibanco — Analista de Dados e Analytics PL*  \n*06/2022 – 03/2024*")
with st.expander("Detalhes da experiência", expanded=False):
    st.markdown(
            """
        - Definição de *métricas operacionais* (tempo de atendimento, tempo de silêncio, NPS) para a central PF.  
        - Construção de *consultas/ETLs (SQL/Spark)* para painéis operacionais e relatórios periódicos.  
        - Apoio à *padronização de dicionário de dados* e regras de qualidade para reduzir divergências.  
        - *Automação de rotinas* que reduziu esforço manual de extrações recorrentes.
        """
        )

st.markdown("🏦 *Itaú Unibanco — Analista de CX JR*  \n*10/2020 – 05/2022*")
with st.expander("Detalhes da experiência", expanded=False):
    st.markdown(
    """
- Análises de *texto* de chamados PJ/PF para identificar padrões (limite, renegociação, acesso a canais).  
- Relatórios temáticos para squads melhorarem *TMA, TME e tempo de espera*.  
- *Scripts simples (Python/SQL)* para acelerar consolidações de dados.  
- Materiais de *storytelling* para comunicar descobertas de discoverys.
"""
)

st.markdown("🏦 *Itaú Unibanco — Estagiário de CX JR*  \n*10/2019 – 09/2020*")
with st.expander("Detalhes da experiência", expanded=False):
    st.markdown(
        """
    - Sustentação de *alertas* e *modelos de machine learning* focados em texto.  
    - Suporte a estudos analíticos para *aprimoramento de processos*.
    """
    )

st.divider()

# ---------- Conquistas ----------
st.markdown("### 🏆 Conquistas-Chave")

# Tentando me aventurar em HTML, hoje com ajuda do ChatGPT ficou mais fácil hahaha
card_style = """
<style>
.card-container {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.card {
    background: #ffffff;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    padding: 1.2rem;
    flex: 1;
    min-width: 0;
}
.card-title {
    font-weight: bold;
    color: #003A88;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}
.card-desc {
    font-size: 0.98rem;
    color: #000000;
}
</style>
<div class="card-container">
    <div class="card">
        <div class="card-title">4× PRAD</div>
        <div class="card-desc">Reconhecimento anual por alta performance.</div>
    </div>
    <div class="card">
        <div class="card-title">Migração de Dados</div>
        <div class="card-desc">On‑prem → <b>AWS</b> e <b>Tableau → QuickSight</b>.</div>
    </div>
    <div class="card">
        <div class="card-title">Redução de Fraude</div>
        <div class="card-desc">Biometria de voz + backoffice, <b>+ R$ 50MM</b> de retorno.</div>
    </div>
</div>
"""
st.markdown(card_style, unsafe_allow_html=True)
st.divider()

# ---------- Habilidades ----------
st.markdown("### 🧰 Habilidades")
cA, cB = st.columns(2)
with cA:
    st.subheader("Linguagens & Dados")
    st.markdown("- *SQL* — 🔵🔵🔵")
    st.markdown("- *Python* — 🔵🔵🔵")
    st.markdown("- *Spark* — 🔵🔵⚪")
    st.markdown("- *VBA* — 🔵⚪⚪")

    st.subheader("Plataformas & Dataviz")
    st.markdown("- *AWS (Athena, S3, Glue, QuickSight)*- 🔵🔵🔵")
    st.markdown("- *Hadoop* - 🔵🔵⚪")
    st.markdown("- *SQL Server* - 🔵⚪⚪")
    st.markdown("- *SAS* - 🔵🔵⚪")
    st.markdown("- *Git* - 🔵⚪⚪")
    st.markdown("- *Tableau* - 🔵🔵🔵")
    st.markdown("- *Power BI*- 🔵🔵⚪")

with cB:
    st.subheader("IA & Analytics")
    st.markdown("- *NLP*")
    st.markdown("- *IA (RAG)*")
    st.markdown("- *ML (incl. deep learning)*")
    st.markdown("- *Speech Analysis*")

    st.subheader("Conhecimentos e Práticas")
    st.markdown("- *ETL, ELT*")
    st.markdown("- *Data Quality*")
    st.markdown("- *Data Governance*")
    st.markdown("- *Estruturar time de dados*")
    st.markdown("- *Data Storytelling*")
    st.markdown("- *Mentoria*")
    st.markdown("- *Comunicação*")

st.divider()

# ---------- Educação ----------
st.markdown("### 🎓 Educação")
st.markdown(
    """
- *FGV* — Finanças Internacionais e Macroeconomia *(em andamento)*
- *FIAP (MBA)* — Business Intelligence e Analytics  
- *FEI (Graduação)* — Engenharia Mecânica  
- *IFSP (Técnico Integrado)* — Mecânica
"""
)

st.divider()

# ---------- Certificações ----------
st.markdown("### 🪪 Certificações")
st.markdown(
    """
- *AWS Cloud Practitioner*  
- *Vox2You* — Treinamento de Oratória 
- *Green Belt Lean Six Sigma* 
- *Engenharia de Prompts*  
- *Formação Python para Data Science*
- *Practitioner - Generative AI*
- *Desing de Serviços - Trained*
- *Associate - Data Products*
- *Practitioner - Quantum Computing*
- *Associate - Data Engineering*
- *Associate - Analytics Engineering*
- *Practitioner - Leadership D*
- *Mineração de Dados com Python e NLTK (IA Expert Academy)*
"""
)

st.divider()
# ---------- Botão para baixar o PDF ----------
    # Botão de download do PDF.
if pdf_path.exists():
    st.download_button(
         label="⬇️ Baixar currículo (PDF)",
         data=pdf_path.read_bytes(),
         file_name=pdf_path.name,
         mime="application/pdf",
         use_container_width=True,
)
else:
    st.info("PDF do currículo não encontrado em assets/.")

# Fim do arquivo Curriculo.py
# -------------------------------------------------------------