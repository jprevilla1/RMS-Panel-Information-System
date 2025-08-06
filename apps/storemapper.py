
import plotly.express as px
import pandas as pd

from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

from app import app
import dbconnect as db
from apps.commonmodules import navbar_home

layout = html.Div(
                [
                navbar_home,
                html.Br(),
                html.H4('Store Mapper'),
                html.Hr(),
                dbc.Form(
                    [   
                        dbc.Row(
                            [
                                dbc.Label('Search Store :', width=1),
                                dbc.Col(
                                    dbc.Input(type='number',id='view_outlet_id',placeholder='Outlet ID'),
                                    width=2
                                ),
                            ],
                            className='mb-3'
                        ),                  
                        dbc.Row(
                            [
                                dbc.Label('Shopsize :', width=1),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='view_outlet_size',
                                        options=["XSMALL", "SMALL", "MEDIUM", "LARGE", "XLARGE"],
                                        placeholder='(All)'
                                    ),
                                    width=2
                                ),
                                dbc.Label('Retailer :', width=1, className='ms-auto text-end'),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='view_outlet_retailer',
                                        placeholder='(All)',
                                        options=['TANGS', 'BHG', 'COURTS', 'HARVEY NORMAN', 'GAIN CITY', 'BEST DENKI', 'MUSTAFA', 'PARISILK ELECTRONICS', 'AUDIO HOUSE', 'MEGA DISCOUNT', 'MAYER MARKETING']
                                    ),
                                    width=2
                                ),
                                dbc.Label('Region :', width=1, className='ms-auto text-end'),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='view_outlet_region',
                                        options=['CENTRAL REG SG', 'EAST REGION SG', 'NORTH EAST SG', 'NORTH REG SG', 'WEST REG SG'],
                                        placeholder='(All)'
                                    ),
                                    width=2
                                ),
                                dbc.Label('Copies :', width=1, className='ms-auto text-end'),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='view_outlet_copies',
                                        options=['REGULAR', 'MODELED', 'COPY_AND_CREATE'],
                                        placeholder='(All)'
                                    ),
                                    width=2
                                ),
                            ],
                            className='mb-3' 
                        ),

                        dbc.Row(
                            [
                                dbc.Label('Channel :', width=1),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='view_outlet_channel',
                                        options=['Department Stores', 'Electrical Specialists', 'Technical Superstores'],
                                        placeholder='(All)'
                                    ),
                                    width=2
                                ),
                                dbc.Label('Org Type :', width=1, className='ms-auto text-end'),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='view_outlet_orgtype',
                                        options=['CHAINS', 'INDEPENDENTS'],
                                        placeholder='(All)'
                                    ),
                                    width=2
                                ),
                                dbc.Label('Status :', width=1, className='ms-auto text-end'),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='view_outlet_status',
                                        options=['Active', 'Closed'],
                                        placeholder='(All)'
                                    ),
                                    width=2
                                ),
                                dbc.Label('Audit Date :', width=1, className='ms-auto text-end'),
                                dbc.Col(
                                    dcc.DatePickerSingle(
                                        id='view_outlet_auditdate',
                                        placeholder='Audit Date',
                                        month_format='MMM Do, YY',
                                    ),
                                    width=2
                                )
                            ],
                            className='mb-3' 
                        ),
                        html.Hr(),
                    ]
            ),
                dcc.Graph(id='display_map_result') 
])

@app.callback(
    [
        Output('display_map_result', 'figure')
    ],
    [
        Input('url', 'pathname'),
        Input('view_outlet_id', 'value'),
        Input('view_outlet_size', 'value'),
        Input('view_outlet_retailer', 'value'),
        Input('view_outlet_channel', 'value'),
        Input('view_outlet_orgtype', 'value'),
        Input('view_outlet_region', 'value'),
        Input('view_outlet_copies', 'value'),
        Input('view_outlet_auditdate', 'date'),
        Input('view_outlet_status', 'value'),
    ]
)

def filtermapview(pathname, outletid, size, retailer, channel, orgtype, region, copies, auditdate, is_active):
    if pathname == '/storemapper':
        sql = """ SELECT s.outletid, s.ad_longitude, s.ad_latitude, s.shopsize, s.retailer, s.channel, r.orgtype, s.region, s.copies, s.audit_date, s.is_active
                    FROM shops s
                    LEFT JOIN retailers r ON s.retailer = r.retailer
                """
        values = []

        cols = ['outletid', 'ad_longitude', 'ad_latitude', 'shopsize', 'retailer', 'channel', 'orgtype', 'region', 'copies', 'audit_date', 'is_active']

        df = db.querydatafromdatabase(sql, values, cols)

        cols_filter = ['outletid', 'shopsize', 'retailer', 'channel', 'orgtype', 'region', 'copies', 'audit_date', 'is_active']
        vals_filter = [outletid, size, retailer, channel, orgtype, region, copies, auditdate, is_active]

        dict_vals = dict(zip(cols_filter, vals_filter))
        
        for col, val in dict_vals.items():
            if val:
                if col == 'is_active':
                    val = 1 if is_active == 'Active' else 0
                    df = df[df[col] == val]
                else:
                    df = df[df[col] == val]

        filtered_df = df[['outletid', 'ad_latitude', 'ad_longitude']]
        # print(filtered_df)

        fig = px.scatter_mapbox(filtered_df, lat="ad_latitude", lon="ad_longitude", hover_name="outletid", zoom=10, height=500)
        fig.update_layout(mapbox_style="carto-positron") # open-street-map
        
        return [fig]

    else:
        raise PreventUpdate
    


