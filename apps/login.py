import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

from app import app
import dbconnect as db

style={
        'justifyContent': 'center',
        'alignItems': 'center',
        'padding': "20px",
        'max-width': "500px",
        'margin': "auto",
    }

layout = html.Div(
    [
        dcc.Store(id='user_store'),
        
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4("Panel IMS Singapore", style={'font-weight':'600', "color": "#0dcaf0"}, className='text-center'),
                        html.H6("Login Portal", style={'fontWeight':'normal'}, className='text-center'),
                        dbc.Form(
                        [
                        dbc.CardGroup(
                            [
                            dcc.Input(
                                id="username",
                                type='text',
                                placeholder='Username',
                                style={'width': '100%', 'padding': '10px', 'marginBottom': '10px'}
                                ),
                            dcc.Input(
                                id='password',
                                type='password',
                                placeholder='Password',
                                style={'width': '100%', 'padding': '10px', 'marginBottom': '20px'}
                                ),
                            html.Div(id='login_output', style={'marginTop': '20px', 'color': 'red'}),
                            dbc.Alert('Invalid username or password!', id='login_alert', color='danger', is_open=False),
                            ]
                            ),
                        html.Button("Log In", 
                                    id='login_btn', 
                                    n_clicks=0,
                                    style={'width': "100%", 'padding': "10px", 'color': "primary"},
                                    className="btn btn-outline-secondary btn-block custom-btn",
                                    ),  
                        ]
                        ),
                    html.Br(),
                    html.Div("New user?", className='text-center'),
                    html.A("Create an Account", 
                                href='/signup',
                                # id='signup_btn', 
                                # n_clicks=0,
                                style={'width': "100%", 'padding': "10px", 'color': "primary"},
                                className="btn btn-outline-secondary btn-block custom-btn",
                                ),
                    ]
                    )
            ],
            style={'backgroundColor': '#f4f4f4'},
            className='container mt-5'  
            ),
    ],
className='container mt-5',
style= style
)


@app.callback(
    [
        Output('login_output', 'children'),
        Output('login_alert', 'is_open'),
        Output('url', 'pathname'),
        Output('user_store', 'data'),
    ],
    [
        Input('login_btn', 'n_clicks'),
    ],
    [
        State('username', 'value'),
        State('password', 'value'),
        State('url', 'pathname'),
    ]
)


def authenticate(login_clicks, username, password, pathname):

    ctx = dash.callback_context

    if ctx.triggered: 

        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        alert_open = False
        
        if eventid == 'login_btn' and login_clicks:
            if all([username, password]):
                sql = """SELECT username, userpassword FROM registeredusers
                        WHERE  
                            is_active = 1 AND 
                            username = %s AND
                            userpassword = %s
                        """
                df = db.querydatafromdatabase(sql, [username, password], ['username', 'userpassword'])

                if df.shape[0] > 0:
                    user_login = 1
                    alert_open = False
                    url = '/home'
                else:
                    user_login = -1
                    alert_open = True
                    url = dash.no_update
            else:
                user_login = -1
                alert_open = True
                url = dash.no_update
        else: 
            raise PreventUpdate

    else: 
        raise PreventUpdate
    
    return ['', alert_open, url, username]
