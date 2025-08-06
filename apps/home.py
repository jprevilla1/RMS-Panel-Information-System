from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app
import dbconnect as db
from apps.commonmodules import navbar_home

layout = html.Div(
    [
        navbar_home,
        html.Br(),
        dbc.Label(id='hello_user'),
        html.H4('Welcome to Panel Information and Management System!'), #page header
        html.Hr(),
        html.A(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H5('Manage Shop Database'),
                            html.P('Add, modify, or delete shops in panel'),
                        ]
                    ),
                ],
                style={"width":"400px", "height":"100px", "padding":"5px", "color":"white","backgroundColor":"#343a40", "paddingBottom": "0"},
                className="mb-3"
            ),
            href='/dbmanager',
            style={"cursor":"pointer", "textDecoration":"none", "display":"inline-block", "width": "fit-content"},
            className='hover-shadow',
        ),
        html.Br(),
        html.A(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H5('Retrieve Extrapolation Factors'),
                            html.P('Download latest extrapolation factor of shops'),
                        ]
                    ),
                ],
                style={"width":"400px", "height":"100px", "padding":"5px", "color":"white","backgroundColor":"#343a40", "paddingBottom": "0"},
                className="mb-3"
            ),
            href='/efactorview',
            style={"cursor":"pointer", "textDecoration":"none", "display":"inline-block", "width": "fit-content"},
            className='hover-shadow',
        ),
        html.Br(),
        html.A(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H5('Locate Stores'),
                            html.P('Show store location in map'),
                        ]
                    ),
                ],
                style={"width":"400px", "height":"100px", "padding":"5px", "color":"white","backgroundColor":"#343a40","paddingBottom": "0" },
                className="mb-3"
            ),
            href='/storemapper',
            style={"cursor":"pointer", "textDecoration":"none", "display":"inline-block", "width": "fit-content"},
            className='hover-shadow',
        ),
        html.Br(),
        html.A(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H5('View Panel Health Dashboard'),
                            html.P('Display volume metrics and simulated sales on panel market'),
                        ]
                    ),
                ],
                style={"width":"400px", "height":"120px", "padding":"5px", "color":"white","backgroundColor":"#343a40","paddingBottom": "0" },
                className="mb-3"
            ),
            href='/dashboard',
            style={"cursor":"pointer", "textDecoration":"none", "display":"inline-block", "width": "fit-content"},
            className='hover-shadow',
        ),
        html.Br(),
    ]
)


# @app.callback(
#     [
#         Output('hello_user', 'children'),
#     ],
#     [
#         Input('url', 'pathname'),
#         Input('user_store', 'data'),
#     ],
# )

# def showuser(pathname, user):
#     if pathname == '/home':
#     # return [f"Hi, {user}!"]
#         return [f"Hi there! {pathname}"]