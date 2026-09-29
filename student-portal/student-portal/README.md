# 🎓 Student Registration Portal

A simple, attractive, ready-to-deploy Flask web app for registering and managing
student records (Name, Age, DOB, Gender, Email, Phone, Address, Course, Study Year).

- Single-page UI (form + live student list) — `templates/index.html`
- Edit page for updating a record — `templates/edit.html`
- **SQLite by default** — zero configuration, works out of the box
- **Optional PostgreSQL** — just set one environment variable (`DATABASE_URL`) and Render's Postgres is used automatically
- Ready to deploy on **Render** in a few clicks

---

## 📁 Project Structure

```
student-portal/
├── app.py                 # Flask app (routes, model, DB config)
├── templates/
│   ├── index.html          # Main page: registration form + student table
│   └── edit.html           # Edit student page
├── requirements.txt
├── Procfile                # tells Render/Heroku how to run the app
├── render.yaml              # one-click Render Blueprint config
├── runtime.txt              # Python version
├── .env.example
└── .gitignore
```

---

## 🚀 Run Locally

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Open **http://localhost:5000** in your browser. A `students.db` SQLite file is
created automatically on first run — no setup needed.

---

## ☁️ Deploy on Render (SQLite — default, simplest)

1. Push this project to a GitHub repository.
2. Go to [render.com](https://render.com) → **New +** → **Web Service**.
3. Connect your GitHub repo.
4. Render will auto-detect settings, or set manually:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **Create Web Service**. Done! 🎉

> ⚠️ Note: Render's free-tier filesystem is **ephemeral** — the SQLite file
> resets on redeploys/restarts. This is fine for demos/testing. For persistent
> data, use the PostgreSQL option below.

### Even faster: One-click Blueprint deploy
This repo includes a `render.yaml` file. On Render, choose
**New + → Blueprint**, point it at your repo, and Render will configure the
service automatically using that file.

---

## 🐘 Switch to Render PostgreSQL (optional, persistent storage)

The app already contains the logic to use PostgreSQL — you just need to turn it on:

1. On Render: **New +** → **PostgreSQL** → create a free database.
2. Copy the **Internal Database URL** it gives you (starts with `postgres://`).
3. Go to your Web Service → **Environment** tab → **Add Environment Variable**:
   - Key: `DATABASE_URL`
   - Value: *(paste the Internal Database URL)*
4. Save changes — Render will redeploy automatically.

That's it. The app detects `DATABASE_URL` and switches from SQLite to
PostgreSQL automatically (see `app.py`, it also auto-fixes the
`postgres://` → `postgresql://` prefix that SQLAlchemy requires).

To switch back to SQLite, just remove the `DATABASE_URL` environment variable.

---

## 🔑 Environment Variables

| Variable       | Required | Default              | Description                              |
|----------------|----------|-----------------------|-------------------------------------------|
| `SECRET_KEY`   | No       | dev key (insecure)    | Flask session secret — set a random value in production |
| `DATABASE_URL` | No       | *(uses SQLite)*       | Set to a PostgreSQL URL to use Postgres instead |
| `PORT`         | No       | 5000                  | Set automatically by Render                |

---

## ✨ Features

- Attractive single-page form: Name, Age, DOB, Gender, Email, Phone, Address, Course, Study Year
- Live table of all registered students on the same page
- Edit and Delete actions for every record
- Flash messages for success/error feedback
- `/api/students` — JSON endpoint listing all students
- `/health` — simple health-check endpoint

---

## 🛠️ Tech Stack

- Flask 3
- Flask-SQLAlchemy
- SQLite (default) / PostgreSQL (optional)
- Gunicorn (production server)
- Plain HTML/CSS (no frontend framework needed)
