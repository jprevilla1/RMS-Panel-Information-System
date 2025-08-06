from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

from app import app
import dbconnect as db
from apps.commonmodules import navbar_home

import plotly.express as px

layout = html.Div(
                [
                navbar_home,
                html.Br(),
                html.H4('Panel Health Dashboard'),
                html.Hr(),
                dbc.Form(
                    [   
                        dbc.Row(
                            [
                                dbc.Label('Search Store', width=1),
                                dbc.Col(
                                    dbc.Input(type='number',id='db_outlet_id',placeholder='Outlet ID'),
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
                                        id='db_outlet_size',
                                        options=["XSMALL", "SMALL", "MEDIUM", "LARGE", "XLARGE"],
                                        placeholder='(All)'
                                    ),
                                    width=2
                                ),
                                dbc.Label('Retailer :', width=1, className='ms-auto text-end'),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='db_outlet_retailer',
                                        placeholder='(All)',
                                        options=['TANGS', 'BHG', 'COURTS', 'HARVEY NORMAN', 'GAIN CITY', 'BEST DENKI', 'MUSTAFA', 'PARISILK ELECTRONICS', 'AUDIO HOUSE', 'MEGA DISCOUNT', 'MAYER MARKETING']
                                    ),
                                    width=2
                                ),
                                dbc.Label('Region :', width=1, className='ms-auto text-end'),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='db_outlet_region',
                                        options=['CENTRAL REG SG', 'EAST REGION SG', 'NORTH EAST SG', 'NORTH REG SG', 'WEST REG SG'],
                                        placeholder='(All)'
                                    ),
                                    width=2
                                ),
                                dbc.Label('Copies :', width=1, className='ms-auto text-end'),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='db_outlet_copies',
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
                                        id='db_outlet_channel',
                                        options=['Department Stores', 'Electrical Specialists', 'Technical Superstores'],
                                        placeholder='(All)'
                                    ),
                                    width=2
                                ),
                                dbc.Label('Org Type :', width=1, className='ms-auto text-end'),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='db_outlet_orgtype',
                                        options=['CHAINS', 'INDEPENDENTS'],
                                        placeholder='(All)'
                                    ),
                                    width=2
                                ),
                                dbc.Label('Audit Date :', id='audit_date_label', width=1, className='ms-auto text-end', style={'display':'block'}),
                                dbc.Col(
                                    dcc.DatePickerSingle(
                                        id='db_outlet_auditdate',
                                        placeholder='Audit Date',
                                        month_format='MMM Do, YY',
                                    ),
                                    width=2,
                                    id='audit_date_filter',
                                    style={'display':'block'},
                                ),
                                dbc.Label('Product Group :', id='pg_label', width=1, className='ms-auto text-end', style={'display':'none'}),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='db_productgroup',
                                        placeholder='(All)',
                                        options=['DISHWASHERS']
                                    ),
                                    width=2,
                                    id='pg_filter',
                                    style={'display':'none'},
                                ),
                                dbc.Label('Brand :', id='brand_label', width=1, className='ms-auto text-end', style={'display':'none'}),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='db_brand',
                                        placeholder='(All)',
                                        options=['BEKO', 'BOSCH', 'BRANDT', 'CANDY', 'DE DIETRICH', 'ELBA', 'ELECTROLUX', 'EUROPACE', 'FISHER&PAYKEL', 'LG', 'MIELE', 'TOSHIBA', 'WHIRLPOOL'],
                                    ),
                                    width=2,
                                    id='brand_filter',
                                    style={'display':'none'},
                                ),
                            ],
                            className='mb-3' 
                        ),
                        html.Hr(),
                    ]
            ),

            html.Hr(),

            dcc.Tabs(id='db_tabs', 
                     value='sample_status_page',
                     children=[
                         dcc.Tab(label='Sample Status', value='sample_status_page'),
                         dcc.Tab(label='Market Simulation', value='ef_simulation_page'),
                     ]
                     ),

            # tab for panel metrics
            html.Div([
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H5("Total Active Shops in Panel", className='card-title'),
                        html.H1(id='shopcount_scorecard', className='card-text', style={"color": "#636EFA", 'fontSize': '150px'}),
                    ])
                ],
                style={"width": "30rem", "height":"20rem", "marginTop": "50px", "textAlign": "center", "boxShadow": "0 2px 5px rgba(0,0,0,0.1)"}
                )),
                dbc.Col(dcc.Graph(id='bar_graph')),
                dbc.Col(dcc.Graph(id='pie_chart')),
                dbc.Col(dcc.Graph(id='line_graph')),
                dbc.Col(dcc.Graph(id='bar_graph_2')),
                dbc.Col(dcc.Graph(id='bar_graph_3')),
                dbc.Col(dcc.Graph(id='bar_graph_4')),
                dbc.Col(dcc.Graph(id='bar_graph_5')),
            ]),
            ],
            id='sample_status_page',
            style={'display': 'block', 'justify-content': 'space-around', 'gap': '10px',}
            ),

            # tab for EF simulation
            html.Div([
            dbc.Row([
                # dbc.Col(dbc.Card([
                #     dbc.CardBody([
                #         html.H5("Total Shops in Panel", className='card-title'),
                #         html.H1(id='shopcount_scorecard', className='card-text', style={"color": "#636EFA", 'fontSize': '150px'}),
                #     ])
                # ],
                # style={"width": "30rem", "height":"20rem", "marginTop": "50px", "textAlign": "center", "boxShadow": "0 2px 5px rgba(0,0,0,0.1)"}
                # )),
                # dbc.Col(dcc.Graph(id='bar_graph_2')),
                # dbc.Col(dcc.Graph(id='bar_graph_3')),
                # dbc.Col(dcc.Graph(id='bar_graph_4')),
                dbc.Col(dcc.Graph(id='bar_brand_units')),
                dbc.Col(dcc.Graph(id='pie_brandshare_units')),
                dbc.Col(dcc.Graph(id='bar_brand_value')),
                dbc.Col(dcc.Graph(id='pie_brandshare_value')),
                dbc.Col(dcc.Graph(id='bar_item_units')),
                dbc.Col(dcc.Graph(id='bar_item_value')),
            ]),
            ],
            id='ef_simulation_page',
            style={'display': 'none', 'justify-content': 'space-around', 'gap': '10px',}
            ),
                
])

