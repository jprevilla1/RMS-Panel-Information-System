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
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4("Create an Account", style={'fontWeight':"normal"}, className="text-center"),
                        html.Br(),
                        html.Div(dcc.Link("Back to Login Page", href="/", className="btn btn-primary")),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label('Employee ID Number', ),
                                        dbc.Input(id="emp_id", type="text", placeholder='Enter Employee ID (IDxxxxx)', maxLength=7, style={'width':"100%", 'padding':"10px", 'marginBottom':"5px"})
                                    ],
                                    width=12,
                                    className="mb-3",
                                )
                            ],
                            className="justify-content-center",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label('First Name', ),
                                        dbc.Input(id="firstname", type="text", placeholder='First Name', style={'width':"100%", 'padding':"10px", 'marginBottom':"5px"})
                                    ],
                                    width=12,
                                    className="mb-3",
                                )
                            ],
                            className="justify-content-center",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label('Last Name', ),
                                        dbc.Input(id="lastname", type="text", placeholder='Last Name', style={'width':"100%", 'padding':"10px", 'marginBottom':"5px"})
                                    ],
                                    width=12,
                                    className="mb-3",
                                )
                            ],
                            className="justify-content-center",                        
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label('Email', ),
                                        dbc.Input(id="email", type="text", placeholder='Enter company email address (@mail.com)', style={'width':"100%", 'padding':"10px", 'marginBottom':"5px"})
                                    ],
                                    width=12,
                                    className="mb-3",
                                )
                            ],
                            className="justify-content-center",                        
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label('Username', ),
                                        dbc.Input(id="username", type="text", placeholder='Enter username', style={'width':"100%", 'padding':"10px", 'marginBottom':"5px"})
                                    ],
                                    width=12,
                                    className="mb-3",
                                )
                            ],
                            className="justify-content-center",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label('Password', ),
                                        dbc.Input(id="password", type="password", placeholder='Enter password', minLength=4, style={'width':"100%", 'padding':"10px", 'marginBottom':"5px"})
                                    ],
                                    width=12,
                                    className="mb-3",
                                )
                            ],
                            className="justify-content-center",                        
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label('Confirm Password', ),
                                        dbc.Input(id="confirm_password", type="password", placeholder='Reenter password', style={'width':"100%", 'padding':"10px", 'marginBottom':"5px"})
                                    ],
                                    width=12,
                                    className="mb-3",
                                )
                            ],
                            className="justify-content-center",                        
                        ),
                        html.Br(),
                        dbc.Alert('All fields are required!', id='alert_missing_fields', color='danger', is_open=False),
                        dbc.Alert('Passwords do not match!', id='alert_pw_mismatched', color='danger', is_open=False),

                        dbc.Alert('Success! Your account has been created.', id='alert_acct_created', color='success', is_open=False),
                        dbc.Alert('An account with that Employee ID already exists!', id='alert_acct_exists', color='danger', is_open=False),
                        dbc.Alert('No such ID exists or email does not match the one registered in our database! Contact admin for assistance.', id='alert_id_dnexist', color='danger', is_open=False),
                        dbc.Alert('Username is not available! Choose a different one.', id='alert_username_exists', color='danger', is_open=False),
                        dbc.Alert('Invalid email!', id='alert_invalid_email', color='danger', is_open=False),
                        dbc.Button('Sign Up', id="signup_btn", className="mt-3", disabled=True, color="primary"),
                    ]
                )
            ],
            style={'backgroundColor': '#f4f4f4'},
            className='container mt-5',
        )
    ],
    className='container mt-5',
    style= style
)

@app.callback(
        [
            Output('signup_btn', 'disabled'),
            Output('signup_btn', 'color'),
            Output('alert_pw_mismatched', 'is_open'),
            Output('alert_invalid_email', 'is_open')
        ],
        [
            Input('password', 'value'),
            Input('confirm_password', 'value'),
            Input('username', 'value'),
            Input('firstname', 'value'),
            Input('lastname', 'value'),
            Input('email', 'value'),
            Input('emp_id', 'value'),
            Input('signup_btn', 'n_clicks'),
            Input('url', 'pathname'),
        ]
)

def returnalerts(password, confirm_password, username, firstname, lastname, email, emp_id, n_clicks, pathname):

    if pathname == '/signup':
        if all([password, confirm_password]):
            if password != confirm_password:
                    return [True, "secondary", True, False]
            
        if all([password, confirm_password, username, firstname, lastname, email, emp_id]):
            return [False, "primary", False, False]
        
        if email:
            if not email.endswith("@mail.com"):
                return [False, "primary", False, True]
            else:
                return [False, "primary", False, False]

        else:
            raise PreventUpdate
        
    else:
        raise PreventUpdate

@app.callback(
        [
            Output('alert_acct_exists', 'is_open'),
            Output('alert_username_exists', 'is_open'),
            Output('alert_acct_created', 'is_open'),
            Output('alert_id_dnexist', 'is_open'),
            Output('alert_missing_fields', 'is_open'),
        ],
        [
            Input('password', 'value'),
            Input('confirm_password', 'value'),
            Input('username', 'value'),
            Input('firstname', 'value'),
            Input('lastname', 'value'),
            Input('email', 'value'),
            Input('emp_id', 'value'),
            Input('signup_btn', 'n_clicks'),
            Input('url', 'pathname'),
        ]
)

def validate_password(password, confirm_password, username, firstname, lastname, email, emp_id, n_clicks, pathname):

    ctx = dash.callback_context

    if ctx.triggered: 

        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    
        if eventid == 'signup_btn' and n_clicks:

            if all([password, confirm_password, username, firstname, lastname, email, emp_id]):

                emp_id = emp_id.upper()
                username = username.lower()
                firstname = firstname.capitalize()
                lastname = lastname.capitalize()

                # # validates employee id with the company's employee database to authenticate identity
                # emp_sql = """SELECT emp_id, email FROM employees
                #         WHERE   emp_id = %s AND
                #                 email = %s AND
                #                 is_active = 1
                #         """

                # emp_df = db.querydatafromdatabase(emp_sql, [emp_id, email], ['emp_id', 'email'])

                reg_sql = """SELECT emp_id, username FROM registeredusers       
                        """
                
                reg_df = db.querydatafromdatabase(reg_sql, [], ['emp_id', 'username'])
                reg_emp = reg_df[reg_df['emp_id'] == emp_id]
                reg_username = reg_df[reg_df['username'] == username]

                if not reg_emp.empty: # alert_account_exists
                    return [True, False, False, False, False]
                elif reg_emp.empty and not reg_username.empty: # alert_username_exists
                    return [False, True, False, False, False]

                else: #alert_account_created
                    # if not emp_df.empty: 
                    insert_sql = """INSERT into registeredusers(emp_id, username, userpassword, firstname, lastname, email, created_timestamp, is_active)
                                VALUES (%s, %s, %s, %s, %s, %s, NOW(), 1)
                            """

                    insert_df = db.modifydatabase(insert_sql, [emp_id, username, password, firstname, lastname, email])

                    return [False, False, True, False, False]
                        
                    # else: #alert_id_dnexist
                    #     return [False, False, False, True, False]
                
            else:
                return [False, False, False, False, True]
            
        else:
            raise PreventUpdate
    
    else:
        raise PreventUpdate

