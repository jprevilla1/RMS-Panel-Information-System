# Panel IMS — Information and Management System for Market Research

A web application for managing the **panel update** process of a Retail
Measurement Service (RMS) market-research company. It centralizes shop-profile
management, automates extrapolation-factor calculation, visualizes panel stores
on a map, and provides a panel-health dashboard — all backed by a PostgreSQL
database.

Built with [Dash](https://dash.plotly.com/) (Plotly) and PostgreSQL. This
repository accompanies the IE 271 capstone paper (see [`docs/`](docs/)).

## Features

- **User authentication** — log in / sign up against a `registeredusers` table.
- **Shop database management** — add, edit, and soft-delete shop records.
- **Extrapolation retrieval** — auto-recalculated extrapolation factors per
  segment, viewable and downloadable as CSV.
- **Store mapper** — map-based visualization of panel stores, filterable by
  segment and attribute.
- **Dashboard** — a two-tab dashboard (Sample Status & Market Simulation) of
  key panel volume and simulated-sales metrics.

## Tech stack

| Layer    | Technology                              |
|----------|-----------------------------------------|
| Frontend | Dash, Dash Bootstrap Components, Plotly  |
| Backend  | Python, Flask (via Dash)                 |
| Database | PostgreSQL (developed with pgAdmin)      |

## Project structure

```
.
├── app.py              # Dash app object & global config
├── index.py            # URL router / entry point
├── dbconnect.py        # DB connection + query/modify helpers (env-driven)
├── requirements.txt
├── sql_scripts.sql     # Schema + seed data (run this first)
├── .env.example        # Template for DB credentials
├── apps/               # One module per page/feature
│   ├── commonmodules.py    # Shared navbars
│   ├── login.py / signup.py
│   ├── home.py
│   ├── dbmanager.py / addmodule.py / modifymodule.py
│   ├── submitupdate.py / deletemodule.py
│   ├── efactorcalc.py / efactorview.py
│   ├── storemapper.py
│   └── dashboard.py
├── assets/             # CSS served by Dash
└── docs/               # Capstone paper (PDF + corrected Markdown) and report
```

## Getting started

### Prerequisites

- Python 3.10+
- PostgreSQL 13+ (with a database you can connect to)

### 1. Clone and install

```bash
git clone <your-repo-url>.git
cd RMS-Panel-Information-System
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Create the database

Create a PostgreSQL database (default name `271casedb`), then run the schema and
seed script:

```bash
psql -U postgres -d 271casedb -f sql_scripts.sql
```

(Or open `sql_scripts.sql` in pgAdmin and execute it.)

### 3. Configure credentials

Copy the example env file and edit it to match your PostgreSQL setup:

```bash
cp .env.example .env
```

`dbconnect.py` reads `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PORT`, and
`DB_PASSWORD` from the environment, falling back to local defaults if they are
unset — so the app runs out of the box for local development.

### 4. Run

```bash
python index.py
```

The app opens at <http://127.0.0.1:8050/>.

Sample login (from the seed data): username `jdoe`, password `doe10001`.

## Security notes

This is an academic project. Before any production or shared deployment, address
the following known limitations:

- **Passwords are stored and compared in plain text.** Replace with a hashing
  scheme such as `bcrypt` or `argon2`.
- **No role-based access control** — every authenticated user can reach every
  module.
- Credentials are read from environment variables; never commit a real `.env`
  file (it is git-ignored).

## Notes on this build

This upload-ready copy differs from the raw working folder in a few ways:

- `__pycache__/` directories are excluded (see `.gitignore`).
- `requirements.txt` was re-encoded as UTF-8 and the invalid `app==0.0.1`
  entry removed.
- Database credentials moved to environment variables with safe fallbacks.
- Two scratch files from the working folder were left out: `dash_connections.py`
  (an incomplete experiment) and `test_db.py` (an ad-hoc connection test). The
  duplicate `apps/dbconnect.py` was removed in favor of the single root
  `dbconnect.py` that the app actually imports.

## License

No license has been specified. Add one (e.g. MIT) if you intend others to reuse
this code.
