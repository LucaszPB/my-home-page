# =========================================================
# Código de Macroeconomia e Dados
# =========================================================

import os  # Biblioteca padrão do Python para manipulação de caminhos e diretórios
import pandas as pd  # Pandas: principal biblioteca para manipulação e análise de dados em formato tabular (DataFrames)
import numpy as np  # Numpy: biblioteca para cálculos numéricos eficientes (vetores, matrizes, funções matemáticas)
import streamlit as st  # Streamlit: framework para criar aplicações web interativas de forma simples e rápida (dashboard/data apps)
import plotly.express as px  # Plotly Express: módulo simplificado do Plotly para criar gráficos interativos com poucas linhas de código
import plotly.graph_objects as go  # Plotly Graph Objects: módulo mais detalhado/flexível do Plotly, que permite customizar gráficos interativos em maior profundidade

# Importa bibliotecas estatísticas específicas para séries temporais
from statsmodels.tsa.stattools import adfuller  # Teste de estacionariedade ADF
from statsmodels.tsa.api import VAR             # Modelo VAR
from statsmodels.tsa.vector_ar.vecm import coint_johansen, VECM  # Cointegração e modelo VECM


# ======= CONFIG =======
# AVISO: Se sua estrutura de projeto for diferente, estou saindo da estrutura.
DATA_DIR = os.path.join("assets", "macro_br")
MERGED_FILE = os.path.join(DATA_DIR, "merged_macro_br.csv")
# ======================

# Configuração da página Streamlit:
# - page_title: título da aba do navegador
# - layout="wide": usa layout mais largo para aproveitar a tela
st.set_page_config(page_title="Macro Brasil — VAR & VECM", layout="wide")
st.title("📈 Macro Brasil — Análise rápida (VAR & VECM)")

# Texto explicativo curto sobre o que a página faz.
# Aqui é apenas um markdown com instruções e descrição para o usuário.
st.markdown(
    """
**O que esta página faz?**  
- Explicada os indicadores macroeconômicos diretos do banco mundial ( Indicadores v'ao estar com bases globais e n'ao bases nacionais devido a API ) e traz umm gráfico com o histórico   
- Mostra um **gráfico de linha** do indicador principal nos.  
- Executa **ADF**, **VAR** e **VECM** (decide com base em cointegração).  
- Exibe **códigos** (ocultos em expanders), **gráficos** e **conclusões**.
    """
)

# Verifica se o arquivo merged existe. Se não existir, exibe erro e interrompe a execução.
# Isso evita erros posteriores ao tentar ler um arquivo inexistente.
if not os.path.exists(MERGED_FILE):
    st.error(
        f"Arquivo não encontrado: `{MERGED_FILE}`.\n\n"
    )
    st.stop()

# Carrega o CSV "merged" que contém todos os indicadores macro necessários.
# Espera-se que o CSV tenha pelo menos a coluna "year" e várias colunas de séries.
dfm = pd.read_csv(MERGED_FILE)

# Validação: o CSV deve conter a coluna 'year'. Se não tiver, mostra erro e para a execução.
if "year" not in dfm.columns:
    st.error("CSV merged não possui coluna 'year'. Verifique o arquivo.")
    st.stop()

# ===== Ajustes básicos no dataframe =====
# - copia para evitar alterar o original
# - ordena por year (importante para séries temporais)
# - remove colunas totalmente vazias
dfm = dfm.copy()
dfm = dfm.sort_values("year")
dfm = dfm.dropna(how="all", axis=1)  # remove colunas totalmente vazias

# Lista de indicadores disponíveis (todas as colunas menos "year").
# Usada para popular o selectbox que escolhe o indicador principal.
indicadores_disponiveis = [c for c in dfm.columns if c != "year"]

# Validação: precisamos de ao menos 2 indicadores para modelagem VAR/VECM.
# Se tiver menos, informamos o usuário e paramos a execução.
if len(indicadores_disponiveis) < 2:
    st.error("São necessários pelo menos 2 indicadores no merged para modelar. Baixe mais séries.")
    st.stop()

# Pequeno divisor visual na interface Streamlit.
st.divider()

st.subheader("***Análise de indicadores macroeconômicos***")

# Caixa de seleção para o usuário escolher qual indicador será mostrado
# como "indicador principal" (gráfico + explicação).
# index=0 define o primeiro item como selecionado por padrão.
indicador_principal = st.selectbox("📌 Indicador principal (gráfico + explicação):", indicadores_disponiveis, index=0)


