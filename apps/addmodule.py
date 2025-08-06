from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app
import dbconnect as db
from apps.commonmodules import navbar_dbmanager

from urllib.parse import urlparse, parse_qs

layout = html.Div(
                [
                dcc.Store(id='delete_item_record'),
                navbar_dbmanager,
                html.Br(),
                html.H4('Module: Add New Shop'),
                html.Hr(),
                dbc.Form(
                    [   
                        html.H5('Shop Profile'),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Label('Assigned Outlet ID', width=2),
                                dbc.Col(
                                    dbc.Input(type='number',id='add_outlet_id',placeholder='Outlet ID'),
                                    width=2
                                )
                            ],
                            className='mb-3'
                        ),
                        dbc.Row(
                            [
                                dbc.Label('Address Coordinates', width=2),
                                dbc.Col([
                                    dbc.Input(type='number',id='add_outlet_long',placeholder='Longitude', min=103.6000, max=104.0500),
                                    dbc.Tooltip("between 103.6000 and 104.0500, round to 4 decimal places", target='add_outlet_long', placement='bottom')
                                    ], 
                                    width=2),
                                dbc.Col([
                                    dbc.Input(type='number',id='add_outlet_lat',placeholder='Latitude', min=1.2200, max=1.4700),
                                    dbc.Tooltip("between 1.2200 and 1.4700, round to 4 decimal places", target='add_outlet_lat', placement='bottom')
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
                                        id='add_outlet_size',
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
                                        id='add_outlet_retailer',
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
                                        id='add_outlet_channel',
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
                                        id='add_outlet_region',
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
                                        id='add_outlet_copies',
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
                                        id='add_outlet_auditdate',
                                        placeholder='Audit Date',
                                        month_format='MMM Do, YY',
                                    ),
                                    width=2
                                )
                            ],
                            className='mb-3'
                        ),
                        dbc.Alert('Outlet ID cannot be empty! Supply Outlet ID first to insert items.', id='alert_missing_outlet', color='danger', is_open=False),
                        dbc.Alert(id='alert_created', color='success', is_open=False),
                        dbc.Alert('All fields are required!', id='alert_missing', color='danger', is_open=False),
                        dbc.Alert(id='alert_existing', color='danger', is_open=False),
                        dbc.Button('Create', id='submit_btn', color='primary'),
                        html.Br(),


                        html.Hr(),
                        html.H5('Products Carried'),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Label('Select items being carried', width=2),
                                dbc.Col([dcc.Dropdown(id='insert_item', placeholder='Select from item list', style={'width': '200px'}),], width=2),
                                dbc.Col([dbc.Button('Insert', id='insertitem_btn', color='primary'),], width=2),
                            ], 
                            # className='g-0 align-items-center',
                            ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Label('Enter Sales (based on Store Audit)', width=2),
                                dbc.Col([dbc.Input(type='number',id='enter_units',placeholder='Enter sales, default is 0', min=0)], width=2),
                                dbc.Col([dbc.Input(type='number',id='enter_price',placeholder='Enter price, default is 0', min=0)], width=2),
                            ], className='g-0 align-items-center',
                            ),

  
                        
                        dbc.Alert('Item already exists in the table!', id='alert_existing_item', color='danger', is_open=False),
                        dbc.Alert('Item successfully inserted!', id='alert_insert_success', color='success', is_open=False),
                        dbc.Alert('Cannot be empty: Select item from dropdown to insert!', id='alert_missing_item', color='danger', is_open=False),

                        html.Div(
                        "Search results...",
                        id='items_table'),

                        html.Hr(),
                        
                        html.Br(),

                        dbc.Modal([
                            dbc.ModalHeader("Confirm Submission"),
                            dbc.ModalBody('Are you sure you want to submit this?'),
                            dbc.ModalFooter([
                                dbc.Button("Yes", id='confirm_submit', color='success', className='me-2'),
                                dbc.Button("Cancel", id='cancel_submit', color='secondary'),
                            ])
                        ],
                        id='confirm_modal',
                        is_open=False
                        ),

                        # pop up form for sales and price input
                        # dbc.Modal([
                        #     dbc.ModalHeader(dbc.ModalTitle("Edit sales based on store audit")),
                        #     dbc.ModalBody([
                        #         dbc.Label("Sales"),
                        #         dbc.Input(id="form_enter_sales", type="number", placeholder="Enter units sold"),

                        #         dbc.Label("Price", className="mt-2"),
                        #         dbc.Input(id="form_enter_price", type="number", placeholder="Enter price"),
                        #     ]),
                        #     dbc.ModalFooter([
                        #         dbc.Button("Submit", id="sales_form_submit_btn", color="primary", className="me-2"),
                        #         dbc.Button("Cancel", id="sales_form_cancel_btn", color="secondary")
                        #     ])
                        # ],
                        # id="sales_form_modal",
                        # is_open=False
                        # ),

                    ]
            )])

