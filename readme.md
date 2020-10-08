# Arctic sun app - Collibri Transport

## Doel
 * Bijhouden van locaties van onze arctic sun machines.

## Installatie
- clone repository to new folder
- Scripts/activate

#### If pip problems
- python -m ensurepip
- python -m pip install --upgrade pip

### Install Dependencies:
- pip install -r requirements.txt

### Create database
```sh
$ python # (to start python cli)
$ from app import db
$ db.create_all()
$ exit()
```

### Start app locally:
flask run


## Upgraden
 * ```pip freeze > requirements.txt```

## Database migraties

* generate migration: ```flask db migrate -m "Text about migration"```
* lokaal: ```flask db upgrade```
* online: ```heroku run flask db upgrade```
* online met export: ```heroku run  "export LC_ALL=C.UTF-8; export LANG=C.UTF-8; flask db upgrade"```

## (1ste) Gebruiker toevoegen
* lokaal: flask users create gebruikersnaam emailadres wachtwoord
* online: heroku run flask users create gebruikersnaam emailadres wachtwoord


### Pagina's
* /login
* /register
* /logout
* / (= index)
* /all