# Explicações mais elaboradas dos indicadores macroeconomicos 
explicacoes = {
  'Inflação (CPI, % a.a.)': """Mostra quanto, em média, os preços pagos pelas famílias subiram nos últimos 12 meses.
- Origem do número: Banco Mundial (API: "FP.CPI.TOTL.ZG")
- Por que importa? Se os preços sobem mais rápido que o salário, o poder de compra cai. Inflação baixa e previsível facilita planejar compras, contratos e investimentos.
- De onde vem: choques de oferta (energia, alimentos, câmbio) e/ou demanda aquecida (crédito, renda, emprego). Itens administrados e alimentação costumam gerar oscilações.
- Política: inflação alta e persistente tende a levar o Banco Central a subir juros; inflação ancorada abre espaço para cortes.
- Leitura prática: acompanhe aluguel, mercado (feira/supermercado) e contas de serviços — são bons termômetros do seu custo de vida.
- Exemplo do dia a dia: se gás, arroz e luz sobem ~8% no ano e seu salário aumenta 5%, o orçamento aperta: você compra menos com o mesmo dinheiro.""",

  'PIB real — crescimento (% a.a.)': """Variação do total produzido pelo país, já descontada a inflação (crescimento “de verdade”).
- Origem do número: Banco Mundial (API: "NY.GDP.MKTP.KD.ZG")
- O que indica: acima de 0% = economia expandindo; abaixo de 0% = retraindo (sinal de recessão se persiste).
- Motores do PIB: consumo das famílias, investimento das empresas, gasto público e saldo externo (exportações – importações).
- Por que importa: orienta emprego, renda, lucros, arrecadação e a percepção de risco do país.
- Uso rápido: combine com inflação e juros para ler o ciclo (aquecendo, estável ou esfriando) e ajustar decisões de crédito e investimento.
- Exemplo do dia a dia: PIB em alta costuma trazer mais vagas, obras e vendas; em baixa, comércio mais fraco e contratações lentas.""",

  'Desemprego (% força de trabalho)': """Parcela de pessoas na força de trabalho que querem e procuram emprego, mas ainda não encontraram.
- Origem do número: Banco Mundial (API: "SL.UEM.TOTL.ZS")
- Tipos: friccional (troca de emprego), estrutural (descompasso de qualificação/região) e cíclico (atividade fraca).
- Atenção: desalentados (quem desistiu de procurar) não entram na taxa; subocupação e informalidade podem mascarar fragilidades.
- Relação com o PIB: crescimento reduz desemprego com defasagem; queda muito forte do desemprego pode pressionar salários e, depois, preços.
- Leitura prática: olhe também participação na força de trabalho e subutilização para ter um retrato completo do mercado de trabalho.
- Exemplo do dia a dia: sua amiga pede demissão e passa 2 meses procurando — enquanto busca, ela entra na estatística de desemprego.""",

  'Conta Corrente (% do PIB)': """Placar das trocas do país com o exterior: bens e serviços, rendas (juros/lucros) e transferências.
- Origem do número: Banco Mundial (API: "BN.CAB.XOKA.GD.ZS")
- Leitura: déficit = país gasta mais do que recebe e precisa de financiamento externo; superávit = entra mais do que sai.
- Risco: déficits altos e persistentes, cobertos por dívida de curto prazo, aumentam a vulnerabilidade a choques e a volatilidade cambial.
- Qualidade do financiamento: IED (fábricas/projetos) é mais estável que dívida de curto prazo e tende a apoiar produtividade.
- Efeito prático: contas externas melhores aliviam o câmbio; piores tendem a pressionar dólar, turismo e eletrônicos importados.
- Exemplo do dia a dia: como uma família — se gasta mais do que ganha, recorre a crédito; se sobra, poupa e investe com folga.""",

  'Juros reais (% a.a.)': """Taxa de juros após descontar a inflação (aprox.: juros nominais – inflação esperada/realizada).
- Origem do número: Banco Mundial (API: "FR.INR.RINR")
- Por que importa? É o “custo verdadeiro” do crédito e o ganho real de quem poupa/investe; baliza decisões de financiamento e alocação.
- Política: principal alavanca do Banco Central; acima do juro “neutro” esfria a economia, abaixo estimula atividade e crédito.
- Medição: ex-ante (usa expectativas) ajuda a decidir hoje; ex-post (usa inflação realizada) descreve o que passou.
- Regra prática: juros reais altos encarecem financiamentos ao longo do tempo; mais baixos aliviam o orçamento e favorecem investimentos produtivos.
- Exemplo do dia a dia: empréstimo a 10% a.a. com inflação de 6% → juro real ~4% — o saldo devedor “cresce” em termos reais e pesa no bolso mês a mês.
- OBS: O número da taxa de juros vinda da API não é a mesma da SELIC em questão de valor absoluto, mas a diferença entre elas é praticamente constante ao longo do tempo. Portanto, para análises de séries temporais e modelos VAR/VECM, essa diferença constante não afeta os resultados."""
}


with st.expander("ℹ️ Sobre o indicador selecionado", expanded=True):
    # Exibe um resumo explicativo do indicador selecionado pelo usuário.
    # Usa o dicionário 'explicacoes' definido no topo do arquivo para mostrar
    # uma descrição já pronta, ou um texto genérico se não houver entrada.
    st.markdown(f"**{indicador_principal}** — {explicacoes.get(indicador_principal, 'Indicador macroeconômico do Banco Mundial (série anual).')}")

