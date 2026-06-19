import streamlit as st


from src.api_live import pobierz_pozycje_pojazdow, pobierz_opoznienia
from src.processing_live import przygotuj_pozycje, przygotuj_opoznienia, zrob_podsumowanie


st.set_page_config(
    page_title="Opóźnienia KMK Kraków",
    page_icon="🚌",
    layout="wide",
)


st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 18px;
        color: #9ca3af;
        margin-bottom: 25px;
    }
    .info-box {
        padding: 15px;
        border-radius: 12px;
        background-color: rgba(49, 130, 206, 0.12);
        border: 1px solid rgba(49, 130, 206, 0.35);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">Opóźnienia komunikacji miejskiej w Krakowie</div>', unsafe_allow_html=True)





@st.cache_data(ttl=60)
def wczytaj_dane(typ_pojazdu):
    pozycje = przygotuj_pozycje(pobierz_pozycje_pojazdow(typ_pojazdu))
    opoznienia = przygotuj_opoznienia(pobierz_opoznienia(typ_pojazdu))
    return pozycje, opoznienia


with st.sidebar:
    st.header("Ustawienia")

    typ_pojazdu = st.selectbox(
        "Typ pojazdu",
        ["autobusy", "tramwaje"],
    )

    linia = st.text_input(
        "Filtr linii",
        placeholder="np. 4, 50, 179",
    )

    pokaz_tabele = st.checkbox("Pokaż szczegółowe tabele", value=False)

    pobierz = st.button("Pobierz dane live", type="primary")


if not pobierz:
    st.info("Wybierz typ pojazdu z panelu bocznego i kliknij **Pobierz dane live**.")
    st.stop()

try:
    pozycje, opoznienia = wczytaj_dane(typ_pojazdu)

    if linia.strip():
        wybrana_linia = linia.strip()
        pozycje = pozycje[pozycje["linia"].astype(str) == wybrana_linia]
        opoznienia = opoznienia[opoznienia["linia"].astype(str) == wybrana_linia]

    podsumowanie = zrob_podsumowanie(opoznienia)

    srednie_opoznienie = 0
    if not opoznienia.empty and opoznienia["opoznienie_min"].notna().any():
        srednie_opoznienie = opoznienia["opoznienie_min"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Liczba pojazdów na mapie", len(pozycje))
    col2.metric("Liczba pomiarów opóźnień", len(opoznienia))
    col3.metric("Średnie opóźnienie", f"{srednie_opoznienie:.1f} min")

    tab1, tab2 = st.tabs(["Mapa", "Dane"])


    with tab1:
        st.subheader("Aktualne pozycje pojazdów")

        if pozycje.empty:
            st.warning("Brak pozycji pojazdów dla wybranych ustawień.")
        else:
            mapa = pozycje.rename(columns={"szerokosc": "lat", "dlugosc": "lon"})
            st.map(mapa[["lat", "lon"]])

    with tab2:
        if pokaz_tabele:
            st.subheader("Tabela pozycji pojazdów")

            kolumny_pozycji = [
            "linia",
            "pojazd",
            "czas_pomiaru"
            ]

            dostepne_kolumny = [kol for kol in kolumny_pozycji if kol in pozycje.columns]

            st.dataframe(
                pozycje[dostepne_kolumny],
                use_container_width=True,
                hide_index=True
            )

            st.subheader("Tabela opóźnień")
            st.dataframe(opoznienia, use_container_width=True, hide_index=True)
        else:
            st.info("Włącz opcję **Pokaż szczegółowe tabele** w panelu bocznym.")

except Exception as blad:
    st.error(f"Nie udało się pobrać danych: {blad}")
