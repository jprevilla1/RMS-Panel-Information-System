from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app
import dbconnect as db
from apps import addmodule
from apps.commonmodules import navbar_home

from urllib.parse import urlparse, parse_qs

layout = html.Div(
    [
        dcc.Location(id='module_url', refresh=True),
        navbar_home,
        html.Br(),
        html.H4('Manage Shop Database'),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label('Select module: ', width=1.5),
                dbc.Col(
                    dbc.Button('Add New Shop', href='/addmodule', className="me-2 btn btn-primary btn-block", color='info'),
                    width="auto" 
                ),
                dbc.Col(
                    dbc.Button('Modify/Delete Shop', href='/modifymodule', className="me-2 btn btn-primary btn-block", color='dark'),
                    width="auto"   
                ),
            ]
        )
    ],
)
        