# ===== Gráfico - Histórico =====
st.subheader("📊 Evolução (histórico completo)")

try:
    # Seleciona apenas as colunas relevantes: ano e o indicador escolhido.
    # dropna() evita anos sem valor para o indicador.
    gdf = dfm[["year", indicador_principal]].dropna().copy()

    if gdf.empty:
        # Caso não existam observações válidas, avisa o usuário.
        st.warning("Sem dados suficientes para este indicador.")
    else:
        # Garantir que o eixo x (year) seja apresentado como string
        # para que o plotly trate cada ano como rótulo categórico e não
        # como número/escala contínua (melhor leitura para séries anuais).
        try:
            # Primeiro tentamos converter para numérico e depois para inteiro,
            # assim evitamos rótulos como '2000.0' caso o CSV venha com floats.
            gdf["year"] = pd.to_numeric(gdf["year"]).astype(int).astype(str)
        except Exception:
            # Se falhar (ex.: formatos estranhos), garantimos ao menos string.
            gdf["year"] = gdf["year"].astype(str)

        # Cria uma coluna auxiliar de rótulos, formatando valores com 2 casas
        # decimais e sufixo '%' para mostrar diretamente sobre os pontos.
        # Isso facilita leitura rápida sem precisar abrir hover.
        gdf["__label"] = gdf[indicador_principal].map(lambda v: f"{float(v):.2f}%")

        # Constrói o gráfico de linha com markers usando plotly express.
        # plotly express cria uma figura pronta e fácil de customizar depois.
        fig = px.line(
            gdf,
            x="year",
            y=indicador_principal,
            markers=True,
        )

        # Ajustes nos traços:
        # - text: mostra o rótulo acima de cada ponto (textposition)
        # - hovertemplate: controla o conteúdo do tooltip com 2 casas decimais
        #   e elimina o texto extra padrão (<extra></extra>).
        fig.update_traces(
            text=gdf["__label"],
            textposition="top center",
            hovertemplate=f"%{{x}}<br>{indicador_principal}: %{{y:.2f}}%<extra></extra>",
        )

        # Layout: títulos de eixos, formato do eixo y com sufixo '%' e margens.
        # tickformat e ticksuffix ajudam a exibir valores percentuais corretamente.
        fig.update_layout(
            xaxis_title="Ano",
            yaxis_title=indicador_principal,
            yaxis=dict(tickformat=".2f", ticksuffix="%"),
            margin=dict(t=20, b=40),
        )

        # Renderiza o gráfico no Streamlit, ajustando à largura do contêiner.
        st.plotly_chart(fig, use_container_width=True)

        # Fonte e período — informação adicional para o usuário.
        st.caption("Fonte: API World Bank. 2000-2024.")
except Exception as e:
    # Em caso de erro em qualquer etapa do plot, mostra uma mensagem amigável
    # com a exceção para facilitar debug.
    st.warning(f"Não foi possível plotar o gráfico: {e}")

# Insere uma linha divisória horizontal na página do Streamlit
st.markdown("---")

# =============================================================
# Inicio Análise de séries temporais VAR e VECM
# =============================================================


# Define o título principal da seção com um emoji e texto descritivo
st.header("📚 Análise de séries temporais VAR e VECM")

# Cria um bloco expansível (accordion) para explicar o teste ADF
with st.expander("📉 ADF — Teste de Raiz Unitária (estacionariedade)", expanded=False):
        # Texto em Markdown explicando o que é o teste ADF,
        # sua importância, como interpretar os resultados e exemplos práticos
        st.markdown(
            """
**O que é?**  
O **ADF (Augmented Dickey–Fuller)** é um teste estatístico para verificar se uma série **é estacionária** (isto é, se não “deriva” ao longo do tempo).  
Em termos simples: ele checa se a série “tem memória de tendência” ou se oscila em torno de um nível médio estável.

**Por que isso importa?**  
Modelos como VAR e VECM **precisam** saber se as séries são estacionárias. Se não forem, é comum **diferenciar** (∆) ou usar **VECM** quando há cointegração.

**Como interpretar (regra prática):**  
- **p-valor < 0,05** → rejeita a hipótese de raiz unitária → **série estacionária** ✅  
- **p-valor ≥ 0,05** → não rejeita a hipótese de raiz unitária → **provável não estacionária** ❌

**Exemplo do dia a dia:**  
Pense no **preço de um imóvel** na sua cidade: ao longo dos anos ele tende a **subir** (tendência). Já a **variação mensal** (alta/queda de um mês para o outro) costuma oscilar perto de zero. O nível de preço é **não estacionário**; a **variação** pode ser **estacionária**.

**Passo a passo (prático):**  
1) Plote a série e avalie tendência/sazonalidade.  
2) Rode o ADF na série em nível.  
3) Se não for estacionária, teste a **primeira diferença** (∆).  
4) Guarde o resultado para decidir entre **VAR em diferenças** ou **VECM** (se houver cointegração).
"""
        )

