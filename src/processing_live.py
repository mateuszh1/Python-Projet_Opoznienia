import pandas as pd


def przygotuj_pozycje(dane):
    
    df = pd.DataFrame(dane)

    if df.empty:
        return df

    df["szerokosc"] = pd.to_numeric(df["szerokosc"], errors="coerce")
    df["dlugosc"] = pd.to_numeric(df["dlugosc"], errors="coerce")
    df["czas"] = pd.to_datetime(df["timestamp"], unit="s", errors="coerce")

    df = df.dropna(subset=["szerokosc", "dlugosc"])

    # Zostawiamy okolice Krakowa
    df = df[
        df["szerokosc"].between(49.8, 50.2)
        & df["dlugosc"].between(19.6, 20.3)
    ]

    return df.reset_index(drop=True)


def przygotuj_opoznienia(dane):
    #Czyści dane o opóźnieniach i dodaje opóźnienie w minutach
    df = pd.DataFrame(dane)

    if df.empty:
        return df

    df["opoznienie_sec"] = pd.to_numeric(df["opoznienie_sec"], errors="coerce")
    df["opoznienie_min"] = (df["opoznienie_sec"] / 60).round(1)

    return df.reset_index(drop=True)


def zrob_podsumowanie(df):
    
    if df.empty or "opoznienie_min" not in df.columns:
        return pd.DataFrame()

    podsumowanie = (
        df.dropna(subset=["linia", "opoznienie_min"])
        .groupby("linia", as_index=False)
        .agg(
            srednie_opoznienie=("opoznienie_min", "mean"),
            najwieksze_opoznienie=("opoznienie_min", "max"),
            liczba_pomiarow=("opoznienie_min", "count"),
        )
    )

    podsumowanie["srednie_opoznienie"] = podsumowanie["srednie_opoznienie"].round(1)
    podsumowanie["najwieksze_opoznienie"] = podsumowanie["najwieksze_opoznienie"].round(1)

    return podsumowanie.sort_values("srednie_opoznienie", ascending=False)
