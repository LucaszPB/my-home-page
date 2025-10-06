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

# ---------- Breve introdução  ----------
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
st.markdown("### 🧑‍💼 Apresentação")
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
- Criação de insights e recomendações com IA para apoiar gerentes PJ na gestão de carteira.
- Co-liderança da migração analítica on-premises (SAS/SQL) → AWS (Glue, Athena), com padronização de queries e pipelines para preservar séries históricas.
- Responsável pela incubadora de IA Generativa na comunidade de ferramentas do time comercial PJ.
- Exploração de ia generativa (RAG) e orquestração para dar insights de carteira para o gerente PJ afim de garantir a máxima performance.
- Estruturação de materiais executivos para superintendência e diretoria comercial PJ, trazendo direcionamentos data-driven.
- Atuação em agendas de Analytics Lead e Data Lead (2024–2025), como ponto focal na disseminação da cultura de dados para a comunidade de atendimento.
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

achievements = [
    {
        "title": "4× PRAD",
        "desc": "Reconhecimento por alta performance no Banco Itaú.",
    },
    {
        "title": "Jornada do Cliente",
        "desc": (
            "Mapeamento de jornada para ofertas de crédito imobiliário, combinando "
            "dados transacionais e insights de atendimento para gerar abordagens "
            "mais relevantes."
        ),
    },
    {
        "title": "Redução de Fraude",
        "desc": "Biometria de voz + backoffice, mais de R$ 50MM de retorno.",
    },
    {
        "title": "Governança de Dados",
        "desc": (
            "Estruturação de ambientes, padrões e qualidade, aliando a migração "
            "on-premises → AWS e Tableau → QuickSight."
        ),
    },
]

cards_per_row = 2
for start in range(0, len(achievements), cards_per_row):
    row = achievements[start : start + cards_per_row]
    columns = st.columns(len(row), gap="large")
    for column, card in zip(columns, row):
        with column:
            with st.container(border=True):
                st.markdown(f"#### :blue[{card['title']}]")
                st.write(card["desc"])

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
- *FGV* — Finanças Internacionais e Macroeconomia
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