# Cria outro bloco expansível para explicar o modelo VAR
with st.expander("🔗 VAR — Vetores Autorregressivos (séries estacionárias)", expanded=False):
        # Explicação detalhada sobre o modelo VAR em linguagem simples
        st.markdown(
            """
**O que é?**  
O **VAR** modela várias séries **ao mesmo tempo**, permitindo que **cada variável** dependa de **defasagens de si mesma e das outras**. É ótimo para entender **dinâmicas e interações** (ex.: inflação ↔ juros ↔ atividade).

**Quando usar?**  
- Séries **estacionárias** (em nível ou em diferenças).  
- Você quer **prever**, **medir impactos** (respostas a choques/IRFs) e **analisar causalidade temporal** (Granger).

**Para que serve (na prática):**  
- **Previsões multivariadas**.  
- **IRF** (Impulse Response Function): “se os juros sobem 1 p.p. hoje, como a inflação e o PIB reagem nos próximos meses?”  
- **Decomposição da variância**: “qual variável explica mais a incerteza da inflação?”

**Exemplo do dia a dia:**  
É como observar **trânsito em cruzamentos**: o fluxo de uma avenida (juros) afeta o de outra (inflação), e vice-versa. O VAR aprende esses **efeitos cruzados ao longo do tempo**.

**Passo a passo (prático):**  
1) Garanta estacionariedade (ADF).  
2) Escolha **lags** (AIC/BIC).  
3) Ajuste o VAR e **valide resíduos** (autocorrelação, normalidade).  
4) Gere **IRFs** e **previsões**; interprete economicamente.
"""
        )

# Cria outro bloco expansível para explicar o modelo VECM
with st.expander("⚖️ VECM — VAR com Correção de Erro (cointegração)", expanded=False):
        # Explicação em markdown sobre quando usar VECM e sua lógica
        st.markdown(
            """
**O que é?**  
O **VECM** é um VAR “especial” para séries **não estacionárias** que possuem **relacionamento de longo prazo** (cointegração).  
Ele separa **curto prazo** (diferenças) de **longo prazo** (termo de correção de erro que “puxa” as séries de volta ao equilíbrio).

**Quando usar?**  
- Séries **I(1)** (não estacionárias em nível, mas estacionárias na primeira diferença).  
- Existe **cointegração** (teste de Johansen indica pelo menos 1 vetor cointegrante).

**Para que serve (na prática):**  
- Modelar sistemas onde há **equilíbrio de longo prazo** (ex.: juros reais, inflação e câmbio; preços e custos; renda e consumo).  
- Entender **ajustes**: quem “corrige” o desvio e **com que velocidade**.

**Exemplo do dia a dia:**  
Pense em dois amigos que caminham juntos: cada um pode se adiantar ou atrasar (curto prazo), mas como estão **amarrados por uma conversa**, naturalmente **voltarem a ficar lado a lado** (longo prazo). O VECM modela essa “amarra”.

**Passo a passo (prático):**  
1) Mostre que as séries são **I(1)** (ADF nas séries e nas diferenças).  
2) Rode **Johansen** para testar **cointegração** e encontrar o(s) vetor(es) de longo prazo.  
3) Ajuste o **VECM** (escolha de lags + rank).  
4) Analise **coeficientes de ajuste**, **IRFs**, **previsões** e **diagnósticos**.
"""
        )

# Cria um último bloco expansível com o "roteiro" completo de análise
with st.expander("🧭 Roteiro de análise (do zero ao resultado)", expanded=False):
        # Passo a passo resumido para análise prática
        st.markdown(
            """
**1) Exploração inicial**  
- Plotar séries, olhar tendência/sazonalidade, checar outliers e data gaps.

**2) Testes de estacionariedade (ADF)**  
- Em **nível** e **primeira diferença**.  
- Decidir: **VAR** (se estacionária) ou **VECM** (se I(1) com cointegração).

**3) Cointegração (se necessário)**  
- Teste de **Johansen** → defina **rank** (nº de relações de longo prazo).

**4) Escolha de defasagens (lags)**  
- Usar **AIC/BIC/HQIC** para selecionar lags ótimos.

**5) Ajuste do modelo**  
- **VAR** (em níveis se estacionário; em diferenças se não).  
- **VECM** (se I(1) + cointegração).  

**6) Diagnósticos**  
- Resíduos (autocorrelação/heteroscedasticidade).  
- Estabilidade (raízes do polinômio).  

**7) Interpretação & uso**  
- **IRFs** (respostas a choques) e **decomposição da variância**.  
- **Previsões** (curto prazo) com intervalos.  
- **Histórias econômicas**: conecte achados aos fatos (política monetária, choques externos, etc.).
"""
        )

# Cria um subtítulo que provavelmente será seguido de código de teste ADF aplicado a dados reais
st.subheader("🧪 Teste de Estacionariedade (ADF)")

