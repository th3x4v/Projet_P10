# Openclassroom Projet 09
Projet réalisé dans le cadre de ma formation OpenClassrooms Développeur d'Applications Python.  
Il s'agit d'une application web réalisée avec Django pour une société fictive, Softdesk.  
L'application SoftDesk Support vise à permettre aux entreprises B2B de remonter et de suivre des problèmes techniques de manière efficace grâce à une API RESTful.

## Fonctionnalités

- Création de tickets de support technique.
- Attribution de tickets à des équipes ou des agents de support.
- Suivi de l'état d'avancement des tickets.
- Commentaires et mises à jour en temps réel.
- Gestion des utilisateurs et des autorisations.

## Installation

Installer Python : https://www.python.org/downloads/ 
 
Lancez ensuite la console, placez vous dans le dossier de votre choix puis clonez ce repository:
```
git clone https://github.com/th3x4v/Projet_P10.git
```
Placez vous dans le dossier Projet_P9, puis créez un nouvel environnement virtuel:
```
python3 -m venv venv
```
Ensuite, activez-le.
Windows:
```
venv\scripts\activate.bat
```
Linux/MAC:
```
source venv/bin/activate
```
Installez ensuite les packages requis:
```
pip install -r requirements.txt
```
Il ne vous reste plus qu'à lancer le serveur: 
```
python manage.py runserver
```
Vous pouvez ensuite utiliser l'applicaton à l'adresse suivante:
```
http://127.0.0.1:8000
```
## Test
### Django administration

Identifiant : **xavier** | Mot de passe : **password-oc**

&rarr; http://127.0.0.1:8000/admin/

### Liste des utilisateurs existants

| *Identifiant*  | *Mot de passe*   |
|----------------|------------------|
| Sylvain        | password-oc      |
| Lucie          | password-oc      |
| Pierre         | password-oc      |
| Sofia          | password-oc      |
| openclassrooms | password-oc      |

