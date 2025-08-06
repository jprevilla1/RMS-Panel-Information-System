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
        html.Div(
            [
                dcc.Store(id='editmode', storage_type='memory', data=0),
            ]
        ),
        navbar_modifymodule,
        html.Hr(),
        html.H4('Module: Modify Existing Shop'),
        html.Hr(),
        dbc.Form(
            [   
                html.H5('Shop Profile'),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Label('Assigned Outlet ID', width=2),
                        dbc.Col(
                            dbc.Input(type='number',id='update_outlet_id',placeholder='Outlet ID', disabled=True),
                            width=2
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label('Address Coordinates', width=2),
                        dbc.Col([
                            dbc.Input(type='number',id='update_outlet_long',placeholder='Longitude', min=103.6000, max=104.0500),
                            dbc.Tooltip("between 103.6000 and 104.0500, round to 4 decimal places", target='update_outlet_long', placement='bottom')
                            ], 
                            width=2),
                        dbc.Col([
                            dbc.Input(type='number',id='update_outlet_lat',placeholder='Latitude', min=1.2200, max=1.4700),
                            dbc.Tooltip("between 1.2200 and 1.4700, round to 4 decimal places", target='update_outlet_lat', placement='bottom')
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
                                id='update_outlet_size',
                                options=["XSMALL", "SMALL", "MEDIUM", "LARGE", "XLARGE"],
                                placeholder='Select size'
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
                                id='update_outlet_retailer',
                                placeholder='Select retailer',
                                options=['TANGS', 'BHG', 'COURTS', 'HARVEY NORMAN', 'GAIN CITY', 'BEST DENKI', 'MUSTAFA', 'PARISILK ELECTRONICS', 'AUDIO HOUSE', 'MEGA DISCOUNT', 'MAYER MARKETING']
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
                                id='update_outlet_channel',
                                placeholder='Select channel',
                                options=['Department Stores', 'Electrical Specialists', 'Technical Superstores']
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
                                id='update_outlet_region',
                                options=['CENTRAL REG SG', 'EAST REGION SG', 'NORTH EAST SG', 'NORTH REG SG', 'WEST REG SG'],
                                placeholder='Select region'
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
                                id='update_outlet_copies',
                                options=['REGULAR', 'MODELED', 'COPY_AND_CREATE'],
                                placeholder='Select copies'
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
                                id='update_outlet_auditdate',
                                placeholder='Audit Date',
                                month_format='MMM Do, YY',
                            ),
                            width=2
                        )
                    ],
                    className='mb-3'
                ),
                html.Hr(),
                dbc.Alert('All fields are required!', id='alert_missing', color='danger', is_open=False),

            ],),
        dbc.Alert('All fields are required!', id='alert_update_missing', color='danger', is_open=False),
        dbc.Button('Update', id='update_btn', n_clicks=0),

        dbc.Modal( # modal = dialog box; feedback for successful saving
            [
                dbc.ModalHeader(
                    html.H4('Update Confirmation')
                ),
                dbc.ModalBody(
                    'Are you sure you want to submit this?'
                ),
                dbc.ModalFooter(
                    [
                    dbc.Button("Proceed", id='confirm_update_btn', color='success', className='me-2'),
                    dbc.Button("Cancel", id='cancel_update_btn', color='secondary'),
                    ]
                ),
            ],
            centered=True,
            id='confirm_update_modal',
            is_open=False,
            backdrop='static' # dialog box does not go away if you click at the background
        ),
        dbc.Modal( # modal = dialog box; feedback for successful saving
                [
                dbc.ModalHeader(
                    html.H4('Update Success')
                ),
                dbc.ModalBody(
                    'Outlet information has been successfully updated!'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        'OK',
                        id='update_success_btn',
                        href='/modifymodule' # clicking this would lead to a change of pages
                    )
                )
                ],
                centered=True,
                id='update_success_modal',
                is_open=False,
                backdrop='static' # dialog box does not go away if you click at the background
        ),
    ]
)

@app.callback(
    [
        Output('update_outlet_id', 'value'),
        Output('update_outlet_long', 'value'),
        Output('update_outlet_lat', 'value'),
        Output('update_outlet_size', 'value'),
        Output('update_outlet_retailer', 'value'),
        Output('update_outlet_channel', 'value'),
        Output('update_outlet_region', 'value'),
        Output('update_outlet_copies', 'value'),
        Output('update_outlet_auditdate', 'date'),

        Output('editmode', 'data'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search') # add this search component to the State
    ]
)


def update_populateform(pathname, search_mode):
    if pathname == '/submitupdate':
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

        # are we on edit or delete mode?
        selected_mode = parse_qs(parsed.query)['mode'][0]
        toload = 1 if selected_mode == 'edit' else 0 # 0 if on delete mode

    else:
        raise PreventUpdate

    return [outletid, ad_longitude, ad_latitude, shopsize, retailer, channel, region, copies, audit_date, toload]


# confirms submission with user
@app.callback(
    [
        Output('confirm_update_modal', 'is_open'),
        Output('update_success_modal', 'is_open'),
        Output('alert_update_missing', 'is_open'),
    ],
    [
        Input('update_btn', 'n_clicks'),
        Input('confirm_update_btn', 'n_clicks'),
        Input('cancel_update_btn', 'n_clicks'),         
    ],
    [
        State('update_outlet_id', 'value'),
        State('update_outlet_long', 'value'),
        State('update_outlet_lat', 'value'),
        State('update_outlet_size', 'value'),
        State('update_outlet_retailer', 'value'),
        State('update_outlet_channel', 'value'),
        State('update_outlet_region', 'value'),
        State('update_outlet_copies', 'value'),
        State('update_outlet_auditdate', 'date'),
    ]
)

def updatedatabase(update_clicks, confirm_update_clicks, cancel_update_clicks, outletid, long, lat, size, retailer, channel, region, copies, auditdate):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'update_btn' and update_clicks:
            if not all([outletid, long, lat, size, retailer, channel, region, copies, auditdate]):
                return [False, False, True]
            
            else:
                return [True, False, False]
            
        elif eventid in ['confirm_update_btn']:
            sql = """UPDATE shops
                    SET
                        ad_longitude = %s,
                        ad_latitude = %s,
                        shopsize = %s,
                        retailer = %s,
                        channel = %s, 
                        region = %s, 
                        copies = %s,
                        audit_date = %s
                    WHERE
                        outletid = %s
                    """
            values = [long, lat, size, retailer, channel, region, copies, auditdate, outletid]

            db.modifydatabase(sql, values)

            return [False, True, False]
        elif eventid in ['cancel_update_btn']:
            return [False, False, False]
        
        else:
            raise PreventUpdate
            
    else:
        raise PreventUpdate
