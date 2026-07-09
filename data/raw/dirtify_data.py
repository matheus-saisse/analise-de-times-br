"""
dirtify_data.py
----------------
Script para "sujar" de forma controlada e reprodutível o dataset
Campeonato Brasileiro (2003-2025) do Kaggle, simulando problemas reais
de qualidade de dados para prática de limpeza/tratamento.

Nível: PESADO (~30% das linhas afetadas por arquivo)
Tipo: MIX completo (missing, duplicatas, outliers, inconsistência de
      texto, encoding, tipos de dado errados, formatos de data variados)

Uso:
    python dirtify_data.py

Estrutura esperada:
    ./input/   -> CSVs originais (limpos)
    ./data/clean_backup/  -> cópia intacta dos originais (gabarito)
    ./data/raw/           -> versão suja, pronta pra você praticar limpeza
"""

import pandas as pd
import numpy as np
import random
import shutil
import os

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

INTENSITY = 0.30  # ~30% das linhas afetadas (nível "pesado")

INPUT_DIR = "input"
CLEAN_BACKUP_DIR = "data/clean_backup"
DIRTY_DIR = "data/raw"

FILES = [
    "campeonato-brasileiro-full.csv",
    "campeonato-brasileiro-estatisticas-full.csv",
    "campeonato-brasileiro-gols.csv",
    "campeonato-brasileiro-cartoes.csv",
]

os.makedirs(CLEAN_BACKUP_DIR, exist_ok=True)
os.makedirs(DIRTY_DIR, exist_ok=True)


# ---------------------------------------------------------------------
# FERRAMENTAS DE SUJEIRA (reutilizáveis entre tabelas)
# ---------------------------------------------------------------------

def pick_rows(df, frac):
    """Seleciona índices aleatórios de forma reprodutível."""
    n = max(1, int(len(df) * frac))
    return np.random.choice(df.index, size=n, replace=False)


def add_missing_values(df, cols, frac):
    """Introduz valores faltando com representações inconsistentes
    (NaN, string vazia, 'N/A', '-', 'null'), pra simular sujeira real
    de quem preencheu a mão ou juntou fontes diferentes."""
    fake_nulls = [np.nan, "", "N/A", "-", "null", "  "]
    for col in cols:
        if col not in df.columns:
            continue
        idx = pick_rows(df, frac / len(cols))
        for i in idx:
            df.loc[i, col] = random.choice(fake_nulls)
    return df


def add_duplicates(df, frac):
    """Duplica uma fração de linhas (algumas exatas, outras quase-exatas
    com pequena variação de texto, comum em merges de fontes)."""
    n = max(1, int(len(df) * frac))
    dup_idx = np.random.choice(df.index, size=n, replace=True)
    dup_rows = df.loc[dup_idx].copy()

    # metade das duplicatas fica exata, metade "quase-exata"
    half = len(dup_rows) // 2
    text_cols = df.select_dtypes(include="object").columns
    if len(text_cols) > 0:
        col = np.random.choice(text_cols)
        dup_rows.iloc[:half, dup_rows.columns.get_loc(col)] = (
            dup_rows.iloc[:half][col].astype(str).str.upper()
        )

    return pd.concat([df, dup_rows], ignore_index=True)


def mess_up_text_casing(df, cols, frac):
    """Deixa texto com capitalização/espaços inconsistentes:
    'São Paulo' vs 'SÃO PAULO' vs 'são paulo ' vs '  são paulo'."""
    for col in cols:
        if col not in df.columns:
            continue
        idx = pick_rows(df, frac / len(cols))
        for i in idx:
            val = df.loc[i, col]
            if pd.isna(val) or val == "":
                continue
            val = str(val)
            choice = random.choice(["upper", "lower", "leading_space", "trailing_space", "double_space"])
            if choice == "upper":
                df.loc[i, col] = val.upper()
            elif choice == "lower":
                df.loc[i, col] = val.lower()
            elif choice == "leading_space":
                df.loc[i, col] = "  " + val
            elif choice == "trailing_space":
                df.loc[i, col] = val + "   "
            elif choice == "double_space":
                df.loc[i, col] = val.replace(" ", "  ")
    return df