# confirms submission with user
@app.callback(
    [
        Output('confirm_modal', 'is_open'),
        Output('alert_missing', 'is_open'),
        Output('alert_existing', 'children'),
        Output('alert_existing', 'is_open'),
    ],
    [
        Input('submit_btn', 'n_clicks'),
        Input('cancel_submit', 'n_clicks'),
        Input('confirm_submit', 'n_clicks'),
        Input('confirm_modal', 'is_open'),
    ],
    [
        State('add_outlet_id', 'value'),
        State('add_outlet_long', 'value'),
        State('add_outlet_lat', 'value'),
        State('add_outlet_size', 'value'),
        State('add_outlet_retailer', 'value'),
        State('add_outlet_channel', 'value'),
        State('add_outlet_region', 'value'),
        State('add_outlet_copies', 'value'),
        State('add_outlet_auditdate', 'date'),
    ]
)

def confirmprompt(n_clicks, cancel_click, confirm_click, is_open, outlet_id, long, lat, size, retailer, channel, region, copies, auditdate):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'submit_btn':
            if not all([outlet_id, long, lat, size, retailer, channel, region, copies, auditdate]):
                return [False, True, '', False]
            else:
                sql = """SELECT outletid FROM shops
                        WHERE  
                            outletid = %s 
                        """
                df = db.querydatafromdatabase(sql, [outlet_id], ['outletid'])
                if df.shape[0] > 0:
                    return [False, False, f'Shop with ID {outlet_id} already exists!', True]
                else:
                    return [True, False, '', False]
        elif eventid in ['cancel_submit', 'confirm_submit']:
            return [False, False, '', False]
        else: 
            raise PreventUpdate
    else: 
        raise PreventUpdate

# returns error or submits record into database
@app.callback(
    [
        Output('alert_created', 'children'),
        Output('alert_created', 'is_open'),

        # # clears the form upon submit button
        # Output('add_outlet_id', 'value'),
        # Output('add_outlet_long', 'value'),
        # Output('add_outlet_lat', 'value'),
        # Output('add_outlet_size', 'value'),
        # Output('add_outlet_retailer', 'value'),
        # Output('add_outlet_channel', 'value'),
        # Output('add_outlet_region', 'value'),
        # Output('add_outlet_copies', 'value'),
        # Output('add_outlet_auditdate', 'date'),
    ],
    [
        Input('confirm_submit', 'n_clicks'),
    ],
    [
        State('add_outlet_id', 'value'),
        State('add_outlet_long', 'value'),
        State('add_outlet_lat', 'value'),
        State('add_outlet_size', 'value'),
        State('add_outlet_retailer', 'value'),
        State('add_outlet_channel', 'value'),
        State('add_outlet_region', 'value'),
        State('add_outlet_copies', 'value'),
        State('add_outlet_auditdate', 'date'),
    ]
)