@app.callback(
    [
        Output('shopcount_scorecard', 'children'),
        Output('bar_graph', 'figure'),
        Output('pie_chart', 'figure'),
        Output('line_graph', 'figure'),
        Output('bar_graph_2', 'figure'),
        Output('bar_graph_3', 'figure'),
        Output('bar_graph_4', 'figure'),
        Output('bar_graph_5', 'figure'),
    ],
    [
        Input('url', 'pathname'),
        Input('db_outlet_id', 'value'),
        Input('db_outlet_size', 'value'),
        Input('db_outlet_retailer', 'value'),
        Input('db_outlet_channel', 'value'),
        Input('db_outlet_orgtype', 'value'),
        Input('db_outlet_region', 'value'),
        Input('db_outlet_copies', 'value'),
        Input('db_outlet_auditdate', 'date'),
    ],
)

def display_sample_health(pathname, outletid, size, retailer, channel, orgtype, region, copies, auditdate): 
    if pathname == '/dashboard':
        sql = """ SELECT s.outletid, s.ad_longitude, s.ad_latitude, s.shopsize, s.retailer, s.channel, r.orgtype, s.region, s.copies, s.audit_date
                    FROM shops s
                    LEFT JOIN retailers r ON s.retailer = r.retailer
                    WHERE s.is_active = 1
                """
        values = []

        cols = ['outletid', 'ad_longitude', 'ad_latitude', 'shopsize', 'retailer', 'channel', 'orgtype', 'region', 'copies', 'audit_date']

        df = db.querydatafromdatabase(sql, values, cols)

        cols_filter = ['outletid', 'shopsize', 'retailer', 'channel', 'orgtype', 'region', 'copies', 'audit_date']
        vals_filter = [outletid, size, retailer, channel, orgtype, region, copies, auditdate]

        dict_vals = dict(zip(cols_filter, vals_filter))
        
        for col, val in dict_vals.items():
            if val:
                df = df[df[col] == val]

        filtered_df = df

        total_shop_count = len(filtered_df.index)
        df_by_retailer = filtered_df.groupby('retailer')['outletid'].count().reset_index(name='store_count').sort_values('store_count', ascending=False)
        df_by_channel = filtered_df.groupby('channel')['outletid'].count().reset_index(name='store_count')
        df_by_size = filtered_df.groupby('shopsize')['outletid'].count().reset_index(name='store_count')
        df_by_auditdate = filtered_df.groupby('audit_date')['outletid'].count().reset_index(name='store_count')
        df_by_region = filtered_df.groupby('region')['outletid'].count().reset_index(name='store_count')
        df_by_orgtype = filtered_df.groupby('orgtype')['outletid'].count().reset_index(name='store_count')
        df_by_copies = filtered_df.groupby('copies')['outletid'].count().reset_index(name='store_count')
        
        fig_by_retailer = px.bar(df_by_retailer, x='retailer', y="store_count", title="Total Shops by Retailer")
        fig_by_channel = px.bar(df_by_channel, x='channel', y="store_count", title="Total Shops by Channel")
        fig_by_size = px.bar(df_by_size, x='shopsize', y="store_count", title="Total Shops by ShopSize")
        fig_by_auditdate = px.line(df_by_auditdate, x='audit_date', y="store_count", title="Shop Audit Trend", markers=True)
        fig_by_region = px.pie(df_by_region, names='region', values='store_count', title='Store Distribution')
        fig_by_orgtype = px.bar(df_by_orgtype, x='orgtype', y="store_count", title="Total Shops by OrgType")
        fig_by_copies = px.bar(df_by_copies, x='copies', y="store_count", title="Total Shops by Copies")
        
        fig_by_retailer.update_layout(height=500, width=800)
        fig_by_channel.update_layout(height=500, width=600)
        fig_by_size.update_layout(height=500, width=600)
        fig_by_auditdate.update_layout(height=500, width=800)
        fig_by_region.update_layout(height=500, width=500)
        fig_by_orgtype.update_layout(height=500, width=500)
        fig_by_copies.update_layout(height=500, width=500)
        
        return [total_shop_count, fig_by_retailer, fig_by_region, fig_by_auditdate, fig_by_orgtype, fig_by_channel, fig_by_copies, fig_by_size]

    else:
        raise PreventUpdate
    

