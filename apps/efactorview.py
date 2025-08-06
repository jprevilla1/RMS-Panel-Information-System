from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app
from apps.commonmodules import navbar_home
from apps.efactorcalc import update_extcell

import dbconnect as db

layout = html.Div(
    [
        navbar_home,
        html.Br(),
        html.H2('View Extrapolation Factors'), #page header
        html.Hr(),
        dbc.Card(
            [
                html.Div( # create section to show list of movies
                [
                    html.Br(),
                    html.Div(
                        dbc.Form(
                            dbc.Row(
                                [
                                    dbc.Label("Search Outlet", width=2),
                                    dbc.Col(
                                        dbc.Input(
                                            type='number',
                                            id='search_outlet_ef',
                                            placeholder='Enter ID'
                                        ),
                                        width=3
                                    ),
                                    dbc.Col(
                                        [html.Button("Download as CSV", id='download_btn'),
                                        dcc.Download(id='download_df_csv')],
                                        width=3
                                    )
                                ],
                                className='mb-3' 
                            )
                        )
                    ),
                    html.Div(
                        "Search results...",
                        id='ef_result_table'
                    )
                ]
                )
            ]
        )
    ]
)

@app.callback(
    [
        Output('ef_result_table', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('search_outlet_ef', 'value'),
    ]
)

def returnsearch(pathname, search_outlet):
    if pathname == '/efactorview':

        # run extrapolationcell table update
        update_extcell()
 
        sql = """ SELECT s.outletid, s.retailer, e.shopsize, e.channel, e.region, e.orgtype, e.ext_factor
                    FROM shops s
                    LEFT JOIN retailers r ON s.retailer = r.retailer
                    LEFT JOIN extrapolationcell e ON
                        s.shopsize = e.shopsize AND
                        r.orgtype = e.orgtype AND
                        s.channel = e.channel AND
                        s.region = e.region
                WHERE 
                    s.is_active = 1
                """
        values = [] 

        cols = ['outletid', 'retailer', 'shopsize', 'channel', 'region', 'orgtype', 'extrapolation_factor']

        if search_outlet:
            # we use the operator ILIKE for pattern-matching
            sql += " AND CAST(outletid as TEXT) LIKE %s"

            # the % before and after the term means that there can be text before and after the search term
            values += [f"%{search_outlet}%"]

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape: 
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')

            
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('download_df_csv', 'data')
    ],
    [
        Input('search_outlet_ef', 'value'),
        Input('download_btn', 'n_clicks') 
    ]
)

def downloadcsv(search_outlet, n_clicks):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'download_btn':

            # run extrapolationcell table update
            update_extcell()
    
            sql = """ SELECT s.outletid, s.retailer, e.shopsize, e.channel, e.region, e.orgtype, e.ext_factor
                        FROM shops s
                        LEFT JOIN retailers r ON s.retailer = r.retailer
                        LEFT JOIN extrapolationcell e ON
                            s.shopsize = e.shopsize AND
                            r.orgtype = e.orgtype AND
                            s.channel = e.channel AND
                            s.region = e.region
                    WHERE 
                        s.is_active = 1
                    """
            values = [] 

            cols = ['outletid', 'retailer', 'shopsize', 'channel', 'region', 'orgtype', 'extrapolation_factor']

            if search_outlet:
                # we use the operator ILIKE for pattern-matching
                sql += " AND CAST(outletid as TEXT) LIKE %s"

                # the % before and after the term means that there can be text before and after the search term
                values += [f"%{search_outlet}%"]

            df = db.querydatafromdatabase(sql, values, cols)

            if df.shape: 
                download_table = dcc.send_data_frame(df.to_csv, "efactor-table.csv", index=False)
                return [download_table]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate