import streamlit as st
from textwrap import dedent

# --------------------------------------
# Página única de Streamlit (para usar dentro de uma sessão/app maior)
# --------------------------------------
st.set_page_config(
    page_title="Arquitetura & Governança de Dados — Visão Prática",
    page_icon="🧭",
    layout="wide",
)

st.title("🧭 Arquitetura & Governança de Dados — Visão Prática")
st.caption(
    "As explicações foram feitas com base em minha experiência prática em projetos de dados e expecializações na área."
)

# Hero / Intro
with st.container():
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.subheader(" que essa página está falando?")
        st.write(
            """
            **Objetivo:** alinhar conceitos de arquitetura de dados, papéis & responsabilidades
            e pilares de governança e como isso tudo flui para que **times de negócio e tecnologia** consigam **construir, operar
            e consumir** dados com segurança, confiabilidade e velocidade.
            """
        )
        st.markdown(
            "- 🔒 **Confiabilidade** (qualidade, segurança, compliance)\n"
            "- ⚡ **Velocidade** (plataforma self-service, automação)\n"
            "- 📈 **Valor** (dados como produto, orientado a domínios)"
        )
    with col2:
        st.info(
            """
            **Escopo da página**\n
            1) Plataforma & Arquitetura (DWH → Data Lake → Data Mesh)  
            2) Camadas (Bronze/Silver/Gold) × (SOR/SOT/SPEC)  
            3) Papéis & Responsabilidades ao longo do ciclo de dados  
            4) Governança (catálogo, qualidade, segurança, LGPD, contratos de dados)  
            5) Fluxo end‑to‑end (app móvel → backend → dados → ML → BI)
            """
        )

# Navegação em abas
aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "🏗️ Plataforma & Arquitetura",
    "🪙 Camadas & SOR/SOT/SPEC",
    "👥 Papéis & Responsabilidades",
    "🛡️ Governança de Dados",
    "🔀 Fluxo end‑to‑end (exemplo prático)",
])

