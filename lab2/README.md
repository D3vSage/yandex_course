## Quick start (Windows / PowerShell)

### 1) Create venv & install deps

```powershell
cd C:\lab2
python -m venv venv
.\venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install Django psycopg2-binary Jinja2
```

### 2) Create database (pgAdmin)

Create database `govdb` (Owner: `postgres`).

> Local dev uses PostgreSQL user **postgres** with password **postgres**.

### 3) Migrations

```powershell
python manage.py makemigrations elections
python manage.py migrate
```

### 4) Import CSV to DB

CSV file: [governors_county.csv](https://www.kaggle.com/datasets/unanimad/us-election-2020?select=governors_county.csv)

```powershell
python manage.py load_governors .\governors_county.csv
```

> If you import twice, `CountyResult` rows will duplicate.

### 5) Run server

```powershell
python manage.py runserver
```

Open:

* Main page: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Project structure

```
lab2/
  manage.py
  governors_county.csv
  gov_project/
    settings.py
    urls.py
    jinja2.py
  elections/
    models.py
    views.py
    management/
      commands/
        load_governors.py
  templates/
    index.html
    macros.html
```
