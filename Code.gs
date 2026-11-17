function sendConfirmationEmail(e) {
  if (!e) return;

  var sheet = SpreadsheetApp.getActiveSheet();
  var row = e.range.getRow();
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var rowData = sheet.getRange(row, 1, 1, sheet.getLastColumn()).getValues()[0];

  var email = "";
  for (var i = 0; i < headers.length; i++) {
    var headerStr = String(headers[i]).toLowerCase();
    if (headerStr.indexOf("e-mail") > -1 || headerStr.indexOf("email") > -1) {
      email = String(rowData[i]).trim();
      break;
    }
  }

  if (!email || email === "") return;

  function getValueByName(columnName) {
    for (var i = 0; i < headers.length; i++) {
      if (String(headers[i]).trim() === columnName) {
        return rowData[i] ? String(rowData[i]).trim() : '';
      }
    }
    return '';
  }

  var nom = getValueByName('Nom') || 'Participant';
  var role = getValueByName('Quel est votre profil ?');
  var whatsapp = getValueByName('Numéro de téléphone');
  var linkedin = getValueByName('Lien Linkedin');
  
  var colonneLienPerso = 'Lien Personnalisé à afficher sur le badge (portfolio/site web/...)';
  var lienPerso = getValueByName(colonneLienPerso);

  var sujet = "Confirmation de votre inscription - Youth Startups 2.0";
  var lienPersoHtml = lienPerso ? `<li style="margin-bottom: 8px;"><b>Lien Personnalisé :</b> <a href="${lienPerso}" style="color: #53b3b0; text-decoration: none; font-weight: bold;">Visiter le site</a></li>` : '';

  var htmlMessage = `
  <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: auto; background-color: #f8fafc; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0;">
      
      <!-- Section Logos-->
      <div style="text-align: center; padding-bottom: 20px; padding-top: 10px;">
      <img src="https://drive.google.com/uc?export=view&id=1EUIFvFAFqFM0hXcisXTaRpUzhJTfoyU4" alt="JCI Monastir" style="height: 80px; margin-right: 25px; vertical-align: middle;">
      <img src="https://drive.google.com/uc?export=view&id=1WZueuHmyz2WVW7BuqxU1BZio3223gWv5" alt="Youth Startups" style="height: 80px; vertical-align: middle;">
</div>

      <div style="text-align: center; background-color: #4c5b73; padding: 25px 20px; border-radius: 10px 10px 0 0;">
          <h1 style="color: #ffffff; margin: 0; font-size: 26px; text-transform: uppercase; letter-spacing: 2px;">Youth Startups 2.0</h1>
      </div>
      
      <!-- Corps du message -->
      <div style="background-color: #ffffff; padding: 35px 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0;">
          
          <!-- Titre -->
          <h2 style="color: #e67e22; margin-top: 0; font-size: 22px;">Inscription Validée ! 🎉</h2>
          
          <p style="color: #334155; font-size: 16px;">Bonjour <strong style="color: #4c5b73;">${nom}</strong>,</p>
          
          <p style="color: #475569; font-size: 15px; line-height: 1.6;">
              Votre place pour <b>Youth Startups 2.0</b> est confirmée. Nous sommes ravis de vous compter parmi nous en tant que <strong style="color: #e67e22;">${role}</strong>.
          </p>
          
          <p style="color: #475569; font-size: 15px; line-height: 1.6;">
              Le jour de l'événement, vous recevrez un <i>Smart Badge</i> équipé de votre QR Code unique. Voici les informations qui y seront encodées. <br><br>
              <strong style="color: #4c5b73;">En cas d'erreur, vous pouvez toujours changer ces informations dans la formulaire</strong>
          </p>
          
          <!-- Boîte -->
          <div style="background-color: #f0fdfc; border-left: 5px solid #53b3b0; padding: 20px; margin: 30px 0; border-radius: 0 8px 8px 0; border-top: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0;">
              <h3 style="color: #4c5b73; margin-top: 0; font-size: 17px; border-bottom: 2px solid #53b3b0; padding-bottom: 10px; display: inline-block;">Vos données de réseautage</h3>
              <ul style="color: #334155; font-size: 15px; margin-bottom: 0; padding-left: 20px; line-height: 1.6; margin-top: 15px;">
                  <li style="margin-bottom: 8px;"><b>WhatsApp :</b> ${whatsapp}</li>
                  <li style="margin-bottom: 8px;"><b>LinkedIn :</b> <a href="${linkedin}" style="color: #53b3b0; text-decoration: none; font-weight: bold;">Vérifier mon profil</a></li>
                  ${lienPersoHtml}
              </ul>
          </div>
          
          <p style="color: #4c5b73; font-size: 16px; font-weight: bold; margin-top: 40px; margin-bottom: 0;">À très vite,<br>L'équipe Youth Startups 2.0</p>
      </div>
  </div>
  <p style="color: #94a3b8; font-size: 11px; text-align: center; margin-top: 30px;">Vous recevez cet e-mail car vous vous êtes inscrit à l'événement Youth Startups 2.0. Si vous n'êtes pas à l'origine de cette inscription, veuillez nous ignorer.</p>
  `;

  try {
    MailApp.sendEmail({
      to: email,
      subject: sujet,
      htmlBody: htmlMessage,
      name: "Youth Startups 2.0"
    });
  } catch(err) {
    console.log("Erreur : " + err.message);
  }
}

function envoyerVersSupabase(e) {
  //Identifiants Supabase
  var supabaseUrl = "https://****.supabase.co";
  var supabaseKey = "sb_secret_****";

  var nom = e.namedValues['Nom et Prénom'] ? e.namedValues['Nom et Prénom'][0] : "";
  var email = e.namedValues['Adresse Email'] ? e.namedValues['Adresse Email'][0] : "";
  var whatsapp = e.namedValues['Numéro WhatsApp'] ? e.namedValues['Numéro WhatsApp'][0] : "";
  var linkedin = e.namedValues['Lien LinkedIn'] ? e.namedValues['Lien LinkedIn'][0] : "";
  var role = e.namedValues['Rôle'] ? e.namedValues['Rôle'][0] : "";
  var portfolio = e.namedValues['Lien Personnalisé à afficher sur le badge (portfolio/site web/...)'] ? e.namedValues['Lien Personnalisé à afficher sur le badge (portfolio/site web/...)'][0] : "";
  
  var data = {
    "name": nom,
    "email": email,
    "whatsapp": whatsapp,
    "linkedin_url": linkedin,
    "portfolio_url": portfolio,
    "role": role
  };

  var options = {
    "method": "post",
    "contentType": "application/json",
    "headers": {
      "apikey": supabaseKey,
      "Authorization": "Bearer " + supabaseKey,
      "Prefer": "return=minimal",
      "Content-Profile": "youth_startup"
    },
      "payload": JSON.stringify(data)
  };

  try {
    UrlFetchApp.fetch(supabaseUrl, options);
    Logger.log("Succès : Données envoyées à Supabase pour " + nom);
  } catch (error) {
    Logger.log("Erreur lors de l'envoi à Supabase : " + error);
  }
}
