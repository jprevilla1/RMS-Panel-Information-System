import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from dash.dependencies import Input, Output, State
from app import app

# CSS Styling for the Navlink components
navlink_style = {
    'color' : '#fff',
    'textDecoration':"none"
}

navbar_home = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Panel IMS Portal Singapore", className="ms-2")),
                ],
                align='center',
                className='me-auto', 
            ),
            href='/home',
            style={'textDecoration':"none"},
        ),
        dbc.NavLink("Sign Out", href="/login", className='ms-auto', style=navlink_style),
    ],
    dark=True,
    color='info',
    style={'height':'40px'},
    className='m-0'
)

navbar_dbmanager = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Panel IMS Portal Singapore", className="ms-2")),
                ],
                align='center',
                className='me-auto',
            ),
            href='/dbmanager',
            style={'textDecoration':"none"},
        ),
        dbc.NavLink("Sign Out", href="/login", className='ms-auto', style=navlink_style),
    ],
    dark=True,
    color='info',
    style={'height':'40px'},
    className='m-0'
)


navbar_modifymodule = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Panel IMS Portal Singapore", className="ms-2")),
                ],
                align='center',
                className='me-auto',
            ),
            href='/modifymodule',
            style={'textDecoration':"none"},
        ),
        dbc.NavLink("Sign Out", href="/login", className='ms-auto', style=navlink_style),
    ],
    dark=True,
    color='info',
    sticky="top",
    style={'height':'40px'},
    className='m-0'
)

# @app.callback(
#     [
#         Output('hello_user', 'value'),
#     ],
#     [
#         Input('user_store', 'value'),
#     ]
# )

# def showuser(user):
#     return ["Hi, " + user + "!"]