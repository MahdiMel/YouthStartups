import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

DOSSIER_TEMPLATES = "templates/"       
DOSSIER_QRCODES = "qrcodes/"         
DOSSIER_SORTIE = "badges_finaux/"     
FICHIER_DONNEES = "attendees.csv"

# Ajout de "EXPLORER" en majuscules dans le dictionnaire
TEMPLATES = {
    "EXPLORER": "explorer_A6_2.jpg",
    "FOUNDER": "founder_A6.jpg",
    "STAFF": "staff_A6.jpg",
    "FREELANCER": "freelancer_A6.jpg",
    "GUEST": "guest_A6_2.jpg"
}

# Création du dossier racine
os.makedirs(DOSSIER_SORTIE, exist_ok=True)

def generer_badge(nom, role):
    nom_fichier_template = TEMPLATES.get(role, TEMPLATES["EXPLORER"])
    chemin_template = os.path.join(DOSSIER_TEMPLATES, nom_fichier_template)
    
    try:
        # Ouverture de l'image de fond
        badge = Image.open(chemin_template).convert("RGBA")
    except FileNotFoundError:
        print(f"❌ Erreur : Modèle introuvable pour le rôle {role} ({chemin_template})")
        return

    # --- CONFIGURATION SPÉCIFIQUE SELON LE RÔLE ---
    if role == "STAFF":
        couleur_texte = (255, 255, 255) 
        offset_x = 0                    
        facteur_y_texte = 0.34          
        facteur_y_qr = 0.536
        
    elif role == "FOUNDER":
        couleur_texte = (27, 43, 76)
        offset_x = 3
        facteur_y_texte = 0.32
        facteur_y_qr = 0.531

    elif role == "FREELANCER":
        couleur_texte = (27, 43, 76)
        offset_x = 3                
        facteur_y_texte = 0.32          
        facteur_y_qr = 0.531
        
    else: # Pour EXPLORER et GUEST
        couleur_texte = (27, 43, 76)
        offset_x = 51
        facteur_y_texte = 0.32          
        facteur_y_qr = 0.535

    # 2. INTÉGRATION DU QR CODE
    nom_formate = nom.title().replace(" ", "_")
    chemin_qr = os.path.join(DOSSIER_QRCODES, f"{nom_formate}_QR.png")
    
    try:
        qr_code = Image.open(chemin_qr).convert("RGBA")
        taille_qr = (580, 580) 
        qr_code = qr_code.resize(taille_qr)
        
        position_x_qr = ((badge.width - taille_qr[0]) // 2) + offset_x
        position_y_qr = int(badge.height * facteur_y_qr)
        
        badge.paste(qr_code, (position_x_qr, position_y_qr), qr_code)
        
    except FileNotFoundError:
        print(f"⚠️ Attention : Fichier QR introuvable -> '{chemin_qr}'.")

    # 3. ÉCRITURE DU NOM DU PARTICIPANT EN HAUT
    draw = ImageDraw.Draw(badge)
    
    taille_police_initiale = 110
    taille_police = taille_police_initiale
    
    # On définit une largeur maximale (ex: 80% de la largeur du badge pour garder des marges)
    largeur_max_autorisee = badge.width * 0.70 
    
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", taille_police)
    except IOError:
        font = ImageFont.load_default()

    # Calcul initial de la taille du texte
    bbox = draw.textbbox((0, 0), nom, font=font)
    largeur_texte = bbox[2] - bbox[0]
    
    # Boucle qui réduit la taille de la police tant que le texte est trop grand
    while largeur_texte > largeur_max_autorisee and taille_police > 30:
        taille_police -= 5 # On diminue la police de 5 en 5
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", taille_police)
        except IOError:
            break
        
        bbox = draw.textbbox((0, 0), nom, font=font)
        largeur_texte = bbox[2] - bbox[0]

    # Recalcul de la position Y si la police a beaucoup rétréci pour que ça reste centré verticalement
    ajustement_y = (taille_police_initiale - taille_police) // 2
    
    position_x_texte = ((badge.width - largeur_texte) // 2) + offset_x
    position_y_texte = int(badge.height * facteur_y_texte) + ajustement_y

    draw.text((position_x_texte, position_y_texte), nom, font=font, fill=couleur_texte)

    # 4. SAUVEGARDE DU RÉSULTAT
    dossier_role = os.path.join(DOSSIER_SORTIE, role)
    os.makedirs(dossier_role, exist_ok=True) 
    
    chemin_sauvegarde = os.path.join(dossier_role, f"Badge_{nom}.jpg")
    badge.convert("RGB").save(chemin_sauvegarde, quality=95)
    print(f"✅ Badge généré dans {role} : Badge_{nom}.jpg")

# --- EXÉCUTION DU SCRIPT ---
try:
    # Construction du chemin absolu vers le fichier CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    fichier_csv_path = os.path.join(script_dir, FICHIER_DONNEES)
    
    df_participants = pd.read_csv(fichier_csv_path)
    
    for index, ligne in df_participants.iterrows():
        nom_participant = str(ligne['name']).strip().upper() 
        role_brut = str(ligne['role']).strip().upper()
        
        # Normalisation des rôles
        if "FOUNDER" in role_brut or "ENTREPRENEUR" in role_brut:
            role_normalise = "FOUNDER"
        elif "STAFF" in role_brut:
            role_normalise = "STAFF"
        elif "FREELANCE" in role_brut: 
            role_normalise = "FREELANCER"
        elif "GUEST" in role_brut:
            role_normalise = "GUEST"
        else:
            role_normalise = "EXPLORER"
            
        generer_badge(nom_participant, role_normalise)
        
except FileNotFoundError:
    print(f"❌ Erreur : Le fichier de données {fichier_csv_path} est introuvable.")