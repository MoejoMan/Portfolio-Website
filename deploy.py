import os
import requests
import zipfile
import io
from dotenv import load_dotenv

# Load local env files so we don't hardcode tokens; expects PA_USERNAME and PA_API_TOKEN to be set.
load_dotenv()
load_dotenv("pa.env")  # optional local file for PythonAnywhere creds; keep out of git


def get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}. Set it in your shell or pa.env before running deploy.")
    return value


username = get_env("PA_USERNAME")
api_token = get_env("PA_API_TOKEN")
webapp_name = "Moejoe06.pythonanywhere.com"

# Zip your project folder
def zip_project():
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith((".py", ".html", ".css", ".js")):  # only relevant files
                    path = os.path.join(root, file)
                    zf.write(path, os.path.relpath(path, "."))
    mem_zip.seek(0)
    return mem_zip

print("🚀 Uploading project to PythonAnywhere...")

files = {"content": ("project.zip", zip_project())}

upload_url = f"https://www.pythonanywhere.com/api/v0/user/{username}/files/path/home/{username}/mysite/project.zip"

resp = requests.post(upload_url, headers={"Authorization": f"Token {api_token}"}, files=files)
if resp.status_code in (200, 201):
    print("✅ Uploaded zip successfully!", resp.text)
else:
    print(f"❌ Upload failed: {resp.status_code} {resp.text}")
    exit(1)

# Extract zip on PythonAnywhere
extract_url = f"https://www.pythonanywhere.com/api/v0/user/{username}/bash/path/home/{username}/mysite"
extract_cmd = f"unzip -o project.zip -d . && rm project.zip"
resp = requests.post(extract_url, headers={"Authorization": f"Token {api_token}"}, json={"command": extract_cmd})
if resp.status_code in (200, 201):
    print("✅ Extracted project successfully!", resp.text)
else:
    print(f"❌ Extract failed: {resp.status_code} {resp.text}")
    exit(1)

# Reload web app
reload_url = f"https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{webapp_name}/reload/"
resp = requests.post(reload_url, headers={"Authorization": f"Token {api_token}"})
if resp.status_code in (200, 201):
    print("✅ Web app reloaded successfully!", resp.text)
else:
    print(f"❌ Reload failed: {resp.status_code} {resp.text}")
    exit(1)
