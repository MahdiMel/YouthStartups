import csv
import smtplib
from email.message import EmailMessage
import io
from supabase import create_client, Client, ClientOptions

# --- CONFIGURATION SUPABASE ---
SUPABASE_URL = "https://bgykmhfbrvqsvxfdiilt.supabase.co"
SUPABASE_SECRET_KEY = "sb_secret_pAzz8uBdsDs--S36gu6AJA_S_szMatt" 
opts = ClientOptions(schema="youth_startup")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY, options=opts)

# --- CONFIGURATION EMAIL ---
EMAIL_SENDER = "youthstartups.monastir@gmail.com"
EMAIL_PASSWORD = "fzfj wcfi dvfe accf"

def fetch_data():
    """Récupère toutes les données nécessaires depuis Supabase."""
    print("Récupération des données depuis Supabase...")
    attendees_res = supabase.table("attendees").select("*").execute()
    connections_res = supabase.table("connections").select("*").execute()
    
    attendees_dict = {a['id']: a for a in attendees_res.data}
    return attendees_dict, connections_res.data

def distribute_emails():
    attendees_dict, connections = fetch_data()
    
    scans_by_user = {}
    for conn in connections:
        scanner = conn['scanner_id']
        scanned = conn['scanned_id']
        if scanner not in scans_by_user:
            scans_by_user[scanner] = []
        scans_by_user[scanner].append(scanned)

    print(f"Préparation de l'envoi pour {len(scans_by_user)} participants actifs...")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        
        for scanner_id, scanned_ids in scans_by_user.items():
            scanner_info = attendees_dict.get(scanner_id)
            if not scanner_info:
                continue
                
            scanner_email = scanner_info['email']
            scanner_name = scanner_info['name']
            
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(['Nom', 'WhatsApp', 'LinkedIn', 'Portfolio']) # En-têtes
            
            html_rows = ""
            
            for scanned_id in scanned_ids:
                contact = attendees_dict.get(scanned_id)
                if contact:
                    c_name = contact.get('name', '') or ''
                    c_wa = contact.get('whatsapp', '') or ''
                    c_in = contact.get('linkedin_url', '') or ''
                    c_port = contact.get('portfolio_url', '') or ''
                    
                    writer.writerow([c_name, c_wa, c_in, c_port])
                    
                    link_wa = f'<a href="https://wa.me/{c_wa.replace("+", "").replace(" ", "")}" style="color: #53b3b0; text-decoration: none; font-weight: bold;">{c_wa}</a>' if c_wa else '-'
                    link_in = f'<a href="{c_in}" style="color: #53b3b0; text-decoration: none; font-weight: bold;">Voir Profil</a>' if c_in else '-'
                    link_port = f'<a href="{c_port}" style="color: #53b3b0; text-decoration: none; font-weight: bold;">Visiter</a>' if c_port else '-'
                    
                    html_rows += f"""
                    <tr>
                        <td style="padding: 12px 10px; border-bottom: 1px solid #e2e8f0; color: #334155; font-weight: bold;">{c_name}</td>
                        <td style="padding: 12px 10px; border-bottom: 1px solid #e2e8f0; color: #334155;">{link_wa}</td>
                        <td style="padding: 12px 10px; border-bottom: 1px solid #e2e8f0; color: #334155;">{link_in}</td>
                        <td style="padding: 12px 10px; border-bottom: 1px solid #e2e8f0; color: #334155;">{link_port}</td>
                    </tr>
                    """
            
            msg = EmailMessage()
            msg['Subject'] = "Vos connexions pendant Youth Startups 2.0 "
            msg['From'] = f"Youth Startups <{EMAIL_SENDER}>"
            msg['To'] = scanner_email
            
            msg.set_content(f"""Bonjour {scanner_name},

Merci d'avoir participé à Youth Startups 2.0 ! Voici les coordonnées des personnes avec qui vous avez connecté. Vous trouverez également ces données au format CSV en pièce jointe.

L'équipe Youth Startups 2.0
""")
            
            html_content = f"""
            <html>
              <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #334155; line-height: 1.6; background-color: #ffffff; padding: 20px;">
                <div style="max-width: 650px; margin: auto; background: #ffffff; padding: 35px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    
                    <!-- Section Logos & en tete -->
                    <div style="text-align: center; padding-bottom: 20px; padding-top: 10px;">
                        <img src="https://drive.google.com/uc?export=view&id=1VNC6NjLllC9qrJeMKDV2-8Coh9rDB1cF" alt="Youth Startups" style="height: 70px; margin-right: 25px; vertical-align: middle;">
                        <img src="https://drive.google.com/uc?export=view&id=1WZueuHmyz2WVW7BuqxU1BZio3223gWv5" alt="JCI Monastir" style="height: 70px; vertical-align: middle;">
                    </div>

                    <div style="text-align: center; background-color: #4c5b73; padding: 25px 20px; border-radius: 10px 10px 0 0;">
                        <h2 style="color: #ffffff; margin: 0; font-size: 24px; text-transform: uppercase; letter-spacing: 2px;">Vos Connexions Pendant Youth Startups 2.0</h2>
                    </div>
                    
                    <!-- Corps du message -->
                    <div style="background-color: #ffffff; padding: 30px 20px; border-radius: 0 0 10px 10px; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0;">
                        
                        <h2 style="color: #e67e22; margin-top: 0; font-size: 22px;">Nouveaux Contacts ! 🎉</h2>
                        
                        <p style="font-size: 16px;">Bonjour <strong style="color: #4c5b73;">{scanner_name}</strong>,</p>
                        
                        <p style="font-size: 15px; color: #475569; line-height: 1.6;">
                            Merci d'avoir participé à <b>Youth Startups 2.0</b> ! Voici les coordonnées des personnes avec qui vous avez connecté. Vous trouverez également ces données au format CSV en pièce jointe.
                        </p>
                        
                        <div style="overflow-x: auto; margin-top: 30px;">
                            <table style="width:100%; border-collapse: collapse; font-size: 15px;">
                                <thead>
                                    <tr>
                                        <!-- En-têtes Turquoise (#53b3b0) -->
                                        <th style="background-color: #53b3b0; color: white; padding: 14px 10px; border: none; text-align: left; border-top-left-radius: 6px;">Nom</th>
                                        <th style="background-color: #53b3b0; color: white; padding: 14px 10px; border: none; text-align: left;">WhatsApp</th>
                                        <th style="background-color: #53b3b0; color: white; padding: 14px 10px; border: none; text-align: left;">LinkedIn</th>
                                        <th style="background-color: #53b3b0; color: white; padding: 14px 10px; border: none; text-align: left; border-top-right-radius: 6px;">Portfolio</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {html_rows}
                                </tbody>
                            </table>
                        </div>
                        
                        <p style="margin-top: 40px; font-weight: bold; color: #4c5b73; font-size: 16px;">À la prochaine,<br>L'équipe Youth Startups 2.0</p>
                    </div>
                </div>
              </body>
            </html>
            """
            
            msg.add_alternative(html_content, subtype='html')
            
            csv_bytes = csv_buffer.getvalue().encode('utf-8-sig') # utf-8-sig pour Excel
            msg.add_attachment(
                csv_bytes, 
                maintype='text', 
                subtype='csv', 
                filename='Mes_Connexions_YouthStartups.csv'
            )
            
            smtp.send_message(msg)
            print(f"✅ E-mail envoyé à {scanner_name} ({scanner_email}) avec {len(scanned_ids)} contacts.")

    print("Distribution terminée avec succès !")

if __name__ == "__main__":
    distribute_emails()