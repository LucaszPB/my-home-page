# =========================================================
# Objetivo: baixar indicadores macro do Brasil (World Bank API)
# e salvar em CSVs: um por indicador + um merged para modelagem.
# =========================================================

import os
import requests
import pandas as pd
from datetime import datetime

# ======= CONFIG =======
# AVISO: Se sua estrutura de projeto for diferente, estou saindo da estrutura.
OUTPUT_DIR = r""        # pasta onde os CSVs serão salvos
COUNTRY = "BR"                      # Brasil
YEARS_BACK = 25                     # janela para download (ajuste se quiser)
# ======================

# Indicadores (World Bank codes)
INDICADORES = {
    "Inflação (CPI, % a.a.)": "FP.CPI.TOTL.ZG",
    "PIB real — crescimento (% a.a.)": "NY.GDP.MKTP.KD.ZG",
    "Desemprego (% força de trabalho)": "SL.UEM.TOTL.ZS",
    "Conta Corrente (% do PIB)": "BN.CAB.XOKA.GD.ZS",
    "Juros reais (% a.a.)": "FR.INR.RINR",
}

# Quais indicadores baixar (por nome da chave acima)
SELECIONADOS = [
    "Inflação (CPI, % a.a.)",
    "PIB real — crescimento (% a.a.)",
    "Desemprego (% força de trabalho)",
    "Conta Corrente (% do PIB)",
    "Juros reais (% a.a.)",
]

def fetch_wb_series(country_code: str, indicator_code: str, start_year: int, end_year: int) -> pd.DataFrame:
    """
    Busca dados da API do Banco Mundial (formato JSON).
    Retorna DataFrame com colunas: ['year', 'value'] (anos crescentes).
    """
    url = (
        f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"
        f"?format=json&date={start_year}:{end_year}&per_page=1000"
    )
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    registros = data[1] if isinstance(data, list) and len(data) > 1 else []

    rows = []
    for item in registros:
        year = item.get("date")
        val = item.get("value")
        try:
            y = int(year)
            rows.append({"year": y, "value": None if val is None else float(val)})
        except:
            pass
    df = pd.DataFrame(rows).dropna(subset=["year"]).sort_values("year")
    return df

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ano_atual = datetime.now().year
    start_year = ano_atual - YEARS_BACK

    print(f"[INFO] Baixando dados {COUNTRY} de {start_year} a {ano_atual}...")
    dfs_por_nome = {}

    for nome in SELECIONADOS:
        code = INDICADORES[nome]
        try:
            df = fetch_wb_series(COUNTRY, code, start_year, ano_atual)
            if df.empty:
                print(f"[AVISO] Sem dados para {nome} ({code}).")
                continue

            # salva CSV por indicador: nome_simplificado.csv
            fname = nome.lower().replace(" ", "_").replace("%", "pct").replace("—", "-").replace("–", "-")
            out_path = os.path.join(OUTPUT_DIR, f"{fname}.csv")
            df.to_csv(out_path, index=False)
            print(f"[OK] {nome} -> {out_path} (linhas={len(df)})")
            dfs_por_nome[nome] = df.rename(columns={"value": nome}).set_index("year")

        except Exception as e:
            print(f"[ERRO] Falha ao baixar {nome} ({code}): {e}")

    # Merged
    if dfs_por_nome:
        merged = None
        for nome, dfx in dfs_por_nome.items():
            merged = dfx if merged is None else merged.join(dfx, how="outer")

        merged = merged.sort_index()
        merged_out = os.path.join(OUTPUT_DIR, "merged_macro_br.csv")
        merged.to_csv(merged_out, index_label="year")
        print(f"[OK] Merged salvo em: {merged_out} (linhas={len(merged)})")
    else:
        print("[ERRO] Nenhum indicador disponível para gerar merged.")

if __name__ == "__main__":
    main()