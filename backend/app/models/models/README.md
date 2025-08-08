# Modèles de Classification

Placez vos modèles TensorFlow entraînés dans ce dossier.

## Format des fichiers

Les modèles doivent être nommés selon le format suivant :
- `model1.h5` ou `model1.keras`
- `model2.h5` ou `model2.keras`  
- `model3.h5` ou `model3.keras`

## Spécifications des modèles

- **Format d'entrée** : Images RGB de taille 224x224 pixels
- **Format de sortie** : Probabilités pour 120 races de chiens
- **Normalisation** : Pixels normalisés entre 0 et 1

## Modèles de démonstration

Si aucun modèle n'est fourni, l'application utilisera des modèles factices pour la démonstration. Ces modèles génèrent des prédictions aléatoires mais permettent de tester toutes les fonctionnalités de l'interface.

## Entraînement de modèles

Pour entraîner vos propres modèles, utilisez un dataset de races de chiens comme :
- Stanford Dogs Dataset
- Dog Breed Identification (Kaggle)

Assurez-vous que vos modèles prédisent les races dans l'ordre défini dans `config.py`.
