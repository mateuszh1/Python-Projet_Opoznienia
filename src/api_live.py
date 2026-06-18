import requests
from google.transit import gtfs_realtime_pb2


URLS = {
    "autobusy": {
        "pozycje": "https://gtfs.ztp.krakow.pl/VehiclePositions_A.pb",
        "opoznienia": "https://gtfs.ztp.krakow.pl/TripUpdates_A.pb",
    },
    "tramwaje": {
        "pozycje": "https://gtfs.ztp.krakow.pl/VehiclePositions_T.pb",
        "opoznienia": "https://gtfs.ztp.krakow.pl/TripUpdates_T.pb",
    },
}


def pobierz_feed(url):
   
    odpowiedz = requests.get(url, timeout=20)
    odpowiedz.raise_for_status()

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(odpowiedz.content)

    return feed


def pobierz_pozycje_pojazdow(typ_pojazdu):
    
    url = URLS[typ_pojazdu]["pozycje"]
    feed = pobierz_feed(url)

    dane = []

    for entity in feed.entity:
        if not entity.HasField("vehicle"):
            continue

        pojazd = entity.vehicle

        if not pojazd.HasField("position"):
            continue

        trip = pojazd.trip if pojazd.HasField("trip") else None
        vehicle_info = pojazd.vehicle if pojazd.HasField("vehicle") else None

        dane.append({
            "linia": trip.route_id if trip else None,
            "kurs": trip.trip_id if trip else None,
            "pojazd": vehicle_info.label if vehicle_info else None,
            "szerokosc": pojazd.position.latitude,
            "dlugosc": pojazd.position.longitude,
            "timestamp": pojazd.timestamp if pojazd.timestamp else None,
        })

    return dane


def pobierz_opoznienia(typ_pojazdu):
   
    url = URLS[typ_pojazdu]["opoznienia"]
    feed = pobierz_feed(url)

    dane = []

    for entity in feed.entity:
        if not entity.HasField("trip_update"):
            continue

        aktualizacja = entity.trip_update
        trip = aktualizacja.trip

        for stop in aktualizacja.stop_time_update:
            opoznienie_sec = None

            if stop.HasField("arrival") and stop.arrival.HasField("delay"):
                opoznienie_sec = stop.arrival.delay
            elif stop.HasField("departure") and stop.departure.HasField("delay"):
                opoznienie_sec = stop.departure.delay

            dane.append({
                "linia": trip.route_id,
                "kurs": trip.trip_id,
                "przystanek_id": stop.stop_id,
                "kolejnosc_przystanku": stop.stop_sequence,
                "opoznienie_sec": opoznienie_sec,
            })

    return dane
