from typing import List
import os

class Settings:
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Dog Breed Classifier API"
    VERSION: str = "1.0.0"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
    
    # Model Configuration
    MODELS_DIR: str = os.path.join(os.path.dirname(__file__), "models", "models")
    MODEL_NAMES: List[str] = ["model1", "model2", "model3"]
    
    # Image Processing
    IMAGE_SIZE: tuple = (224, 224)
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "webp"]
    
    # Dog Breeds (120 most common breeds)
    DOG_BREEDS: List[str] = [
        "Affenpinscher", "Afghan Hound", "Airedale Terrier", "Akita", "Alaskan Malamute",
        "American Bulldog", "American Pit Bull Terrier", "American Staffordshire Terrier",
        "Australian Cattle Dog", "Australian Shepherd", "Basenji", "Basset Hound", "Beagle",
        "Belgian Malinois", "Bernese Mountain Dog", "Bichon Frise", "Bloodhound", "Border Collie",
        "Border Terrier", "Boston Terrier", "Boxer", "Brittany", "Bull Terrier", "Bulldog",
        "Bullmastiff", "Cairn Terrier", "Cavalier King Charles Spaniel", "Chihuahua",
        "Chinese Crested", "Chow Chow", "Cocker Spaniel", "Collie", "Coonhound", "Corgi",
        "Dachshund", "Dalmatian", "Doberman Pinscher", "English Setter", "English Springer Spaniel",
        "Fox Terrier", "French Bulldog", "German Shepherd", "German Shorthaired Pointer",
        "Golden Retriever", "Great Dane", "Great Pyrenees", "Greyhound", "Havanese",
        "Irish Setter", "Irish Wolfhound", "Jack Russell Terrier", "Japanese Chin",
        "Labrador Retriever", "Maltese", "Mastiff", "Miniature Schnauzer", "Newfoundland",
        "Norwegian Elkhound", "Old English Sheepdog", "Papillon", "Pekingese", "Pointer",
        "Pomeranian", "Poodle", "Portuguese Water Dog", "Pug", "Rhodesian Ridgeback",
        "Rottweiler", "Saint Bernard", "Saluki", "Samoyed", "Scottish Terrier", "Shar Pei",
        "Shiba Inu", "Shih Tzu", "Siberian Husky", "Staffordshire Bull Terrier", "Vizsla",
        "Weimaraner", "Welsh Corgi", "West Highland White Terrier", "Whippet", "Yorkshire Terrier",
        "Australian Kelpie", "Belgian Tervuren", "Bernedoodle", "Catahoula Leopard Dog",
        "English Bulldog", "German Pinscher", "Giant Schnauzer", "Gordon Setter", "Italian Greyhound",
        "Keeshond", "Leonberger", "Lhasa Apso", "Norwegian Lundehund", "Nova Scotia Duck Tolling Retriever",
        "Otterhound", "Pharaoh Hound", "Plott Hound", "Redbone Coonhound", "Russell Terrier",
        "Smooth Fox Terrier", "Soft Coated Wheaten Terrier", "Spanish Water Dog", "Standard Schnauzer",
        "Sussex Spaniel", "Tibetan Mastiff", "Tibetan Spaniel", "Tibetan Terrier", "Toy Fox Terrier",
        "Treeing Walker Coonhound", "Welsh Springer Spaniel", "Welsh Terrier", "Wire Fox Terrier",
        "Xoloitzcuintli", "American Eskimo Dog", "Anatolian Shepherd Dog", "Black Russian Terrier",
        "Bluetick Coonhound", "Boerboel", "Bouvier des Flandres", "Boykin Spaniel", "Bracco Italiano",
        "Briard", "Brussels Griffon", "Canaan Dog", "Cane Corso", "Cardigan Welsh Corgi",
        "Chinese Shar Pei", "Clumber Spaniel", "Curly Coated Retriever", "English Cocker Spaniel",
        "Field Spaniel", "Finnish Lapphund", "Flat Coated Retriever", "German Wirehaired Pointer",
        "Glen of Imaal Terrier", "Greater Swiss Mountain Dog", "Ibizan Hound", "Icelandic Sheepdog"
    ]

settings = Settings()
