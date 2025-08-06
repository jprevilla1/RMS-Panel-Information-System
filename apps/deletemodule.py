from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app
import dbconnect as db

from apps.commonmodules import navbar_modifymodule

from urllib.parse import urlparse, parse_qs

layout = html.Div(
    [
        navbar_modifymodule,
        html.Hr(),
        html.H4('Module: Delete Existing Shop'),
        html.Hr(),
        dbc.Form(
            [   
                html.H5('Shop Profile (Read-Only)'),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Label('Assigned Outlet ID', width=2),
                        dbc.Col(
                            dbc.Input(type='number',id='delete_outlet_id',placeholder='Outlet ID', disabled=True),
                            width=2
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label('Address Coordinates', width=2),
                        dbc.Col([
                            dbc.Input(type='number',id='delete_outlet_long',placeholder='Longitude', min=103.6000, max=104.0500, disabled=True),
                            dbc.Tooltip("between 103.6000 and 104.0500, round to 4 decimal places", target='delete_outlet_long', placement='bottom')
                            ], 
                            width=2),
                        dbc.Col([
                            dbc.Input(type='number',id='delete_outlet_lat',placeholder='Latitude', min=1.2200, max=1.4700, disabled=True),
                            dbc.Tooltip("between 1.2200 and 1.4700, round to 4 decimal places", target='delete_outlet_lat', placement='bottom')
                            ], 
                            width=2),
                    ],
                    className='mb-3' 
                ),                    
                dbc.Row(
                    [
                        dbc.Label('Shopsize', width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id='delete_outlet_size',
                                options=["XSMALL", "SMALL", "MEDIUM", "LARGE", "XLARGE"],
                                placeholder='Select size',
                                disabled=True
                            ),
                            width=2
                        )
                    ],
                    className='mb-3' 
                ),
                dbc.Row(
                    [
                        dbc.Label('Retailer', width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id='delete_outlet_retailer',
                                placeholder='Select retailer',
                                options=['TANGS', 'BHG', 'COURTS', 'HARVEY NORMAN', 'GAIN CITY', 'BEST DENKI', 'MUSTAFA', 'PARISILK ELECTRONICS', 'AUDIO HOUSE', 'MEGA DISCOUNT', 'MAYER MARKETING'],
                                disabled=True
                            ),
                            width=2
                        )
                    ],
                    className='mb-3' 
                ),
                dbc.Row(
                    [
                        dbc.Label('Channel', width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id='delete_outlet_channel',
                                placeholder='Select channel',
                                options=['Department Stores', 'Electrical Specialists', 'Technical Superstores'],
                                disabled=True
                            ),
                            width=2
                        )
                    ],
                    className='mb-3' 
                ),
                dbc.Row(
                    [
                        dbc.Label('Region', width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id='delete_outlet_region',
                                options=['CENTRAL REG SG', 'EAST REGION SG', 'NORTH EAST SG', 'NORTH REG SG', 'WEST REG SG'],
                                placeholder='Select region',
                                disabled=True
                            ),
                            width=2
                        )
                    ],
                    className='mb-3' 
                ),
                dbc.Row(
                    [
                        dbc.Label('Copies', width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id='delete_outlet_copies',
                                options=['REGULAR', 'MODELED', 'COPY_AND_CREATE'],
                                placeholder='Select copies',
                                disabled=True
                            ),
                            width=2
                        )
                    ],
                    className='mb-3' 
                ),
                dbc.Row(
                    [
                        dbc.Label('Audit Date', width=2),
                        dbc.Col(
                            dcc.DatePickerSingle(
                                id='delete_outlet_auditdate',
                                placeholder='Audit Date',
                                month_format='MMM Do, YY',
                                disabled=True
                            ),
                            width=2
                        )
                    ],
                    className='mb-3'
                ),
                # html.H5('Products Carried'),
                html.Hr(),
            ],),

        dbc.Button('Delete', id='delete_btn', color='danger', n_clicks=0),

        dbc.Modal( # modal = dialog box; feedback for successful saving
            [
                dbc.ModalHeader(
                    html.H4('Delete Confirmation')
                ),
                dbc.ModalBody(
                    'Are you sure you want to submit this?'
                ),
                dbc.ModalFooter(
                    [
                    dbc.Button("Proceed", id='confirm_delete_btn', color='success', className='me-2'),
                    dbc.Button("Cancel", id='cancel_delete_btn', color='secondary'),
                    ]
                ),
            ],
            centered=True,
            id='confirm_delete_modal',
            is_open=False,
            backdrop='static' # dialog box does not go away if you click at the background
        ),
        dbc.Modal( # modal = dialog box; feedback for successful saving
                [
                dbc.ModalHeader(
                    html.H4('Delete Success')
                ),
                dbc.ModalBody(
                    'Outlet information has been successfully deleted!'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        'OK',
                        id='delete_success_btn',
                        href='/modifymodule' # clicking this would lead to a change of pages
                    )
                )
                ],
                centered=True,
                id='delete_success_modal',
                is_open=False,
                backdrop='static' # dialog box does not go away if you click at the background
        ),
    ]
)

