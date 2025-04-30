# Requirements:
# pip install flask azure-identity azure-keyvault-secrets

from flask import Flask, request, render_template_string
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Azure Key Vault Secret</title>
</head>
<body>
  <h1>Récupérer un secret depuis Azure Key Vault</h1>
  <form method="post">
    <label for="vault">Nom du Key Vault :</label><br>
    <input type="text" id="vault" name="vault" required><br><br>
    <label for="secret">Nom du secret :</label><br>
    <input type="text" id="secret" name="secret" required><br><br>
    <button type="submit">Valider</button>
  </form>
  {% if secret_value %}
    <h2>Valeur du secret :</h2>
    <pre>{{ secret_value }}</pre>
  {% endif %}
  {% if error %}
    <h2>Erreur :</h2>
    <pre>{{ error }}</pre>
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
    app.run(debug=True, host="0.0.0.0", port=5000)
