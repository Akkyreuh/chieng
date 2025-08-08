# Dog Breed Classifier 🐕

Une application web pour classifier les races de chiens utilisant plusieurs modèles de Deep Learning.

## 🚀 Fonctionnalités

- **Upload d'images** : Interface drag & drop intuitive
- **Prédiction multi-modèles** : 3 modèles TensorFlow analysent chaque image
- **Top 3 des races** : Affichage des résultats avec scores de confiance
- **Interface responsive** : Compatible desktop et mobile

## 🏗️ Architecture

- **Frontend** : React.js + TypeScript
- **Backend** : FastAPI (Python)
- **Modèles** : Support TensorFlow (.h5, .keras)
- **Déploiement** : Docker + docker-compose

## 🛠️ Installation et lancement

### Avec Docker (recommandé)

```bash
# Cloner le projet
git clone <repo-url>
cd dog-breed-classifier

# Lancer avec docker-compose
docker-compose up --build
```

L'application sera accessible sur :
- Frontend : http://localhost:3000
- Backend API : http://localhost:8000

### Développement local

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## 📁 Structure du projet

```
dog-breed-classifier/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── main.py         # Point d'entrée
│   │   ├── api/routes.py   # Routes API
│   │   ├── models/         # Logique ML
│   │   └── utils/          # Utilitaires
│   └── requirements.txt
├── frontend/               # Interface React
│   ├── src/
│   │   ├── components/     # Composants React
│   │   ├── services/       # Services API
│   │   └── types/          # Types TypeScript
│   └── package.json
└── docker-compose.yml      # Configuration Docker
```

## Utilisation

1. Accédez à l'application web
2. Glissez-déposez une image de chien ou cliquez pour sélectionner
3. Attendez l'analyse par les 3 modèles
4. Consultez le Top 3 des races prédites avec leurs scores

## Configuration

Placez vos modèles TensorFlow (.h5 ou .keras) dans le dossier `backend/app/models/models/`

Les modèles doivent être nommés :
- `model1.h5` (ou .keras)
- `model2.h5` (ou .keras)  
- `model3.h5` (ou .keras)

## API Endpoints

- `POST /predict` : Upload d'image et prédiction
- `GET /health` : Status de l'API
- `GET /models` : Liste des modèles chargés
