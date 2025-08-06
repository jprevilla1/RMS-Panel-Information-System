import dash
from dash import html, dcc, ctx, ALL, Input, Output, State
import psycopg2
import pandas as pd
import sqlite3

app = dash.Dash()
app.layout = html.Div([
    dcc.Input(
        id= 'number-in',
        value = 1,
        style = {'fontSize': 28}
    ),
    html.Button(
        id='submit-button',
        n_clicks=0,
        children='Submit',
        style={'fontSize':28}
    ),
    html.H1(
        id='number-out'
    )
])

@app.callback(
    [
        Output('number-out','children'),
    ],
    [
        Input('submit-button', 'n_clicks')
    ],
    [
        State('number-in', 'value')
    ]
)

def output(n_clicks, number):
    if n_clicks:
        sql = """SELECT * FROM shippers;"""
        print(querydatafromdatabase(sql, [], ['shipper_id', 'name', 'phone']))
    return [number]

def querydatafromdatabase(sql, values, dbcolumns):
    db = psycopg2.connect(
        user = 'north'
    )