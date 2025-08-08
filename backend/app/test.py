import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification
import pandas as pd
import os

# --- Sert juste à transfor
mapping_path = r"C:\Users\lucas\Documents\IPSSI\IA Cours\Projet\class_mapping.csv"
df_classes = pd.read_csv(mapping_path)
class_names = df_classes.sort_values("class_index")["class_name"].tolist()

# --- Étape 2 : Charger le modèle depuis Hugging Face ---
model_name = "anonauthors/stanford_dogs-resnet50"
processor = AutoImageProcessor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)

# --- Étape 3 : Charger et préparer une image ---
img_path = r"C:\Users\lucas\Documents\IPSSI\IA Cours\Projet\images\n02112706-Brabancon_griffon\n02112706_16.jpg"
image = Image.open(img_path).convert("RGB")
inputs = processor(images=image, return_tensors="pt")

# --- Étape 4 : Inférence ---
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    idx = logits.argmax(-1).item()
    prob = torch.softmax(logits, dim=1)[0, idx].item()

pred_label = class_names[idx]
print(f"Classe prédite : **{pred_label}** (probabilité : {prob:.2f})")
