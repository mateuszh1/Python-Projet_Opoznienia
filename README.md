# Opóźnienia komunikacji miejskiej w Krakowie

Projekt przedstawia prostą aplikację w Pythonie do podglądu aktualnych danych komunikacji miejskiej w Krakowie. Aplikacja pobiera dane live z ZTP Kraków i pokazuje pozycje autobusów lub tramwajów na mapie.

## Funkcje aplikacji

* pobieranie aktualnych danych komunikacji miejskiej,
* wybór typu pojazdu: autobusy lub tramwaje,
* filtrowanie danych po numerze linii,
* wyświetlanie pojazdów na mapie,
* pokazanie podstawowych informacji o pojazdach,


## Technologie
* Python
* Streamlit
* Pandas
* GTFS Realtime
* gtfs-realtime-bindings

## Struktura projektu

```text
.
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── .gitkeep
└── src/
    ├── __init__.py
    ├── api_live.py
    └── processing_live.py
```

## Opis plików

`app.py`
Główny plik aplikacji. Odpowiada za wygląd strony, panel boczny, mapę oraz wyświetlanie danych.

`src/api_live.py`
Plik odpowiedzialny za pobieranie danych live z plików GTFS Realtime.

`src/processing_live.py`
Plik odpowiedzialny za przygotowanie danych do pokazania w aplikacji.

`requirements.txt`
Lista bibliotek potrzebnych do uruchomienia projektu.


## Uruchomienie

Aplikację uruchamia się komendą:

```bash
python -m streamlit run app.py
```


## Jak korzystać z aplikacji

1. W panelu bocznym wybierz typ pojazdu: autobusy albo tramwaje.
2. Opcjonalnie wpisz numer linii, np. `4`, `50`, `179`.
3. Kliknij przycisk `Pobierz dane live`.
4. Sprawdź aktualne pozycje pojazdów na mapie.
5. W razie potrzeby włącz szczegółowe tabele.

## Autor

Mateusz Horabik, Dawid Strojny