# --------------------------------------
# ABA 1 — Plataforma & Arquitetura
# --------------------------------------
with aba1:
    st.markdown("## 🏗️ Plataforma de Dados & Evolução da Arquitetura")

    with st.expander("📦 Data Warehouse (DW) — a base histórica"):
        st.write(
            """
            **Ideia central:** consolidar dados **estruturados** em um repositório único, estável e consistente
            para **análises corporativas** (ex.: risco de crédito, rentabilidade, P&L, ALM).  
            **Características:** schema‑on‑write, modelagem dimensional (star/snowflake), forte **governança central**,
            SLAs rígidos, performance de consulta otimizada.

            **Forças:** dados consistentes, governança e compliance robustos, ótimo para relatórios regulatórios
            e indicadores corporativos.  
            **Limites:** menos flexível para dados semiestruturados/não estruturados, tempo maior para incorporar
            novas fontes, custos de escala.
            """
        )

    with st.expander("🌊 Data Lake — flexibilidade e escala"):
        st.write(
            """
            **Ideia central:** armazenar grandes volumes de dados **em qualquer formato** (estruturado, semi, não
            estruturado) com **schema‑on‑read**, permitindo exploração, ciência de dados e ML com custo mais baixo.  
            **Características:** storage barato, múltiplos formatos (CSV, Parquet, JSON, logs, eventos), integração
            com frameworks distribuídos e engines SQL.

            **Forças:** alta **flexibilidade**, barata **escala**, ótimo para descoberta e ML.  
            **Limites:** se não houver governança, vira **“data swamp”** (qualidade/linhagem incertas, duplicidade,
            dificuldade de achar a “versão oficial” dos dados).
            """
        )

    with st.expander("🧩 Data Mesh — dados como produto, orientado a domínios (foco)"):
        st.write(
            """
            **Ideia central:** descentralizar a produção/posse dos dados para os **domínios de negócio** (Finanças,
            Crédito, Comercial, Riscos, Operações), tratando **dados como produtos** com donos, SLAs, contratos,
            observabilidade e catálogos; ao mesmo tempo, manter **governança e plataformas** **centralizadas** para
            padrões, segurança e custos.

            **Quatro princípios clássicos:**
            1. **Propriedade orientada a domínios:** cada domínio **produz e opera** seus produtos de dados.  
            2. **Dados como produto:** claro **público‑alvo**, **SLO/SLAs**, documentação, versionamento e roadmap.  
            3. **Plataforma self‑service:** componentes reutilizáveis (ingestão, transformação, catálogo, lineage,
               qualidade, orquestração, observabilidade, feature store).  
            4. **Governança federada computacional:** políticas **automatizadas** (segurança/LGPD, nomenclatura,
               versionamento, qualidade mínima), auditáveis e aplicadas por tooling.

            **Modelo híbrido pedido:**  
            - **Governança centralizada:** políticas, padrões, catálogo corporativo, gestão de acessos, auditoria.  
            - **Produtos de dados descentralizados:** domínio **Finanças** é dono do **Produto de Dados de Finanças**
              (definições, regras, SLAs), **Crédito** do produto de Crédito, e assim por diante.  

            **Benefício prático:** equipes de negócio passam a **publicar** dados confiáveis (com contrato), em vez de
            apenas “entregar extrações”. Isso **reduz atrito**, acelera time‑to‑value e melhora a qualidade sistêmica.

            **Limites:** requer **cultura de produto**, maturidade técnica (automação, testes, CI/CD) e governança bem robusta para garantir que os dados não tenham duplicidade e principalmente estejam disponíveis com qualidade e segurança, para todos.
            """
        )

    st.markdown("---")
    st.subheader("🔗 Como tudo se conecta na prática")
    st.markdown(
        """
        - **DW e Data Lake** convivem: o lake dá **escala/flexibilidade**; o DW (ou **camada Gold**) entrega **verdades
          corporativas** para relatórios críticos.  
        - O **Data Mesh** organiza **quem faz o quê**: domínios **possuem** produtos de dados; a **plataforma** provê
          automação e governança; a **área central** regula padrões e segurança.
        """
    )
    st.markdown("Links úteis:")
    st.markdown("- [Explicação do Data Mesh](https://medium.com/data-hackers/data-mesh-indo-al%C3%A9m-do-data-lake-e-data-warehouse-465d57539d89)")
    st.markdown("- [Explicação do Data lake](https://azure.microsoft.com/pt-br/resources/cloud-computing-dictionary/what-is-a-data-lake)")

    st.subheader("Opinião pessoal")

    st.write(
        """
        - O modelo de data mesh é bastante interessante, mas exige **maturidade técnica e cultural**. Para evitar que os dados sejam tratados de forma paralela (como em planilhas Excel ou relatórios fora do fluxo oficial), é fundamental observar três pontos principais:

        1. **Disponibilidade dos dados:** garantir que os dados estejam acessíveis e atualizados para todos os domínios.
        2. **Facilidade de compartilhamento:** criar frameworks estruturados que permitam a qualquer pessoa, mesmo com pouca experiência, publicar bases de dados com descritivos e documentação de forma simples e escalável. Com o avanço da IA generativa, a documentação tende a se tornar cada vez mais fácil e automatizada.
        3. **Governança:** este é o ponto mais crítico. É necessário um time dedicado e ferramentas que automatizem processos de governança, evitando que o ambiente se torne um “data swamp”.

        Por fim, o aspecto mais importante é a **responsabilidade sobre o dado**. É essencial definir claramente quem é o responsável pela informação, pois dados sem um “dono” definido tendem a ser menos confiáveis, dificultando a tomada de decisão baseada em informações seguras.
        """
    )


