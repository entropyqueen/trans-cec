*trans-cec* permet de générer des fichiers PDF à partir d'un formulaire Django en utilisant [django-tex](https://pypi.org/project/django-tex/).
Il s'agit d'un fork du project de Maria Climent-Pommeret
[site-transadministratif](https://gitlab.chelsea486mhz.fr/Chelsea486MHz/trans-cec).

| Auteur.ice             | Licence     |
|------------------------|-------------|
| Maria Climent-Pommeret | Licence MIT |


| Mainteneur.euse(s) | Tâche(s)   | Contact |
|--------------------|------------|---------|
| Emy Canton         | all        |         |

Comment cela fonctionne
-----------------------

Pour l'instant, sont gérées :
- les lettres polies de demande de changement de prénom et de civilité
- les lettres de relance en cas d'absence de réponse (satisfaisante)

Les différents modes :
- par procuration (génère une procuration + la lettre de demande à faire envoyer
par un.e cis de l'entourage qui pourra gérer les tracas administratifs, pour pas
que vous ayez a gérer vous même cette merde)
- [to come] les lettres si vous souhaitez le faire vous même.

Checklist des papiers à changer
-------------------------------

Si changement de prénom à l'EC
- [ ] carte de transport
- [ ] CNI/passeport
- [ ] permis de conduire
- [ ] impôts
- [ ] médecins
- [ ] mutuelle
- [ ] carte de groupe sanguin/donneur.se d'organes
- [ ] MDPH
- [ ] électricité/gaz/eau
- [ ] opérateur téléphonique/Internet
- [ ] carte d'électeur.rice

Si changement de mention de sexe à l'État-Civil (pas encore pris en charge) :
- [ ] CNI/passeport
- [ ] permis de conduire
- [ ] numéro INSEE
- [ ] numéro de sécurité sociale

Requirements
------------

- Python>=3.10 (Latest tested with)
- django-tex
- jinja2-django-tags
- texlive-full (pour la génération du PDF à partir de .tex)

Déploiement
----------

Installer docker et docker-compose

```shell
$ sudo apt install docker docker-compose
```

#### Environnement de dev

```shell
$ docker-compose up
```

#### Environnement de prod

Commencer par créer le fichier d'environnement de Prod `.env.prod`:
```shell
DEBUG=0
SECRET_KEY=CHANGE_ME
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
CSRF_TRUSTED_ORIGINS=https://your-domain.com
```
⚠️ Changer la SECRET_KEY par une valeur aléatoire d'au moins 50 caractères.

```shell
$ docker-compose -f docker-compose.prod.yml up -d --build
```
L'option `--build` permet de re-build l'image pour qu'elle soit à jour

L'option `-d` permet de passer en mode daemon.

Contribuer ?
------------

OUI SVP ! Pour cela, n'hésitez pas à faire des issues github ou bien ouvrir directement des PR sur github 

Pour cela les dépendances système requises sont :

- git
- python3.10
- python3-venv
- texlive-full

Il vous reste à configurer et faire fonctionner votre copie locale.

La première étape est de créer un environnement virtuel python afin d'installer les dépendances du projet :

    $ python3 -m venv virtualenv

Ensuite, installez les dépendances python requises pour faire fonctionne le projet :

    $ virtualenv/bin/pip install -r requirements.txt

Créez votre fichier de configuration :

    $ cp mysite/mysite/localsettings.py.dist mysite/mysite/localsettings.py

Éditez le fichier `mysite/mysite/localsettings.py` et ajoutez une valeur pour `SECRET_KEY`,
par exemple `SECRET_KEY = 'dev'`.

Appliquez les migrations

    $ virtualenv/bin/python mysite/manage.py migrate

Lancez le serveur de développement :

    $ virtualenv/bin/python mysite/manage.py runserver

Le projet est démarré et accessible à l'adresse http://127.0.0.1:8000/ :)

Lancer les tests
----------------

Des tests unitaires sont disponibles pour ce projet. Si vous modifiez du code, vous pouvez
les lancer pour vérifier que vous n'avez rien cassé :

    $ cd mysite
    $ pytest tests

Ont contribué
-------------

Un grand merci à toutes ces personnes qui ont fait des tests, bugs reports, merge requests, corrections orthographiques
et montré du soutien \o/ :

- [Emy Canton](https://entropyqueen.github.io/)
- [Alice Climent-Pommeret](https://alice.climent-pommeret.red/fr)
- [Sasha Emily Chelsea Murgia](https://www.chelsea486mhz.fr)
- Aurore Moisy-Mabille
- [Agate Berriot](https://agate.blue/)
- Une autre [Alice](https://bidule.menf.in/users/alice)
- [Freyja Wildes](https://social.art-software.fr/@freyja_wildes)
- Misc