@app.callback(
    [
        Output('delete_outlet_id', 'value'),
        Output('delete_outlet_long', 'value'),
        Output('delete_outlet_lat', 'value'),
        Output('delete_outlet_size', 'value'),
        Output('delete_outlet_retailer', 'value'),
        Output('delete_outlet_channel', 'value'),
        Output('delete_outlet_region', 'value'),
        Output('delete_outlet_copies', 'value'),
        Output('delete_outlet_auditdate', 'date'),

    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search') # add this search component to the State
    ]
)


def delete_populateform(pathname, search_mode):
    if pathname == '/deletemodule':
        # extract outlet id
        parsed = urlparse(search_mode)
        selected_outlet = parse_qs(parsed.query)['id'][0]

        sql = """
        SELECT outletid, ad_longitude, ad_latitude, shopsize, retailer, channel, region, copies, audit_date
        FROM shops
        WHERE is_active = 1 AND
            outletid = %s
        """
        values = [selected_outlet]
        cols = ['outletid', 'ad_longitude', 'ad_latitude', 'shopsize', 'retailer', 'channel', 'region', 'copies', 'audit_date']
        df = db.querydatafromdatabase(sql, values, cols)

        outletid, ad_longitude, ad_latitude, shopsize, retailer, channel, region, copies, audit_date = df.iloc[0]

    else:
        raise PreventUpdate

    return [outletid, ad_longitude, ad_latitude, shopsize, retailer, channel, region, copies, audit_date]


# confirms submission with user
@app.callback(
    [
        Output('confirm_delete_modal', 'is_open'),
        Output('delete_success_modal', 'is_open'),
    ],
    [
        Input('delete_btn', 'n_clicks'),
        Input('confirm_delete_btn', 'n_clicks'),
        Input('cancel_delete_btn', 'n_clicks'),        
    ],
    [
        State('delete_outlet_id', 'value'),
        State('delete_outlet_long', 'value'),
        State('delete_outlet_lat', 'value'),
        State('delete_outlet_size', 'value'),
        State('delete_outlet_retailer', 'value'),
        State('delete_outlet_channel', 'value'),
        State('delete_outlet_region', 'value'),
        State('delete_outlet_copies', 'value'),
        State('delete_outlet_auditdate', 'date'),
    ]
)

def deletedatabase(delete_clicks, confirm_delete_clicks, cancel_delete_clicks, outletid, long, lat, size, retailer, channel, region, copies, auditdate):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'delete_btn' and delete_clicks:
            return [True, False]
        
        elif eventid in ['confirm_delete_btn']:
            sql = """UPDATE shops
                    SET
                        is_active = %s
                    WHERE
                        outletid = %s
                    """
            values = [0, outletid]

            db.modifydatabase(sql, values)

            return [False, True]
        
        elif eventid in ['cancel_delete_btn']:
            return [False, False]

        else:
            raise PreventUpdate
            
    else:
        raise PreventUpdate
