from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import stripe, pdfkit, json, os
from flask_mail import Mail, Message
from dotenv import load_dotenv
from utils.generate_text import generate_mentions_text, generate_cgv_text




from flask import flash

load_dotenv()
app = Flask(__name__)
stripe.api_key = os.getenv("STRIPE_API_KEY")
app.secret_key = os.getenv("SECRET_KEY")


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

stripe.api_key = os.getenv("STRIPE_API_KEY")


mail = Mail(app)

from flask import redirect, url_for

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    import json
    data = json.loads(request.form['data'])
    session['user_data'] = data  # session Flask, on garde

    # ⚠️ On NE l'appelle plus "session" ici !
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': 'Mentions légales + CGV PDF',
                },
                'unit_amount': 500,  # 5 €
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('success', _external=True),
        cancel_url=url_for('cancel', _external=True),
    )

    return redirect(checkout_session.url, code=303)


@app.route('/success')
def success():
    session['paid'] = True
    data = session.get('user_data')

    if not data:
        return "Erreur : données manquantes."

    return render_template('success.html', data=data)


@app.route('/cancel')
def cancel():
    return "<h1>Paiement annulé ❌</h1><p><a href='/'>Retour à l'accueil</a></p>"

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    from utils.generate_text import generate_mentions_text, generate_cgv_text
    import json

    data = json.loads(request.form['data'])
    mentions = generate_mentions_text(data)
    cgv = generate_cgv_text(data)
    texte = mentions + "<hr><br>" + cgv

    import pdfkit
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")  # adapte le chemin si besoin

    full_html = f"""
    <!DOCTYPE html>
    <html lang='fr'>
    <head>
      <meta charset='UTF-8'>
      <title>Mentions légales</title>
  <style>
    body {{
      font-family: 'Segoe UI', sans-serif;
      font-size: 15px;
      color: #222;
      padding: 50px;
      line-height: 1.7;
      background: white;
    }}

    h2 {{
      font-size: 20px;
      margin-top: 40px;
      margin-bottom: 15px;
      color: #2c3e50;
      border-bottom: 1px solid #ccc;
      padding-bottom: 5px;
    }}

    /* … etc … */
  </style>
    </head>
    <body>
      <div class="section">
        {mentions}
      </div>
      <hr>
      <div class="section">
        {cgv}
      </div>
    </body>
    </html>
    """

    pdf = pdfkit.from_string(full_html, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=mentions_legales.pdf'
    return response


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = {
        'nom_entreprise': request.form['nom_entreprise'],
        'adresse': request.form['adresse'],
        'statut': request.form['statut'],
        'email': request.form['email'],
        'siret': request.form['siret']
    }

    # 💾 On stocke les données dans la session pour les réutiliser après le paiement
    session['user_data'] = json.dumps(data)  # stocke les données du formulaire

    texte_mentions = generate_mentions_text(data)

    return render_template('result.html', data=data, texte=texte_mentions)


if __name__== '__main__':
    app.run(debug=True)