def submitrecord(n_clicks, outlet_id, long, lat, size, retailer, channel, region, copies, auditdate):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'confirm_submit':
            is_active = 1
            ext_factor = 1
            sql = """
                    INSERT INTO shops (outletid, ad_longitude, ad_latitude, shopsize, retailer, channel, region, copies, audit_date, is_active, ext_factor)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            df = db.modifydatabase(sql, [outlet_id, long, lat, size, retailer, channel, region, copies, auditdate, is_active, ext_factor])
            return [f'New record for shop with ID {outlet_id} created!', True]
        else:
            url = dash.noupdate
            return ['', False]

    else: 
        raise PreventUpdate 


# returns elements in 'products carried' section and deletes item record when triggered
@app.callback(
    [
        Output('items_table', 'children'),
        Output('insert_item', 'options'),
        Output('alert_missing_outlet', 'is_open'),
        Output('alert_existing_item', 'is_open'),
        Output('alert_missing_item', 'is_open'),
        Output('alert_insert_success', 'is_open'),
    ],
    [
        Input('insertitem_btn', 'n_clicks'),
        Input('url', 'pathname'),
        Input({"type": "delete_item_record", "index": dash.ALL}, "n_clicks"),
    ],
    [
        State('add_outlet_id', 'value'),
        State('insert_item', 'value'),
        State('enter_units', 'value'),
        State('enter_price', 'value'),
    ]
)


def returnitems(n_clicks, pathname, delete_clicks, outletid, itemname, units, price ):
    if pathname == '/addmodule':
        sql = """SELECT brand, itemname, itemid FROM items
            """
        df = db.querydatafromdatabase(sql, [], ['brand', 'itemname', 'itemid'])
        # itemslist = (df['brand'] + ' ' + df['itemname']).tolist()
        itemslist =df['itemname'].tolist()

        ctx = dash.callback_context

        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

            if eventid == 'insertitem_btn' and n_clicks:
                            
                if all([outletid, itemname]):

                    selected_itemid = int(df[df['itemname'] == itemname]['itemid'].iloc[0]) # get itemid from itemname

                    retrieve_outlet_sql = """SELECT s.itemid, i.itemname, i.brand, i.productgroup, s.units, s.price 
                            FROM sales s
                            LEFT JOIN items i ON s.itemid = i.itemid
                            WHERE   s.outletid = %s
                        """
                    retrieve_df = db.querydatafromdatabase(retrieve_outlet_sql, [outletid], ['itemid', 'itemname', 'brand', 'productgroup', 'sales', 'price'])
                    retrieve_itemcheck = retrieve_df[retrieve_df['itemid'] == selected_itemid]

                    delete_buttons = []

                    for itemname in retrieve_df['itemname']:

                        delete_buttons += [
                            html.Div(
                                dbc.Button('Delete',
                                            id={"type":"delete_item_record", "index":itemname},
                                            size='sm', color='danger'),
                                            style={'text-align': 'center'}
                            )
                        ]

         
                    retrieve_df['action'] = delete_buttons

                    table = dbc.Table.from_dataframe(retrieve_df, striped=True, bordered=True, hover=True, size='sm')

                    if not retrieve_itemcheck.empty:
                        return [table, itemslist, False, True, False, False]

                    else:
                        insert_sql = """INSERT INTO sales (outletid, itemid, units, price)
                                    VALUES (%s, %s, %s, %s)
                                """
                        if not all([units, price]):
                            units = 0
                            price=0

                        insertdf = db.modifydatabase(insert_sql, [outletid, selected_itemid, units, price])

                        retrieve_df = db.querydatafromdatabase(retrieve_outlet_sql, [outletid], ['itemid', 'itemname', 'brand', 'productgroup', 'sales', 'price'])

                        delete_buttons = []

                        for itemname in retrieve_df['itemname']:

                            delete_buttons += [
                                html.Div(
                                    dbc.Button('Delete',
                                               id={"type":"delete_item_record", "index":itemname},
                                                size='sm', color='danger'),
                                                style={'text-align': 'center'}
                                )
                            ]

                        retrieve_df['action'] = delete_buttons

                        table = dbc.Table.from_dataframe(retrieve_df, striped=True, bordered=True, hover=True, size='sm')

                        return [table, itemslist, False, False, False, False]

                else:
                    if not all([itemname]):
                        return ['', itemslist, False, False, True, False]
                    else:
                        return ['', itemslist, True, False, False, False]
        
        # if ctx.triggered:
        if delete_clicks:
            triggered_index = ctx.triggered_id["index"]

            sql = """DELETE FROM sales
                    WHERE itemid = %s
                """
            
            selected_itemid = int(df[df['itemname'] == triggered_index]['itemid'].iloc[0])

            df = db.modifydatabase(sql, [selected_itemid])

            retrieve_sql= """SELECT s.itemid, i.itemname, i.brand, i.productgroup, s.units, s.price 
                                FROM sales s
                                LEFT JOIN items i ON s.itemid = i.itemid
                                WHERE   s.outletid = %s
                            """
            retrieve_df = db.querydatafromdatabase(retrieve_sql, [outletid], ['itemid', 'itemname', 'brand', 'productgroup', 'sales', 'price'])

            delete_buttons = []

            for itemname in retrieve_df['itemname']:

                delete_buttons += [
                    html.Div(
                        dbc.Button('Delete',
                                    id={"type":"delete_item_record", "index":itemname},
                                    size='sm', color='danger'),
                                    style={'text-align': 'center'}
                    )
                ]

            retrieve_df['action'] = delete_buttons

            table = dbc.Table.from_dataframe(retrieve_df, striped=True, bordered=True, hover=True, size='sm')

            return [table, itemslist, False, False, False, False]

        return ['', itemslist, False, False, False, False]
    
    else:
            raise PreventUpdate

