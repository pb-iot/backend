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

## Business requirements

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