# Função para rodar o teste ADF (Augmented Dickey-Fuller) em uma série temporal
def run_adf_show(x: pd.Series):
    # Converte os valores da série para numérico (se houver strings, converte ou descarta),
    # e remove valores ausentes (NaN)
    x = pd.to_numeric(x, errors="coerce").dropna()
    try:
        # Executa o teste ADF com critério de seleção de defasagens baseado no AIC
        # O adfuller retorna: estatística do teste, p-valor e outros resultados
        stat, pval, *_ = adfuller(x, autolag="AIC")
        # Retorna os resultados principais (estatística e p-valor) já convertidos para float
        return {"stat": float(stat), "pvalue": float(round(pval, 4))}
    except Exception as e:
        # Caso o teste dê erro (ex.: série muito curta), retorna NaN e o erro capturado
        return {"stat": np.nan, "pvalue": np.nan, "err": str(e)}

# Lista de indicadores econômicos que serão analisados no teste ADF
indicadores_focus = [
    "Inflação (CPI, % a.a.)",
    "PIB real — crescimento (% a.a.)",
    "Desemprego (% força de trabalho)",
    "Conta Corrente (% do PIB)",
    "Juros reais (% a.a.)"
]

# Loop para exibir os resultados do ADF em layout de 2 colunas no Streamlit
# Percorre a lista de indicadores de 2 em 2
for i in range(0, len(indicadores_focus), 2):
    # Cria duas colunas lado a lado
    cols = st.columns(2)
    # Itera sobre cada coluna preenchendo com um indicador (se existir)
    for j, col in enumerate(cols):
        if i + j < len(indicadores_focus):
            ind = indicadores_focus[i + j]  # Nome do indicador atual
            with col:  # Renderiza dentro da coluna correspondente
                # Verifica se o indicador está presente no DataFrame "dfm"
                if ind in dfm.columns:
                    # Executa o ADF na série do indicador
                    res = run_adf_show(dfm[ind])
                    # Caso o p-valor seja NaN (erro ou série inválida)
                    if np.isnan(res["pvalue"]):
                        # Mostra estatística, p-valor e erro retornado pela função
                        st.write({"stat": res["stat"], "pvalue": res["pvalue"], "err": res.get("err")})
                    else:
                        # Caso o teste rode normalmente, mostra resultados formatados
                        st.write(
                            {
                                "indicador": ind,  # Nome do indicador
                                "stat": round(res["stat"], 4),  # Estatística do teste ADF
                                "pvalue": round(res["pvalue"], 4),  # P-valor
                                # Interpretação prática: estacionária se p < 0.05
                                "Resultado": "✅ Estacionária" if res["pvalue"] < 0.05 else "❌ Não estacionária",
                            }
                        )
                else:
                    # Caso a coluna não exista no CSV, mostra aviso
                    st.write(f"**{ind}** não encontrado no CSV.")

# Linha divisória na página
st.markdown("---")

# Subtítulo para indicar a seção do teste ADF
st.subheader("🧪 Teste de Estacionariedade (ADF)")

# ========== Opção de limpeza via BOTÕES ==========
# Cria um título/legenda na tela para a seção de "Limpeza de Dados"
st.markdown("### 🧹 Opção de limpeza de dados")

# Divide a tela em duas colunas (para os botões de escolha)
left, right = st.columns(2)

# Cria uma variável de estado no Streamlit para guardar a escolha do usuário
# "apply_cleaning" indica se a limpeza deve ser aplicada ou não
if "apply_cleaning" not in st.session_state:
    st.session_state.apply_cleaning = False  # valor padrão = não aplicar limpeza

# Coluna da esquerda → opção de NÃO aplicar limpeza
with left:
    if st.button("Usar **sem** limpeza (padrão)", use_container_width=True):
        # Se o usuário clicar nesse botão, atualiza a flag no session_state
        st.session_state.apply_cleaning = False

# Coluna da direita → opção de APLICAR limpeza
with right:
    if st.button("Aplicar **limpeza** agora", use_container_width=True):
        # Se o usuário clicar nesse botão, ativa a flag de limpeza
        st.session_state.apply_cleaning = True

    # Texto explicativo abaixo do botão, em formato de legenda/caption
    st.caption(
        "🧹 **Limpeza:** tiro os anos totalmente atípicos que aconteceram entre 2000 e 2024 "
        "(ex.: 2008-2009 [crise global], 2020 [pandemia]) e removemos saltos ano-a-ano maiores que **3 p.p.** "
        "Por quê? Pra evitar que choques distorçam ADF/VAR/VECM e deixar as "
        "previsões mais estáveis e fáceis de ler."
    )




# Função para rodar o teste ADF (Augmented Dickey-Fuller)
def run_adf(x: pd.Series) -> dict:
    # Converte a série para numérico (caso venha com strings) e remove valores ausentes
    x = pd.to_numeric(x, errors="coerce").dropna()
    try:
        # Executa o teste ADF com:
        # - autolag="AIC": escolhe o número ótimo de defasagens usando critério AIC
        # - maxlag = mínimo entre 8 e 1/3 do tamanho da série (evita sobreajuste em séries curtas)
        stat, pval, *_ = adfuller(x, autolag="AIC", maxlag=min(8, int(len(x) / 3)))
        
        # Retorna estatística do teste e p-valor como floats
        return {"stat": float(stat), "pvalue": float(pval)}
    except Exception:
        # Caso o teste não rode (ex.: série muito curta, problemas de dados),
        # retorna NaN para facilitar o tratamento na visualização
        return {"stat": np.nan, "pvalue": np.nan}



