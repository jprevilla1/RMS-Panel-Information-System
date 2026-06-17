"""Database helper functions for the Panel IMS app.

Connection settings are read from environment variables so that no credentials
need to be committed to source control. If a variable is not set, a sensible
local-development default is used (matching the values in the original project),
so the app still runs out of the box against a local PostgreSQL instance.

Copy `.env.example` to `.env` and adjust the values for your environment.
"""

import os

import pandas as pd
import psycopg2

try:
    # Optional: load variables from a local .env file if python-dotenv is installed.
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # python-dotenv is optional; environment variables still work without it.
    pass


def getdblocation():
    """Open and return a new PostgreSQL connection.

    Credentials are taken from the environment, falling back to local defaults.
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "271casedb"),
        user=os.getenv("DB_USER", "postgres"),
        port=int(os.getenv("DB_PORT", "5432")),
        password=os.getenv("DB_PASSWORD", "password"),
    )


def modifydatabase(sql, values):
    """Run an INSERT/UPDATE/DELETE statement and commit it.

    Arguments:
        sql    -- SQL statement with %s placeholders
        values -- list of values for the placeholders (use [] if none)
    """
    db = getdblocation()
    try:
        cursor = db.cursor()
        cursor.execute(sql, values)
        db.commit()
    finally:
        # Always close the connection, even if the query raises.
        db.close()


def querydatafromdatabase(sql, values, dfcolumns):
    """Run a SELECT query and return the result as a pandas DataFrame.

    Arguments:
        sql       -- SQL query with %s placeholders
        values    -- list of values for the placeholders (use [] if none)
        dfcolumns -- column names for the returned DataFrame
    """
    db = getdblocation()
    try:
        cur = db.cursor()
        cur.execute(sql, values)
        rows = pd.DataFrame(cur.fetchall(), columns=dfcolumns)
    finally:
        db.close()

    return rows