# --------------------------------------
# ABA 2 — Camadas & SOR/SOT/SPEC
# --------------------------------------
with aba2:
    st.markdown("## 🪙 Camadas de Dados × Fontes de Verdade")

    st.markdown(
        """
        **Glossário rápido**  

        - **Bronze (Raw/Landing):** dados **brutos**, imutáveis, como vieram da fonte.  
        - **Silver (Cleansed/Conformed):** dados **limpos e padronizados**, com chaves, tipos e regras de qualidade.  
        - **Gold (Curated/Analytics/BI):** dados **modelados para consumo**, métricas consolidadas, dimensões e fatos.  

        - **SOR — Source of Record:** registro **transacional**/operacional **oficial** (ex.: core bancário, ERP).  
        - **SOT — Source of Truth:** visão **curada e padronizada** para decisões corporativas (ex.: rentabilidade
          oficial, carteira ativa). Geralmente **Gold**/**DW**.  
        - **SPEC — Specialized:** **marts**/visões **especializadas** para casos de uso (BI, APIs de dados, sandboxes),
          com otimizações de desempenho e formas de acesso sob demanda.
        """
    )

    st.markdown("### Mapeamento prático")

    # Dados da tabela
    dados = [
        {
            "Camada": "🟫 Bronze (Raw)",
            "Ligação": "Aproxima-se de SOR (espelho/CDC/landing)",
            "Conteúdo": "Bruto, imutável, com metadados de origem/ingestão",
            "Boas práticas": "Particionamento, esquema de versionamento, catálogo e lineage",
        },
        {
            "Camada": "⬜ Silver (Cleansed)",
            "Ligação": "Transição Bronze→Gold; base para padronização",
            "Conteúdo": "Tipos/coerência validados, regras de qualidade, conformidade de chaves",
            "Boas práticas": "Testes de DQ automatizados, data contracts, documentação",
        },
        {
            "Camada": "🟨 Gold (Curated/DW)",
            "Ligação": "Tipicamente SOT (verdade corporativa)",
            "Conteúdo": "Métricas oficiais, dimensões/fatos, granularidades definidas",
            "Boas práticas": "Controle de mudança, SLO/SLAs, versionamento de métricas",
        },
        {
            "Camada": "🟦 SPEC (Especializada)",
            "Ligação": "Consumo especializado (marts/serving)",
            "Conteúdo": "Visões por público (ex.: Comercial, Risco, Finanças)",
            "Boas práticas": "Segregação de acesso, caching, catálogos, contratos de consumo",
        },
    ]

    # Tabela
    st.table(dados)

    st.markdown(
        """
        **Ligação com visualizações e databases**  

        - O **SPEC** costuma abastecer **dashboards** (ex.: QuickSight/Power BI), **APIs de dados**, e **serviços** de
          consumo (ex.: apps, portais).  
        - **Gold/SOT** é a referência **corporativa** (indicadores oficiais).  
        - **Silver** serve para **reuso** e manutenção de coerência.  
        - **Bronze** garante **rastreabilidade** e auditoria.
        """
    )

    st.subheader("Opinião pessoal")

    st.write("""
        - Na prática, as camadas de dados nem sempre seguem rigidamente o padrão Bronze → Silver → Gold. Muitas vezes, há confusão quando camadas Gold são criadas sobre outras Gold, o que pode dificultar a rastreabilidade dos dados e gerar dependências entre áreas que não deveriam existir. Isso ocorre porque o uso da informação pode acontecer em diferentes momentos do ciclo de vida do dado.
        - Entre todas as camadas, a SOT (Source of Truth) é a mais relevante no dia a dia, pois serve como referência oficial para todos os produtos de dados, garantindo consistência e confiança.
        - Já a camada SPEC é onde o valor do dado é extraído, transformando a matéria-prima em impacto real para o negócio, por meio de visões especializadas e produtos direcionados.
    """)