# Função simples de limpeza de dados
def simple_clean(df: pd.DataFrame, cols: list,
                 anos_excluir=(2008, 2009, 2020),  # anos fixos a remover (choques conhecidos)
                 pp_threshold: float = 3.0):       # limiar em pontos percentuais para detectar outliers
    # Cria cópia do DataFrame para não alterar o original
    base = df.copy()

    # Remove anos fixos pré-definidos (ex.: crise de 2008, 2009 e pandemia em 2020)
    anos_fix = [a for a in anos_excluir if a in set(base["year"])]
    if anos_fix:
        base = base[~base["year"].isin(anos_fix)]

    # Conjunto para armazenar anos detectados automaticamente como outliers
    anos_auto = set()

    # Seleciona apenas colunas relevantes (ano + variáveis de interesse),
    # ordena por ano e define "year" como índice
    tmp = base[["year"] + cols].dropna().sort_values("year").set_index("year")

    # Para cada variável, calcula a diferença ano a ano (∆)
    for c in cols:
        dif = tmp[c].diff()  # diferença em relação ao ano anterior
        # Se a variação absoluta for maior que o limite (pp_threshold),
        # marca o ano como outlier automático
        anos_auto.update(tmp.index[(dif.abs() > pp_threshold)].tolist())

    # Ordena a lista de anos outliers automáticos
    anos_auto = sorted(list(anos_auto))

    # Remove os anos identificados automaticamente como outliers
    if anos_auto:
        base = base[~base["year"].isin(anos_auto)]

    # Retorna:
    # - base limpa
    # - anos removidos manualmente (anos_fix)
    # - anos removidos automaticamente (anos_auto)
    return base, anos_fix, anos_auto


