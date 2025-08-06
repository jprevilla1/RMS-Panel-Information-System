from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd

import dbconnect as db

def update_extcell():
        # recalculate extrapolation factors based on latest changes in shops database
        sql = """ SELECT 
                    s.shopsize, 
                    r.orgtype, 
                    s.channel, 
                    s.region,
                    COUNT(*) as count,
                    SUM(s.ext_factor) as ef_sum
            FROM shops s
                    LEFT JOIN retailers r ON s.retailer = r.retailer
            WHERE 
                    s.is_active = %s
            GROUP BY s.shopsize, r.orgtype, s.channel, s.region
                    """
        values = [1]

        cols = ['shopsize', 'orgtype', 'channel', 'region', 'count', 'ef_sum']

        latestdf = db.querydatafromdatabase(sql, values, cols)

        latestdf['ext_factor'] = latestdf['ef_sum']/latestdf['count']

        latestdf = latestdf.drop(['ef_sum', 'count'], axis=1)

        # update extrapolation records in SQL database

        delete_sql = """ DELETE FROM extrapolationcell;"""

        values = []

        df = db.modifydatabase(delete_sql, values)

        for index, row in latestdf.iterrows():
                try:
                        insert_sql=""" INSERT INTO extrapolationcell (shopsize, orgtype, channel, region, ext_factor)
                                VALUES
                                (%s, %s, %s, %s, %s)
                                """
                        values = [row['shopsize'], row['orgtype'], row['channel'], row['region'], row['ext_factor']]
                        df = db.modifydatabase(insert_sql, values)
                except:
                        pass

        # update EF column in shops table
        new_efs_sql = """SELECT s.outletid, e.ext_factor
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
        new_efs_df = db.querydatafromdatabase(new_efs_sql, [], ['outletid', 'ext_factor'])
        new_efs_df_tuples = list(zip(new_efs_df['ext_factor'], new_efs_df['outletid']))
        
        for factor, outletid in new_efs_df_tuples:
                update_sql = """UPDATE shops
                                SET ext_factor = %s
                                WHERE   is_active = 1 AND
                                        outletid = %s
                        """
                updated_efs_df = db.modifydatabase(update_sql, [factor, outletid])



                
