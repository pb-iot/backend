# Backend

## Installation

```bash
poetry install
```

## Migrations

### Create migrations

```bash
poetry run python manage.py makemigrations
```

### Apply migrations

```bash
poetry run python manage.py migrate
```

## Running application

```bash
poetry run python manage.py runserver
```

## About

### Business requirements

- [ ] komunikacja z frontem
- [ ] komunikacja z symulatorem
- [ ] przetwarzanie i wysylanie paczek json
- [ ] obslua wielu szlarni
- [ ] userzy + permissions (admin, trainee, experienced)
- [ ] wytrenowanie i zaaplikowanie modelu do obslugi informacji z fronta i symulatora
- [ ] model user
- [ ] model role
- [ ] model permission
- [ ] mdoel thing (rodzaj id)
- [ ] model lokalizacja (id, nazwa)
- [ ] model szklarnia (id, nazwa, lokalizacja, lista urzadzen, lista uprawnionych uzytkownikow4, owner)
- [ ] model pomiary
- [ ] rozpoznawanie awarii

# Struktura 
## User
- imie
- nazwisko
- email
- haslo
- rola (fk)
- aktywny

## Rola + uprawnienia jako enumy (do ustalenia czy nie wystarcza nam is_superuser itp i tylko do nich przypisywac uprawnienia)
- nazwa
- lista uprawnien

## Urządzenie
- nazwa
- rodzaj (np. tablet, natryski)
- typ (dostepowe, funkcyjne)

## Lokalizacja
- nazwa

## Szklarnia
- nazwa
- srodowisko (fk)
- lokalizacja (fk)
- lista urzadzen (fk)
- lista uprawnionych uzytkownikow (fk)
- wlasciciel (fk)

## Srodowisko
- temperatura
- wilgotność powietrza
- poziom światła
- PAR
- poziom CO2
- poziom wody w podłożu
- poziom zasolenia (EC) w podłożu
- temperatura podłoża
- waga podłoża i roślin
- mikro zmienność łodygi
  
## Autentykacja:
- JWT

## Funkcjonalności:
### Użytkownik:
- rejestracja
- logowanie
- przypisywanie roli (admin)
- dodawanie szklarni
- edycja/usuwanie konta
  
### Szklarnia:
- włączanie/wyłączanie urządzeń funkcyjnych
- zebranie pomiarów
- informowanie o awarii sprzętu
- dodawanie urządzeń
- manualne sterowanie sprzętem