def break_encoding(df, cols, frac):
    """Simula acentos quebrados (mojibake), comum quando um CSV
    é salvo/lido com encoding errado (latin1 vs utf-8)."""
    replacements = {
        "ã": "Ã£", "á": "Ã¡", "â": "Ã¢", "à": "Ã ",
        "é": "Ã©", "ê": "Ãª", "í": "Ã­", "õ": "Ãµ",
        "ó": "Ã³", "ô": "Ã´", "ú": "Ãº", "ç": "Ã§",
    }
    for col in cols:
        if col not in df.columns:
            continue
        idx = pick_rows(df, frac / len(cols))
        for i in idx:
            val = df.loc[i, col]
            if pd.isna(val) or val == "":
                continue
            val = str(val)
            for orig, broken in replacements.items():
                val = val.replace(orig, broken)
            df.loc[i, col] = val
    return df


def scramble_date_formats(df, col, frac):
    """Mistura formatos de data: DD/MM/AAAA, AAAA-MM-DD, DD-MM-AA etc.
    Clássico problema de quem junta exports de sistemas diferentes."""
    if col not in df.columns:
        return df
    idx = pick_rows(df, frac)
    for i in idx:
        val = df.loc[i, col]
        if pd.isna(val) or val == "":
            continue
        try:
            dt = pd.to_datetime(val, dayfirst=True, errors="coerce")
            if pd.isna(dt):
                continue
            fmt = random.choice([
                "%Y-%m-%d", "%d-%m-%Y", "%d.%m.%Y",
                "%m/%d/%Y", "%d/%m/%y", "%Y/%m/%d",
            ])
            df.loc[i, col] = dt.strftime(fmt)
        except Exception:
            continue
    return df


def add_outliers(df, col, frac, mode="multiply"):
    """Insere valores absurdos em colunas numéricas
    (ex: posse de bola = 450%, cartões = -3)."""
    if col not in df.columns:
        return df
    idx = pick_rows(df, frac)
    for i in idx:
        try:
            original = pd.to_numeric(df.loc[i, col], errors="coerce")
            if pd.isna(original):
                continue
            if mode == "multiply":
                df.loc[i, col] = original * random.choice([10, 50, 100])
            elif mode == "negative":
                df.loc[i, col] = -abs(original) - random.randint(1, 10)
        except Exception:
            continue
    return df


def corrupt_numeric_as_text(df, cols, frac):
    """Transforma número em texto sujo: '12' vira '12 gols', 'doze', '12,0' etc.
    Simula planilha preenchida manualmente."""
    for col in cols:
        if col not in df.columns:
            continue
        idx = pick_rows(df, frac / len(cols))
        for i in idx:
            val = df.loc[i, col]
            if pd.isna(val) or val == "":
                continue
            choice = random.choice(["comma_decimal", "with_text", "spaces"])
            if choice == "comma_decimal":
                df.loc[i, col] = str(val).replace(".", ",")
            elif choice == "with_text":
                df.loc[i, col] = f"{val} un"
            elif choice == "spaces":
                df.loc[i, col] = f" {val} "
    return df


def rename_inconsistent_categories(df, col, mapping, frac):
    """Aplica variações de escrita para o mesmo valor categórico
    (ex: 'Amarelo' vs 'amarelo' vs 'AMARELO' vs 'Cartão Amarelo')."""
    if col not in df.columns:
        return df
    idx = pick_rows(df, frac)
    for i in idx:
        val = df.loc[i, col]
        if val in mapping:
            df.loc[i, col] = random.choice(mapping[val])
    return df


def shuffle_column_order(df, seed_offset=0):
    """Embaralha a ordem das colunas — simples, mas realista
    quando dados vêm de exports diferentes."""
    cols = list(df.columns)
    rng = random.Random(SEED + seed_offset)
    rng.shuffle(cols)
    return df[cols]


# ---------------------------------------------------------------------
# PIPELINE POR ARQUIVO
# ---------------------------------------------------------------------

def dirtify_full(df):
    df = add_missing_values(df, ["arrecadacao", "formacao_mandante", "formacao_visitante",
                                  "tecnico_mandante", "tecnico_visitante"], INTENSITY)
    df = mess_up_text_casing(df, ["mandante", "visitante", "arena", "vencedor"], INTENSITY)
    df = break_encoding(df, ["arena", "mandante", "visitante"], INTENSITY * 0.5)
    df = scramble_date_formats(df, "data", INTENSITY)
    df = corrupt_numeric_as_text(df, ["mandante_Placar", "visitante_Placar"], INTENSITY * 0.5)
    df = add_outliers(df, "mandante_Placar", INTENSITY * 0.05, mode="multiply")
    df = add_duplicates(df, INTENSITY * 0.3)
    df = shuffle_column_order(df, seed_offset=1)
    return df


