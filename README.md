# Reconnaissance faciale en temps réel

## Description

Ce projet consiste à développer une méthode de **reconnaissance faciale en temps réel à partir d'une webcam**.

L'application permet de :

* détecter les visages présents dans le flux vidéo ;
* encoder les visages détectés ;
* comparer ces encodages avec des visages de référence ;
* identifier les personnes reconnues ;
* afficher le résultat directement sur le flux vidéo ;
* reconnaître automatiquement les nouvelles personnes ajoutées dans le dossier `faces`.

La reconnaissance est effectuée en temps réel grâce à une webcam et à la bibliothèque `face_recognition`.

## Technologies utilisées

* **Python 3**
* **OpenCV** (`cv2`) pour la capture et l'affichage vidéo
* **face_recognition** pour la détection, l'encodage et la comparaison des visages
* **NumPy**, utilisé par les bibliothèques de traitement d'image

## Structure du projet

```text
Facial-Recognition/
│
├── FACE/
│   ├── faceFinding.py
│   ├── faces/
│   │   └── .gitkeep
│   └── runProg.txt
│
├── README.md
└── requirements.txt
```

Le dossier `faces/` contient les photos utilisées comme références pour la reconnaissance.

> Les photos de référence ne sont pas incluses dans le dépôt. Elles doivent être ajoutées localement dans `FACE/faces/`.

## Installation

### 1. Cloner le projet

```bash
git clone git@github.com:Alex-ov1/Facial-Recognition.git
cd Facial-Recognition
```

### 2. Créer un environnement virtuel

Il est recommandé d'utiliser un environnement virtuel Python :

```bash
python3 -m venv venv
```

Activer l'environnement :

```bash
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Ajouter des visages de référence

Ajouter les photos dans :

```text
FACE/faces/
```

Les formats suivants sont acceptés :

* `.jpg`
* `.jpeg`
* `.png`

Le **nom du fichier est utilisé comme nom de la personne**.

Par exemple :

```text
FACE/faces/
├── alice.jpg
├── bob.jpg
└── charlie.png
```

L'application affichera alors :

```text
alice
bob
charlie
```

Lors du lancement, les images sont automatiquement parcourues et les visages présents sont encodés.

Si aucune photo ne contient de visage détectable, elle est ignorée.

## Lancer le programme

Se placer dans le dossier `FACE` :

```bash
cd FACE
```

Puis lancer :

```bash
python3 faceFinding.py
```

La webcam est ensuite ouverte et la reconnaissance faciale démarre automatiquement.

## Fonctionnement

Le programme fonctionne selon les étapes suivantes :

### 1. Chargement des références

Le programme parcourt automatiquement le dossier `faces/` et recherche les fichiers image.

Pour chaque image contenant un visage, un encodage facial est créé.

### 2. Ouverture de la webcam

La webcam est configurée pour essayer d'utiliser :

* une résolution de `1280 × 720` ;
* `30 FPS` ;
* le format `MJPG` ;
* un buffer réduit afin de limiter la latence.

La caméra utilisée par le programme est actuellement :

```text
/dev/video2
```

Si votre webcam utilise un autre périphérique Linux, cette valeur peut être modifiée dans `faceFinding.py`.

### 3. Traitement de l'image

Chaque image provenant de la webcam est réduite à 25 % de sa taille avant la détection afin de diminuer le temps de traitement.

L'image est ensuite convertie de **BGR vers RGB**, car `face_recognition` utilise le format RGB.

### 4. Détection et reconnaissance

Les visages présents dans l'image sont détectés puis encodés.

Chaque encodage est comparé aux visages de référence avec une tolérance de `0.5`.

Si une correspondance est trouvée :

```text
Nom de la personne
```

est affiché en vert.

Sinon :

```text
Inconnu
```

est affiché en rouge.

### 5. Affichage

Un rectangle est dessiné autour de chaque visage détecté :

* **vert** : visage reconnu ;
* **rouge** : visage inconnu.

Le nom est affiché au-dessus du rectangle.

## Commandes

Pour quitter le programme, appuyer sur :

```text
q
```

## Exemple

Avec une photo :

```text
FACE/faces/Alex.jpg
```

le programme peut afficher :

```text
Alex
```

lorsque le visage correspondant est détecté par la webcam.

Pour une personne qui ne correspond à aucune photo de référence :

```text
Inconnu
```

sera affiché.

## Remarques

La qualité de la reconnaissance dépend notamment :

* de la qualité des photos de référence ;
* de l'éclairage ;
* de l'angle du visage ;
* de la distance par rapport à la webcam ;
* de la qualité de la caméra.

Pour obtenir de meilleurs résultats, il est recommandé d'utiliser des photos où le visage est clairement visible et suffisamment éclairé.

## Objectif du projet

L'objectif est de mettre en œuvre une chaîne complète de reconnaissance faciale en temps réel :

```text
Webcam
   ↓
Détection des visages
   ↓
Encodage facial
   ↓
Comparaison avec les références
   ↓
Identification
   ↓
Affichage en temps réel
```