# --------------------------------------
# ABA 3 — Papéis & Responsabilidades
# --------------------------------------
with aba3:
    st.markdown("## 👥 Quem faz o quê no ciclo de dados")

    st.markdown(
        """
        **Visão geral humanizada**: do **app** que capta eventos/solicitações, ao **modelo de ML** em produção,
        passando por **engenharia de dados** e **BI** — cada papel tem um foco e um **entregável concreto**.
        """
    )

    st.table([
    {
        "Papel": "Desenvolvedor(a) Front-end",
        "Foco": "Transformar necessidades do usuário em telas simples e rápidas de usar. Menos cliques, menos fricção, mais clareza — para qualquer pessoa conseguir fazer o que precisa sem se perder.",
        "Entregáveis": "Interfaces, instrumentação de eventos, acessibilidade",
        "KPIs": "Conversão, latência de UI, erros de UX",
    },
    {
        "Papel": "Desenvolvedor(a) Back-end / Eng. de Software",
        "Foco": "Fazer o sistema “aguentar o tranco” e responder do jeito certo. Regras de negócio confiáveis, dados salvos com segurança e respostas previsíveis, mesmo quando o volume cresce.",
        "Entregáveis": "APIs escaláveis, logs/telemetria, contratos (OpenAPI)",
        "KPIs": "Disponibilidade, throughput, SLO de API",
    },
    {
        "Papel": "Eng. de Dados",
        "Foco": "Garantir que os dados cheguem completos, no horário e do jeito certo. Evitar surpresas e retrabalho; facilitar confiar e reutilizar os dados no dia a dia.",
        "Entregáveis": "Pipelines Bronze→Silver→Gold, testes de DQ, lineage",
        "KPIs": "Confiabilidade (SLAs), custo/eficiência, falhas por pipeline",
    },
    {
        "Papel": "Eng. de Analytics (Analytics Engineer)",
        "Foco": "Traduzir perguntas de negócio em tabelas e métricas consistentes. Criar uma base comum para que todos falem o mesmo idioma e não haja “dois números certos”.",
        "Entregáveis": "Marts/Esquemas Gold/SPEC, documentação de métricas",
        "KPIs": "Reuso, consistência de KPIs, satisfação do consumidor",
    },
    {
        "Papel": "Cientista de Dados",
        "Foco": "Descobrir padrões e responder perguntas difíceis com dados. Testar hipóteses, medir impacto e explicar resultados de forma clara para orientar decisões.",
        "Entregáveis": "Features, modelos, notebooks/experimentos documentados",
        "KPIs": "Lift/AUC/KS, impacto de negócio, explainability",
    },
    {
        "Papel": "Eng. de ML (MLOps)",
        "Foco": "Colocar modelos em produção com segurança e manter tudo saudável. Observar desempenho, detectar desvios e corrigir rápido quando algo sai do esperado.",
        "Entregáveis": "Feature store, model registry, inferência online/batch",
        "KPIs": "Drift, latência de predição, tempo de roll-back",
    },
    {
        "Papel": "Data Steward (por domínio)",
        "Foco": "Ser o ponto de verdade do domínio. Deixar nomes e regras dos dados claros, documentados e fáceis de achar — reduzindo dúvidas e ruídos.",
        "Entregáveis": "Dicionário, contratos, SLAs/SLOs, políticas de acesso",
        "KPIs": "DQ (completude, unicidade), tempo de resposta a dúvidas",
    },
    {
        "Papel": "Analista de Dados (BI)",
        "Foco": "Contar a história por trás dos números. Transformar dados em decisões práticas, com painéis que tiram dúvidas e apontam próximos passos com objetividade.",
        "Entregáveis": "Dashboards, semantic layer, guias de uso",
        "KPIs": "Adoção, tempo de resposta, acurácia percebida",
    },
]
)

    st.subheader("Opinião pessoal")

    st.write("""
        Nem todas as empresas possuem essa granularidade de papéis; algumas empresas ou setores contam apenas com o analista de dados, que acaba sendo um faz-tudo, assumindo o papel de todos. Ao fazer isso, cria-se um gargalo enorme, pois o analista de dados não tem a expertise necessária e acaba fazendo fluxos confusos e impossíveis de replicar, gerando um ambiente onde a documentação se torna inviável devido ao volume de demandas que recaem sobre esse profissional.

        Outro ponto é como o analista de dados coexiste com o engenheiro de analytics. Eu acredito que, no futuro, todos os analistas de dados irão se tornar engenheiros de analytics, pois o engenheiro de analytics traduz o problema de negócio em dados com maior maestria e tecnicidade. Porém, como é uma profissão super recente, ainda vão existir casos onde os dois papéis se divergem. Então, o engenheiro de analytics acaba cuidando do pipeline de dados (se tornando um engenheiro de dados) e o analista de dados cuida da parte de BI, virando o construtor dos painéis e deixando de lado a análise dos dados para se tornar um construtor.
    """)
# --------------------------------------
# ABA 4 — Governança de Dados
# --------------------------------------
with aba4:
    st.markdown("## 🛡️ Governança: manter dados úteis, seguros e auditáveis")

    st.markdown(
        """
        **Pilares práticos**  
        - **Catálogo & metadados:** localização, dicionário, dono, propósito, ciclo de vida.  
        - **Qualidade (DQ) & SLO/SLAs:** testes automatizados (completude, unicidade, intervalo, conformidade), alertas.  
        - **Segurança & LGPD:** princípio do **mínimo privilégio**, mascaramento/pseudonimização, retenção & descarte.  
        - **Data Contracts:** esquemas e regras **versionados**, eventos de quebra detectados automaticamente.  
        - **Linhagem (lineage):** rastreabilidade fim‑a‑fim (who‑touched‑what‑when).  
        - **Observabilidade:** saúde dos pipelines (atrasos, falhas, volume anômalo, custo).  
        - **Gestão de custos:** partições, formatos colunares (ex.: Parquet), políticas de ciclo de vida.
        """
    )

    st.markdown("### RACI resumido (exemplo por domínio: Finanças)")
    st.table([
        {"Atividade": "Definir métrica oficial (ex.: Margem Financeira)", "R": "Data Steward Finanças", "A": "Data Owner Finanças", "C": "BI/Analytics", "I": "Governança Central"},
        {"Atividade": "Pipeline Bronze→Silver", "R": "Eng. de Dados", "A": "Data Owner Finanças", "C": "Governança Central", "I": "BI/Analytics"},
        {"Atividade": "Publicar Produto de Dados (SPEC)", "R": "Data Steward Finanças", "A": "Data Owner Finanças", "C": "BI/Segurança", "I": "Demais domínios"},
        {"Atividade": "Controle de acesso LGPD", "R": "Segurança/Privacidade", "A": "Governança Central", "C": "Data Steward", "I": "Usuários finais"},
    ])

    with st.expander("Checklist de prontidão de um Produto de Dados (use no dia a dia)"):
        st.checkbox("Definições e dicionário publicados no catálogo")
        st.checkbox("Contratos de dados (schema + regras) versionados e testados")
        st.checkbox("Testes de DQ (Data Quality) automatizados (completude/intervalo/unicidade)")
        st.checkbox("Métricas com SLO/SLAs e dashboard de saúde do dado")
        st.checkbox("Regras LGPD aplicadas (mínimo privilégio, mascaramento, retenção)")
        st.checkbox("Custos monitorados (partições, formatos colunares, ciclo de vida)")

