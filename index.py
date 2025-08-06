import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import webbrowser

from app import app
from apps import commonmodules as cm
from apps import login, signup, home, dbmanager, addmodule, modifymodule, submitupdate, deletemodule, efactorview, storemapper, dashboard

CONTENT_STYLE = {
    "margin-top" : "1em",
    "margin-left" : "1em",
    "margin-right" : "1em",
    "padding" : "1em 1em",
}

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)

@app.callback(
    [
        Output('page-content','children')
    ],           
    [
        Input('url', 'pathname'),
    ]
)

def displaypage(pathname):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'url':
            if pathname == '/':
                returnlayout = login.layout
            elif pathname == '/signup':
                returnlayout = signup.layout
            elif pathname == '/home':
                returnlayout = home.layout
            elif pathname == '/dbmanager':
                returnlayout = dbmanager.layout
            elif pathname == '/addmodule':
                returnlayout = addmodule.layout
            elif pathname == '/modifymodule':
                returnlayout = modifymodule.layout
            elif pathname == '/login':
                returnlayout = login.layout
            elif pathname == '/submitupdate':
                returnlayout = submitupdate.layout
            elif pathname == '/deletemodule':
                returnlayout = deletemodule.layout
            elif pathname == '/efactorview':
                returnlayout = efactorview.layout
            elif pathname == '/storemapper':
                returnlayout = storemapper.layout
            elif pathname == '/dashboard':
                returnlayout = dashboard.layout
            else:
                returnlayout = 'error404'

            return [returnlayout]
        
        else:
            raise PreventUpdate
        
    else:
        raise PreventUpdate

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run(debug=True)