def dirtify_estatisticas(df):
    df = add_missing_values(df, ["posse_de_bola", "precisao_passes", "chutes", "passes"], INTENSITY)
    df = mess_up_text_casing(df, ["clube"], INTENSITY)
    df = break_encoding(df, ["clube"], INTENSITY * 0.4)
    df = corrupt_numeric_as_text(df, ["posse_de_bola", "precisao_passes"], INTENSITY * 0.6)
    df = add_outliers(df, "posse_de_bola", INTENSITY * 0.08, mode="multiply")
    df = add_outliers(df, "cartao_amarelo", INTENSITY * 0.05, mode="negative")
    df = add_duplicates(df, INTENSITY * 0.3)
    df = shuffle_column_order(df, seed_offset=2)
    return df


def dirtify_gols(df):
    df = add_missing_values(df, ["tipo_de_gol", "atleta", "minuto"], INTENSITY)
    df = mess_up_text_casing(df, ["clube", "atleta"], INTENSITY)
    df = break_encoding(df, ["atleta", "clube"], INTENSITY * 0.5)
    tipo_map = {
        "Penalty": ["penalty", "PENALTY", "Pênalti", "penalti", "PÊNALTI"],
        "Gol Contra": ["gol contra", "GOL CONTRA", "Contra", "autogol"],
    }
    df = rename_inconsistent_categories(df, "tipo_de_gol", tipo_map, INTENSITY)
    df = add_outliers(df, "minuto", INTENSITY * 0.05, mode="multiply")
    df = add_duplicates(df, INTENSITY * 0.3)
    df = shuffle_column_order(df, seed_offset=3)
    return df


def dirtify_cartoes(df):
    df = add_missing_values(df, ["posicao", "num_camisa", "minuto"], INTENSITY)
    df = mess_up_text_casing(df, ["clube", "atleta", "posicao"], INTENSITY)
    df = break_encoding(df, ["atleta", "clube", "posicao"], INTENSITY * 0.5)
    cartao_map = {
        "Amarelo": ["amarelo", "AMARELO", "Cartão Amarelo", "cartao amarelo"],
        "Vermelho": ["vermelho", "VERMELHO", "Cartão Vermelho", "cartao vermelho"],
    }
    df = rename_inconsistent_categories(df, "cartao", cartao_map, INTENSITY)
    df = add_outliers(df, "minuto", INTENSITY * 0.05, mode="multiply")
    df = add_duplicates(df, INTENSITY * 0.3)
    df = shuffle_column_order(df, seed_offset=4)
    return df


PIPELINES = {
    "campeonato-brasileiro-full.csv": dirtify_full,
    "campeonato-brasileiro-estatisticas-full.csv": dirtify_estatisticas,
    "campeonato-brasileiro-gols.csv": dirtify_gols,
    "campeonato-brasileiro-cartoes.csv": dirtify_cartoes,
}


# ---------------------------------------------------------------------
# EXECUÇÃO
# ---------------------------------------------------------------------

def main():
    for filename in FILES:
        input_path = os.path.join(INPUT_DIR, filename)
        clean_path = os.path.join(CLEAN_BACKUP_DIR, filename)
        dirty_path = os.path.join(DIRTY_DIR, filename)

        print(f"Processando {filename}...")

        df_original = pd.read_csv(input_path)

        # 1) guarda backup limpo, intocado
        shutil.copy(input_path, clean_path)

        # 2) aplica sujeira (cast pra object evita erro de tipo ao misturar
        #    string/NaN/número em colunas originalmente numéricas)
        df_dirty = PIPELINES[filename](df_original.copy().astype(object))

        # 3) embaralha a ordem das linhas (mais um toque de realismo)
        df_dirty = df_dirty.sample(frac=1, random_state=SEED).reset_index(drop=True)

        # 4) salva versão suja
        df_dirty.to_csv(dirty_path, index=False)

        print(f"  -> original: {len(df_original)} linhas | sujo: {len(df_dirty)} linhas "
              f"(+{len(df_dirty) - len(df_original)} de duplicatas)")

    print("\nConcluído!")
    print(f"Backup limpo em: {CLEAN_BACKUP_DIR}/")
    print(f"Dados sujos em:  {DIRTY_DIR}/")


if __name__ == "__main__":
    main()