@app.callback(
[
    Output('bar_brand_units', 'figure'),
    Output('pie_brandshare_units', 'figure'),
    Output('bar_brand_value', 'figure'),
    Output('pie_brandshare_value', 'figure'),
    Output('bar_item_units', 'figure'),
    Output('bar_item_value', 'figure'),
],
[
    Input('url', 'pathname'),
    Input('db_outlet_id', 'value'),
    Input('db_outlet_size', 'value'),
    Input('db_outlet_retailer', 'value'),
    Input('db_outlet_channel', 'value'),
    Input('db_outlet_orgtype', 'value'),
    Input('db_outlet_region', 'value'),
    Input('db_outlet_copies', 'value'),
    Input('db_outlet_auditdate', 'date'),
    Input('db_productgroup', 'value'),
    Input('db_brand', 'value'),
],
)

def display_market_simulation(pathname, outletid, size, retailer, channel, orgtype, region, copies, auditdate, productgroup, brand):
    if pathname == '/dashboard':
        sql = """
            SELECT sl.outletid, sp.shopsize, sp.retailer, sp. region, sp.copies, sp.channel, r.orgtype, sp.audit_date, i.itemid, i.itemname, i.brand, i.productgroup, sp.ext_factor, sl.units, sl.price
            FROM sales sl
            LEFT JOIN shops sp ON sl.outletid = sp.outletid
            LEFT JOIN retailers r ON sp.retailer = r.retailer
            LEFT JOIN items i ON sl.itemid = i.itemid
            WHERE 
                sp.is_active = 1
            """
        
        simulated_df = db.querydatafromdatabase(sql, [], ['outletid', 'shopsize', 'retailer', 'region', 'copies', 'channel', 'orgtype', 'audit_date', 'itemid', 'itemname','brand', 'productgroup', 'ext_factor', 'units', 'price'])
        simulated_df['units_extrapolated'] = simulated_df['units']*simulated_df['ext_factor']
        simulated_df['value'] = simulated_df['units_extrapolated']*simulated_df['price']

        cols_filter = ['outletid', 'shopsize', 'retailer', 'channel', 'orgtype', 'region', 'copies', 'productgroup', 'brand']
        vals_filter = [outletid, size, retailer, channel, orgtype, region, copies, productgroup, brand]

        dict_vals = dict(zip(cols_filter, vals_filter))
        
        for col, val in dict_vals.items():
            if val:
                simulated_df = simulated_df[simulated_df[col] == val]


        df_brand_units = simulated_df.groupby('brand')['units'].sum().reset_index(name='sales units').sort_values('sales units', ascending=False)
        df_brand_value = simulated_df.groupby('brand')['value'].sum().reset_index(name='sales value').sort_values('sales value', ascending=False)
        df_item_units = simulated_df.groupby('itemname')['units'].sum().reset_index(name='sales units').sort_values('sales units', ascending=False)
        df_item_value = simulated_df.groupby('itemname')['value'].sum().reset_index(name='sales value').sort_values('sales value', ascending=False)


        fig_brand_units = px.bar(df_brand_units, x='brand', y="sales units", title="Total Sales Units by Brand")
        fig_brandshare_units = px.pie(df_brand_units, names='brand', values='sales units', title='Sales Units Brand Share')

        fig_brand_value = px.bar(df_brand_value, x='brand', y="sales value", title="Total Sales Value by Brand (in SGD)")
        fig_brandshare_value = px.pie(df_brand_value, names='brand', values='sales value', title='Sales Value Brand Share')

        fig_item_units = px.bar(df_item_units, x='itemname', y="sales units", title="Total Sales Units by Item")
        fig_item_value = px.bar(df_item_value, x='itemname', y="sales value", title="Total Sales Value by Item (in SGD)")

        fig_brand_units.update_layout(height=500, width=700)
        fig_brandshare_units.update_layout(height=500, width=600)
        fig_brand_value.update_layout(height=500, width=700)
        fig_brandshare_value.update_layout(height=500, width=600)
        fig_item_units.update_layout(height=500, width=650)
        fig_item_value.update_layout(height=500, width=650)


        return [fig_brand_units, fig_brandshare_units, fig_brand_value, fig_brandshare_value, fig_item_units, fig_item_value]
    else:
        raise PreventUpdate



@app.callback(
[
    Output('sample_status_page', 'style'),
    Output('ef_simulation_page', 'style'),
    Output('pg_filter', 'style'),
    Output('pg_label', 'style'),
    Output('audit_date_label', 'style'),
    Output('audit_date_filter', 'style'),
    Output('brand_label', 'style'),
    Output('brand_filter', 'style'),
],
[
    Input('db_tabs','value'),
],
)

def movepages(tab):
    if tab == 'sample_status_page':
        return [{'display':'block'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'block'}, {'display':'block'}, {'display':'none'}, {'display':'none'}]
    else:
        return [{'display':'none'}, {'display':'block'}, {'display':'block'}, {'display':'block'}, {'display':'none'}, {'display':'none'}, {'display':'block'}, {'display':'block'}]
