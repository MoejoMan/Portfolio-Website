import requests
import os

# ✅ Your PythonAnywhere username
username = "Moejoe06"

# ✅ API token (provided by GitHub secret)
api_token = os.environ["PA_API_TOKEN"]

# ✅ Your web app domain (update only if you change your PythonAnywhere app name)
webapp_domain = "Moejoe06.pythonanywhere.com"

# ✅ Reload URL for your web app
url = f"https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{webapp_domain}/reload/"

print("🚀 Triggering PythonAnywhere reload...")
response = requests.post(url, headers={"Authorization": f"Token {api_token}"})

if response.status_code == 200:
    print("✅ Successfully reloaded web app!")
else:
    print(f"❌ Reload failed with status {response.status_code}: {response.text}")
    exit(1)
