# Requirements:
# pip install flask azure-identity azure-keyvault-secrets

from flask import Flask, request, render_template_string
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Azure Key Vault Secret</title>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap">
  <style>
    /* Animated gradient background */
    @keyframes gradient {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }

    body {
        margin: 0;
        height: 100vh;
        background: linear-gradient(-45deg, #0d0d0d, #1a1a1a, #0d0d0d, #1a1a1a);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #00ffea;
        font-family: 'Orbitron', sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        overflow: hidden;
    }

    /* Glitch effect */
    .glitch {
      position: relative;
      color: #e600ff;
    }
    .glitch::before,
    .glitch::after {
      content: attr(data-text);
      position: absolute;
      left: 0;
      top: 0;
      width: 100%;
      overflow: hidden;
      clip: rect(0, 900px, 0, 0);
    }
    .glitch::before {
      left: 2px;
      text-shadow: -2px 0 #00ffea;
      animation: glitch-anim 2s infinite linear alternate-reverse;
    }
    .glitch::after {
      left: -2px;
      text-shadow: -2px 0 #ff00ff;
      animation: glitch-anim2 3s infinite linear alternate-reverse;
    }
    @keyframes glitch-anim {
      0% { clip: rect(20px, 9999px, 44px, 0); }
      20% { clip: rect(14px, 9999px, 56px, 0); }
      40% { clip: rect(66px, 9999px, 88px, 0); }
      60% { clip: rect(10px, 9999px, 30px, 0); }
      80% { clip: rect(72px, 9999px, 94px, 0); }
      100% { clip: rect(0, 9999px, 0, 0); }
    }
    @keyframes glitch-anim2 {
      0% { clip: rect(49px, 9999px, 72px, 0); }
      20% { clip: rect(10px, 9999px, 34px, 0); }
      40% { clip: rect(88px, 9999px, 118px, 0); }
      60% { clip: rect(24px, 9999px, 50px, 0); }
      80% { clip: rect(60px, 9999px, 84px, 0); }
      100% { clip: rect(0, 9999px, 0, 0); }
    }

    h1 {
        font-size: 2.5em;
        margin-bottom: 1em;
        text-shadow: 0 0 10px #e600ff, 0 0 20px #ff00ff;
    }

    form {
        margin: 20px auto;
        width: 320px;
    }
    label {
        display: block;
        text-align: left;
        margin-bottom: 5px;
    }
    input[type="text"] {
        width: 100%;
        padding: 10px;
        border: 2px solid #00ffea;
        border-radius: 5px;
        background: rgba(26,26,26,0.8);
        color: #00ffea;
        margin-bottom: 15px;
        transition: border-color 0.3s;
    }
    input[type="text"]:focus {
        border-color: #e600ff;
        outline: none;
    }

    button {
        padding: 12px 24px;
        background: #e600ff;
        border: none;
        border-radius: 5px;
        color: #fff;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 0 10px #e600ff;
        transition: box-shadow 0.3s;
    }
    button:hover {
        box-shadow: 0 0 20px #ff00ff;
    }

    .secret {
        margin-top: 30px;
        font-size: 1.2em;
        padding: 20px;
        border: 2px solid #00ffea;
        border-radius: 5px;
        background: rgba(0, 255, 234, 0.1);
        opacity: 0;
        animation: fadeIn 1.5s forwards;
    }
    @keyframes fadeIn {
        to { opacity: 1; }
    }

    .error {
        color: #ff0044;
        margin-top: 30px;
    }
  </style>
</head>
<body>
  <h1 class="glitch" data-text="Récupérer un secret depuis Azure Key Vault">Récupérer un secret depuis Azure Key Vault</h1>
  <form method="post">
    <label for="vault">Nom du Key Vault :</label>
    <input type="text" id="vault" name="vault" required>
    <label for="secret">Nom du secret :</label>
    <input type="text" id="secret" name="secret" required>
    <button type="submit">Valider</button>
  </form>
  {% if secret_value %}
    <div class="secret glitch" data-text="{{ secret_value }}">
      <pre>{{ secret_value }}</pre>
    </div>
  {% endif %}
  {% if error %}
    <div class="error">
      <pre>{{ error }}</pre>
    </div>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    secret_value = None
    error = None
    if request.method == "POST":
        vault_name = request.form.get("vault")
        secret_name = request.form.get("secret")
        try:
            vault_url = f"https://{vault_name}.vault.azure.net/"
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=vault_url, credential=credential)
            secret = client.get_secret(secret_name)
            secret_value = secret.value
        except Exception as e:
            error = str(e)
    return render_template_string(TEMPLATE, secret_value=secret_value, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