# --------------------------------------
# ABA 5 — Fluxo end‑to‑end (exemplo prático)
# --------------------------------------
with aba5:
    st.markdown("## 🔀 Exemplo prático: app móvel → backend → dados → ML → BI")
    st.caption("Fluxograma simplificado com os papéis principais em cada etapa.")

    dot = dedent(
        r"""
        digraph G {
          rankdir=LR;
          fontsize=12;
          node [shape=rectangle, style=rounded, fontname=Helvetica];

          subgraph cluster_app {
            label="Aplicativo (Front‑end)"; color=lightgrey;
            app[ label="App Mobile\n(Dev Front‑end)" ];
          }

          subgraph cluster_backend {
            label="APIs & Transacional"; color=lightgrey;
            api[ label="APIs REST/GraphQL\n(Dev Back‑end)" ];
            txdb[ label="Banco Transacional\n(Back‑end/DBA)" ];
          }

          subgraph cluster_data {
            label="Plataforma de Dados"; color=lightgrey;
            ingest[ label="Ingestão (batch/CDC/stream)\n(Eng. de Dados)" ];
            bronze[ label="Bronze/SOR (Raw/Landing)" ];
            silver[ label="Silver (Cleansed/Conformed)" ];
            gold[ label="Gold (Curated/DW) — SOT" ];
            spec[ label="SPEC (Marts/Serviços)" ];
          }

          subgraph cluster_ml {
            label="Analytics & ML"; color=lightgrey;
            feat[ label="Feature Store\n(Eng. de ML)" ];
            train[ label="Treino/Validação\n(Cientista de Dados)" ];
            registry[ label="Model Registry\n(Eng. de ML)" ];
            serving[ label="Serving/Inferência\n(Eng. de ML)" ];
          }

          subgraph cluster_consumo {
            label="Consumo"; color=lightgrey;
            bi[ label="Dashboards / APIs de Dados\n(BI/Analytics)" ];
            apps[ label="Apps/Serviços Consumidores\n(Domínios de Negócio)" ];
          }

          # Conexões
          app -> api -> txdb;
          txdb -> ingest -> bronze -> silver -> gold -> spec;
          silver -> feat;
          feat -> train -> registry -> serving;
          spec -> bi;
          serving -> apps;
          spec -> apps;
        }
        """
    )

    st.graphviz_chart(dot, use_container_width=True)

    st.markdown("### Descrição do fluxo")
    st.markdown(
        """
        1. **Usuário usa o app** (ex.: solicitação de limite/transferência). O **Front‑end** instrumenta eventos.  
        2. **Back‑end/APIs** validam regras e persistem no **banco transacional (SOR)**.  
        3. A **Engenharia de Dados** ingere (CDC/batch/stream) para **Bronze**, aplica regras e validações em **Silver**,
           e modela **Gold** (tipicamente a **SOT** corporativa).  
        4. A camada **SPEC** expõe **marts** e **serviços** para BI, APIs de dados e casos especializados.  
        5. **Cientistas de Dados** criam features e modelos; **Eng. de ML** publica em produção (serving/monitoramento).  
        6. **Dashboards** e **Apps** consomem **SPEC** e/ou **inferências** do modelo com governança, qualidade e custo sob controle.
        """
    )

st.markdown("---")
st.success(
    "Dica final: comece pequeno (um domínio, um produto de dados), publique contratos, monitore qualidade/custos e \n"
    "evolua para o modelo federado com governança central — **velocidade com segurança**."
)