# --------------------------------
# Função principal (renderiza tudo)
# --------------------------------
def analyze_pair(df: pd.DataFrame, a: str, b: str, apply_cleaning: bool):
    # Validação: garante que as duas colunas (variáveis escolhidas) existem no DataFrame
    if a not in df.columns or b not in df.columns:
        st.warning(f"Colunas ausentes para {a} vs {b}."); return

    # Seleção / Limpeza de dados
    if apply_cleaning:
        # Aplica limpeza simples:
        # - remove anos "fixos" (choques conhecidos, ex.: 2008/2009/2020)
        # - detecta e remove anos com saltos anuais > 3 p.p. nas colunas analisadas
        df_use, anos_fix, anos_auto = simple_clean(df, [a, b], anos_excluir=(2008, 2009, 2020), pp_threshold=3.0)
        # Se houve remoções, prepara texto para informar no UI (caption/explicação)
        if anos_fix or anos_auto:
            blocos = []
            if anos_fix: blocos.append(f"anos removidos: {anos_fix}")            # removidos manualmente (fixos)
            if anos_auto: blocos.append(f"outliers Δp.p. > 3.0: {anos_auto}")    # removidos automaticamente (saltos)
    else:
        # Sem limpeza: usa a base original
        df_use = df.copy()

    # Monta par numérico (pré-processamento)
    # Seleciona ano + as duas séries, ordena por ano, define índice = year
    tmp = (df_use[["year", a, b]].dropna().sort_values("year").set_index("year")).copy()
    # Garante que as séries estão em formato numérico
    tmp[a] = pd.to_numeric(tmp[a], errors="coerce")
    tmp[b] = pd.to_numeric(tmp[b], errors="coerce")
    # Remove linhas com NaN após coerções e força dtype float
    tmp = tmp.dropna().astype(float)
    # Checagem de tamanho mínimo: abaixo de 8 observações, o ajuste/forecast fica frágil
    if tmp.empty or tmp.shape[0] < 8:
        st.warning(f"Dados insuficientes para {a} vs {b}."); return


    # Decisão por VECM (teste de cointegração de Johansen)

    vecm_ok = False
    try:
        # coint_johansen espera um array numpy; det_order=0: sem determinístico em nível;
        # k_ar_diff=1: 1 defasagem nas diferenças (config simples)
        cj = coint_johansen(tmp.values, det_order=0, k_ar_diff=1)
        # Regra prática: usa a estatística "trace" (lr1) e compara com crítico de 5% (cvt[:,1])
        # Se lr1[0] > cvt[0,1] => pelo menos 1 relação de cointegração (rank >= 1)
        vecm_ok = float(cj.lr1[0]) > float(cj.cvt[0, 1])  # trace > crítico 5%
    except Exception:
        # Se algo falhar no Johansen, cai para a rota VAR
        vecm_ok = False

    # Horizonte de previsão (anos à frente)
    forecast_years = 3
    pred_df, modelo_usado = None, ""

    # ============
    #   VECM
    # ============
    if vecm_ok:
        # Cabeçalho para a seção VECM
        st.subheader(f"🔹 VECM — {a} vs {b}")
        # Mostra um "snippet" do código usado, para transparência pedagógica
        with st.expander("📦 Código usado (VECM)", expanded=False):
            st.code(
                "model = VECM(df_pair, k_ar_diff=1, deterministic='ci')\n"
                "res = model.fit()\n"
                "fc = res.predict(steps=3)\n", language="python")
        try:
            # Ajuste do VECM:
            # - k_ar_diff=1: 1 defasagem nas diferenças
            # - deterministic='ci': intercepto apenas no vetor de cointegração (forma comum)
            model = VECM(tmp, k_ar_diff=1, deterministic="ci")
            res = model.fit()
            # Previsão out-of-sample para N passos (anos)
            fc = res.predict(steps=forecast_years)

            # Constrói índice futuro com base no último ano observado
            last_year = int(tmp.index.max())
            fut_years = list(range(last_year + 1, last_year + 1 + forecast_years))

            # DataFrame de previsões com mesmas colunas e index dos anos futuros
            pred_df = pd.DataFrame(fc, columns=tmp.columns, index=fut_years).astype(float)
            modelo_usado = "VECM"
        except Exception as e:
            # Em caso de erro no ajuste/predict do VECM, informa e habilita fallback para VAR
            st.error(f"Erro no VECM: {e}")
            vecm_ok = False

    # ============
    #   VAR
    # ============
    if not vecm_ok:
        # Cabeçalho para a seção VAR (rota padrão se não houver cointegração)
        st.subheader(f"🔹 VAR — {a} vs {b}")
        # Mostra um "snippet" do código usado, para transparência pedagógica
        with st.expander("📦 Código usado (VAR)", expanded=False):
            st.code(
                "sel = VAR(X).select_order(4)\n"
                "p = sel.aic or 1\n"
                "model = VAR(X).fit(p)\n"
                "fc = model.forecast(model.endog[-p:], steps=3)\n", language="python")
        try:
            X = tmp.copy()
            # Estratégia: diferenciar variáveis individualmente apenas se o ADF indicar não-estacionariedade
            diffed = {}
            for col in X.columns:
                adf = run_adf(X[col])  # roda ADF coluna a coluna
                # need_diff=True se p-valor >= 0.05 (não rejeita raiz unitária)
                need_diff = (not np.isnan(adf["pvalue"])) and (adf["pvalue"] >= 0.05)
                diffed[col] = bool(need_diff)
                # Aplica a primeira diferença apenas na(s) série(s) não estacionária(s)
                if need_diff: X[col] = X[col].diff()

            # Remove linhas iniciais perdidas pela diferença e garante float
            X = X.dropna().astype(float)
            # Checagem de tamanho mínimo de amostra após diferenciação
            if X.shape[0] < 8:
                st.warning("Amostra ficou curta após a diferenciação."); return

            # Define p máximo com bom senso: não exagerar em séries curtas
            max_p = min(4, max(1, X.shape[0] - 2))
            try:
                # Seleciona ordem via critério AIC até p máximo
                sel = VAR(X).select_order(max_p)
                # Alguns objetos retornam p diretamente em sel.aic; se None, usa 1
                p = int(sel.aic) if sel.aic is not None else 1
            except Exception:
                # Se falhar a seleção de ordem, usa p=1
                p = 1
            # Garante que p está no intervalo [1, max_p]
            p = max(1, min(max_p, int(p)))

            # Ajusta o VAR com p defasagens
            model = VAR(X).fit(p)

            # Forecast para N passos à frente, usando as últimas p observações
            fc = model.forecast(y=X.values[-model.k_ar:], steps=forecast_years)
            fc_df = pd.DataFrame(fc, columns=X.columns)

            # Reconstrói níveis para as séries que foram diferenciadas
            last_year = int(tmp.index.max())
            fut_years = list(range(last_year + 1, last_year + 1 + forecast_years))
            pred_df = pd.DataFrame(index=fut_years, columns=tmp.columns, dtype=float)
            for col in tmp.columns:
                if diffed.get(col, False):
                    # Se a série foi diferenciada: soma cumulativa às previsões + último nível observado
                    base = float(tmp[col].iloc[-1])
                    pred_df[col] = base + fc_df[col].cumsum().values
                else:
                    # Se não foi diferenciada: previsão já está em nível
                    pred_df[col] = fc_df[col].values

            # Fallback anti-NaN:
            # Em caso raro de NaN nas previsões (por numérico/colinearidade),
            # tenta refitar com p=1 e refaz reconstrução
            if pred_df.isna().any().any():
                model = VAR(X).fit(1)
                fc = model.forecast(y=X.values[-1:], steps=forecast_years)
                fc_df = pd.DataFrame(fc, columns=X.columns)
                for col in tmp.columns:
                    if diffed.get(col, False):
                        base = float(tmp[col].iloc[-1])
                        pred_df[col] = base + fc_df[col].cumsum().values
                    else:
                        pred_df[col] = fc_df[col].values

        except Exception as e:
            # Qualquer erro no pipeline VAR: informa e encerra
            st.error(f"Erro no VAR: {e}"); return


    # ---------- Plot + Conclusão ----------
    # Se por algum motivo não foi possível gerar o DataFrame de previsão, avisa e encerra
    if pred_df is None or pred_df.empty:
        st.warning("Sem forecast gerado."); return
    
    # Mantém somente os últimos 5 anos antes do forecast no histórico
    x_sep = int(tmp.index.max())  # último ano observado
    hist_start = max(tmp.index.min(), x_sep - 4)  # pega até 5 anos antes
    tmp_plot = tmp.loc[hist_start:]  # subset do histórico para plotagem

    # Cria a figura Plotly para visualizar histórico e previsões
    fig = go.Figure()

    # Série A (histórico): linhas + marcadores ao longo dos anos observados
    fig.add_trace(go.Scatter(x=tmp_plot.index, y=tmp_plot[a], mode="lines+markers", name=f"{a} — histórico"))

    # Série B (histórico): linhas + marcadores ao longo dos anos observados
    fig.add_trace(go.Scatter(x=tmp_plot.index, y=tmp_plot[b], mode="lines+markers", name=f"{b} — histórico"))

    # Série A (previsão): linhas + marcadores nos anos futuros; linha tracejada para diferenciar do histórico
    fig.add_trace(go.Scatter(x=pred_df.index, y=pred_df[a], mode="lines+markers",
                             name=f"{a} — previsão ({modelo_usado})", line=dict(dash="dash")))

    # Série B (previsão): idem acima, com estilo tracejado
    fig.add_trace(go.Scatter(x=pred_df.index, y=pred_df[b], mode="lines+markers",
                             name=f"{b} — previsão ({modelo_usado})", line=dict(dash="dash")))

    # Linha vertical separando o último ano histórico do início do forecast (ajuda visual)
    x_sep = int(tmp_plot.index.max())
    fig.add_vline(x=x_sep, line_width=1, line_dash="dash")

    # Anotação textual no topo do gráfico para indicar o ponto de início da previsão
    fig.add_annotation(x=x_sep, yref="paper", y=1.05, showarrow=False, text="Início do forecast")

    # Layout do gráfico: título centralizado, rótulos de eixos, legenda horizontal e margens
    fig.update_layout(title={"text": f"Evolução + previsão ({modelo_usado}) — {a} & {b}", "x": 0.5},
                      xaxis_title="Ano", yaxis_title="Valor (%)",
                      legend=dict(orientation="h", y=1.02, x=0),
                      margin=dict(t=80, b=40, l=40, r=20))

    y_min = min(tmp_plot[a].min(), tmp_plot[b].min(), pred_df[a].min(), pred_df[b].min())
    y_max = max(tmp_plot[a].max(), tmp_plot[b].max(), pred_df[a].max(), pred_df[b].max())
    y_range = [y_min - (abs(y_min) * 0.1), y_max + (abs(y_max) * 0.1)]

    fig.update_yaxes(tickformat=".2f", range=y_range)

    # Renderiza o gráfico no Streamlit ocupando toda a largura do container
    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------------------------------------
    # Conclusão textual (resumo) com base no último ponto previsto vs último histórico
    # ---------------------------------------------------------
    try:
        # Último valor histórico e última projeção para a série 'a'
        last_hist = float(tmp[a].iloc[-1]); last_fore = float(pred_df[a].iloc[-1])

        # Apenas se a projeção é um número finito (evita NaN/inf)
        if np.isfinite(last_fore):
            # Variação prevista entre o fim do histórico e o último ano projetado
            delta = last_fore - last_hist

            # Direção qualitativa: alta, queda ou estável
            direcao = "↑ alta" if delta > 0 else ("↓ queda" if delta < 0 else "→ estável")

            # Mensagem amigável com valores formatados e horizonte em anos
            st.success(f"**Conclusão ({a})**: de {last_hist:.2f}% para {last_fore:.2f}% → {direcao} nos próximos {forecast_years} anos ({modelo_usado}).")
        else:
            # Caso a última previsão esteja inválida
            st.warning("A última projeção veio NaN.")
    except Exception:
        # Se algo falhar no cálculo/formatação, apenas ignora silenciosamente (não quebra a UI)
        pass


# Chama a função principal para pares de variáveis de interesse,
# usando a flag de limpeza definida anteriormente no session_state
analyze_pair(dfm, "PIB real — crescimento (% a.a.)", "Desemprego (% força de trabalho)", st.session_state.apply_cleaning)
analyze_pair(dfm, "Inflação (CPI, % a.a.)", "Juros reais (% a.a.)", st.session_state.apply_cleaning)
analyze_pair(dfm, "Conta Corrente (% do PIB)", "PIB real — crescimento (% a.a.)", st.session_state.apply_cleaning)
