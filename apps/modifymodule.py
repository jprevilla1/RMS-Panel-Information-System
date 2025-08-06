from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app
from apps.commonmodules import navbar_dbmanager

import dbconnect as db

layout = html.Div(
    [
        navbar_dbmanager,
        html.Br(),
        html.H4('Module: Modify/Delete Existing Shop'), #page header
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
                                            id='search_outletid',
                                            placeholder='Enter ID'
                                        ),
                                        width=3
                                    )
                                ],
                                className='mb-3' # add 1em bottom margin
                            )
                        )
                    ),
                    html.Div(
                        "Search results...",
                        id='search_result_table'
                    )
                ]
                )
            ]
        )
    ]
)

@app.callback(
    [
        Output('search_result_table', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('search_outletid', 'value') # changing the textbox value should update the table
    ]
)

def displaysearchresult(pathname, search_outlet):
    if pathname == '/modifymodule':
        # 1. Obtain records from the DB via SQL
        sql = """ SELECT s.outletid, s.ad_longitude, s.ad_latitude, s.shopsize, s.retailer, s.channel, s.region, r.orgtype, s.copies, s.audit_date
                    FROM shops s
                    LEFT JOIN retailers r ON s.retailer = r.retailer
                WHERE 
                    s.is_active = 1
                """
        values = [] # blank since I do not have placeholders in my SQL

        cols = ['outletid', 'ad_longitude', 'ad_latitude', 'shopsize', 'retailer', 'channel', 'region', 'orgtype', 'copies', 'audit_date']

        if search_outlet:
            # we use the operator ILIKE for pattern-matching
            sql += " AND CAST(s.outletid as TEXT) LIKE %s"

            # the % before and after the term means that there can be text before and after the search term
            values += [f"%{search_outlet}%"]

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape: 
            
            edit_buttons = []
            delete_buttons = []
            for outletid in df['outletid']:
                # print(outletid)
                edit_buttons += [
                    html.Div(
                        dbc.Button('Edit',
                                    href=f'submitupdate?mode=edit&id={outletid}',
                                    size='sm', color='warning'),
                                    style={'text-align': 'center'}
                    )
                ]

                delete_buttons += [
                    html.Div(
                        dbc.Button('Delete',
                                    href=f'deletemodule?&id={outletid}',
                                    size='sm', color='danger'),
                                    style={'text-align': 'center'}
                    )
                ]

            df['edit_action'] = edit_buttons
            df['delete_action'] = delete_buttons

            # remove the column ID before turning into a table
            df = df[['edit_action', 'delete_action', 'outletid', 'ad_longitude', 'ad_latitude', 'shopsize', 'retailer', 'channel', 'region', 'orgtype', 'copies', 'audit_date']]

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate
    