
import pandas as pd

images_dir = r"C:\Users\lucas\Documents\IPSSI\IA Cours\Projet\images"


class_folders = [name for name in os.listdir(images_dir) if os.path.isdir(os.path.join(images_dir, name))]


cleaned_names = [name.split('-')[-1] for name in class_folders]

df_classes = pd.DataFrame({
    "class_index": range(len(cleaned_names)),
    "class_name": cleaned_names
})

df_classes.to_csv("class_mapping.csv", index=False)
print(df_classes.head())
