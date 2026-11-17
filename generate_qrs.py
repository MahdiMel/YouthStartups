import csv
import qrcode
from PIL import Image
import os
import re

output_dir = "qrcodes"
os.makedirs(output_dir, exist_ok=True)

base_url = "https://youthstartupsmonastir.github.io/youthstartups2.0/connect.html?scanned="

logo_path = r"images\logo ys.png" 

try:
    logo = Image.open(logo_path)
except FileNotFoundError:
    print(f"Erreur: Le fichier '{logo_path}' est introuvable.")
    exit()

with open('attendees.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        attendee_id = row['id']
        clean_name = "".join(char for char in row['name'] if char.isalnum() or char == ' ')
        attendee_name = clean_name.strip().replace(" ", "_")
        qr_data = f"{base_url}{attendee_id}"
        
        qr = qrcode.QRCode(
            version=5, 
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10, 
            border=4
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        img_width, img_height = qr_img.size
        logo_size = int(img_width * 0.25)
        
        logo_resized = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        pos = ((img_width - logo_size) // 2, (img_height - logo_size) // 2)
        
        if logo_resized.mode == 'RGBA':
            qr_img.paste(logo_resized, pos, logo_resized)
        else:
            qr_img.paste(logo_resized, pos)
        
        filename = os.path.join(output_dir, f"{attendee_name}_QR.png")
        qr_img.save(filename)
        
        print(f"Badge généré avec logo Youth Startups pour : {row['name']}")

print("\nTous les badges ont été générés avec succès !")