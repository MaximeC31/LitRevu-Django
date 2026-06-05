# LITRevu

Application web Django de critiques de livres et d'articles.

LITRevu permet a une communaute de lecteurs de publier des critiques, demander un avis sur une lecture et suivre d'autres utilisateurs pour construire un flux personnalise.

## Fonctionnalites

- inscription, connexion et deconnexion
- flux antichronologique combinant tickets et critiques
- creation d'un ticket pour demander une critique
- creation d'une critique complete avec ticket en une etape
- reponse a un ticket existant avec une critique
- modification et suppression de ses propres tickets
- suppression de ses propres critiques
- systeme d'abonnements entre utilisateurs
- page `Vos posts` pour retrouver ses publications
- upload d'image sur les tickets

## Stack

- Python
- Django 6
- SQLite
- templates Django rendus cote serveur
- Tailwind CSS via CDN

## Installation

Prerequis:

- Python 3.12+
- `pip`

Installation locale:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

L'application sera accessible sur `http://127.0.0.1:8000/`.

## Commandes utiles

```bash
python -m flake8 manage.py authentication core reviews
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py check
python manage.py test
```

## Parcours principal

1. Un visiteur arrive sur la page d'accueil `/`.
2. Il cree un compte ou se connecte.
3. Il peut publier un ticket pour demander une critique.
4. Il peut publier une critique complete sur un livre ou article.
5. Il peut suivre d'autres utilisateurs depuis `Abonnements`.
6. Son flux `feed/` affiche les tickets et critiques de son reseau.

## Routes principales

- `/` : accueil
- `/signup/` : inscription
- `/login/` : connexion
- `/logout/` : deconnexion
- `/feed/` : flux principal
- `/posts/` : publications de l'utilisateur connecte
- `/tickets/create/` : creation de ticket
- `/reviews/create` : creation d'une critique avec ticket
- `/subscriptions/` : abonnements

## Structure

```text
authentication/  gestion des utilisateurs et de l'authentification
core/            configuration Django et routing principal
reviews/         coeur metier: tickets, critiques, abonnements, flux
templates/       templates globaux
media/           fichiers uploades en local
manage.py        point d'entree Django
```
