# Portfolio Website

Personal portfolio for Joseph Hayes Gonzalez, a BSc Cybersecurity and Digital Forensics student at Anglia Ruskin University. Live at https://moejoe06.pythonanywhere.com/

Built with Flask and plain HTML and CSS, and deployed to PythonAnywhere by GitHub Actions on every push to `main`.

## Pages

| Route | Template | Purpose |
|---|---|---|
| `/` | `main_page.html` | Home, highlights, and timeline |
| `/projects` | `projects.html` | Project showcase |
| `/case-study/cambridge-fibre` | `case_study.html` | Design level case study of a commercial project (private code) |
| `/about` | `about.html` | Background, skills, tools, and homelab |
| `/contact` | `contact.html` | Contact details and links |

## Run locally

```bash
git clone https://github.com/MoejoMan/Portfolio-Website.git
cd Portfolio-Website
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then set SECRET_KEY to a long random value
python flask_app.py
```

## Configuration

The app reads `SECRET_KEY` from the environment or from a local `.env` or `prtlnkps.env` file. These files are listed in `.gitignore` and must never be committed. Generate a key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Deployment

`.github/workflows/deploy.yml` packages the project and uploads it to PythonAnywhere using the `PA_USERNAME` and `PA_API_TOKEN` repository secrets.