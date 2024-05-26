# -*- coding: utf-8 -*-
"""
Created on Sun May 26 16:39:01 2024

@author: megar
"""

import os
import pathlib
import re

from app import app

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import plotly.express as px
import dash_daq as daq
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np
import psycopg2
import cufflinks as cf
from apps.analytics import( querydatafromdatabase,
                            modifydatabase
                                    )


layout3 = html.Div([    html.Div(' ',
        style={'backgroundColor':'rgb(0,123,255)','height':42}),
        html.Div([
            html.H2('Orders Inputs',
                    style={'color':'rgb(0,123,255)'}),
            
            html.Div([
                html.Div([html.Label('Order ID:',
                       style={'font-weight':'bold'}),
                         html.Br(),html.Br(),
                         html.Label('Order Date:',
                       style={'font-weight':'bold'}),
                         html.Br(),html.Br(),
                        html.Label('Product Name:',
                       style={'font-weight':'bold'}),
                        html.Br(),html.Br(),
                        html.Label('Size:',
                       style={'font-weight':'bold'}),
                        html.Br(),
                        html.Label('Order Date:',
                       style={'font-weight':'bold'}),
                        html.Br(),html.Br(),
                        html.Label('Order Year:',
                       style={'font-weight':'bold'}),
                        html.Br(),html.Br(),
                        html.Label('Stock:',
                       style={'font-weight':'bold'})],

                        style={'float':'left','display': 'inline-block'}),
                
                html.Div([
                    dcc.Input(id='orderid',value=1, type='text'),
                    html.Br(),html.Br(),
                    dcc.Input(id='orderdate',value='2020-12-11', type='date'),
                    html.Br(),html.Br(),    
                    dcc.Input(id='productname',value='Thor Costume for Kids with Mask and Cape', type='text'),
                    html.Br(),html.Br(), 
                    dcc.Input(id='times',value='05/16/2024', type='text'),
                    html.Br(),html.Br(),
                    dcc.Input(id='sample',value=2024, type='text'),
                    html.Br(),html.Br(),
                    dcc.Input(id='percent',value=50, type='text'),
                    html.Br(),html.Br(),
                    
                html.Button(
                    id='query-button',
                    n_clicks=0,
                    children='Query',
                    style={'fontSize':28,
                    'borderRadius':5,
                    'height':42}
                ),    
                html.Button(
                    id='save-button',
                    n_clicks=0,
                    children='Save',
                    style={'fontSize':28,'color':'rgb(255,255,255)',
                    'backgroundColor':'rgb(0,123,255)',
                    'borderRadius':5,
                    'height':42}
                ),
                ]
                    ),
                dcc.Checklist(
                    options=[
                        {'label': 'Edit Mode', 'value': 1},
                    ],
                    id="mode",
                    value=[],
                    labelStyle={'display': 'inline-block'}
                )  ,        
                        
                  html.Br(),

                
                dash_table.DataTable(
                id='firstdatatable',
                row_selectable='single',
                ),
                html.Div([dcc.Input(id='submitmode')
                    ], style={'display':'none'}),
            
            ], 
                      )
                      ]
                      )
                               ],style={'float':'left','display': 'inline-block',
                                              'margin-left':50}
                               )
      
        
layout4 = html.Div([    html.Div(' ',
        style={'backgroundColor':'rgb(0,123,255)','height':42}),
        html.Div([
            html.H2('Inventory Inputs',
                    style={'color':'rgb(0,123,255)'}),
            
            html.Div([
                html.Div([html.Label('Product ID:',
                       style={'font-weight':'bold'}),
                         html.Br(),html.Br(),
                         html.Label('Product Name:',
                       style={'font-weight':'bold'}),
                         html.Br(),html.Br(),
                        html.Label('Category:',
                       style={'font-weight':'bold'}),
                        html.Br(),html.Br(),
                        html.Label('Size:',
                       style={'font-weight':'bold'}),
                        html.Br(),
                        html.Label('Order Date:',
                       style={'font-weight':'bold'}),
                        html.Br(),html.Br(),
                        html.Label('Order Year:',
                       style={'font-weight':'bold'}),
                        html.Br(),html.Br(),
                        html.Label('Stock:',
                       style={'font-weight':'bold'})],

                        style={'float':'left','display': 'inline-block'}),
                
                html.Div([
                    dcc.Input(id='hits',value=1, type='text'),
                    html.Br(),html.Br(),
                    dcc.Input(id='conversion',value='Toy', type='text'),
                    html.Br(),html.Br(),    
                    dcc.Input(id='revenue',value='Toy', type='text'),
                    html.Br(),html.Br(), 
                    dcc.Input(id='times',value='05/16/2024', type='text'),
                    html.Br(),html.Br(),
                    dcc.Input(id='sample',value=2024, type='text'),
                    html.Br(),html.Br(),
                    dcc.Input(id='percent',value=50, type='text'),
                    html.Br(),html.Br(),
                html.Button(
                    id='query-button2',
                    n_clicks=0,
                    children='Query',
                    style={'fontSize':28}
                ),    html.Button(
                    id='save-button2',
                    n_clicks=0,
                    children='Save',
                    style={'fontSize':28,'color':'rgb(255,255,255)',
                    'backgroundColor':'rgb(0,123,255)',
                    'borderRadius':5,
                    'height':42}
                ),
                dcc.Checklist(
                    options=[
                        {'label': 'Edit Mode', 'value': 1},
                    ],
                    id="mode2",
                    value=[],
                    labelStyle={'display': 'inline-block'}
                )  ,        
                        
                  html.Br(),

                
                dash_table.DataTable(
                id='seconddatatable',
                row_selectable='single',
                ),
                html.Div([dcc.Input(id='submitmode')
                    ], style={'display':'none'}),
            
            ], 
                      )
                      ]
                      )
                               ],style={'float':'left','display': 'inline-block',
                                              'margin-left':50}
                               )
                               ]
                               )
                                        

layout5 = html.Div([    html.Div(' ',
        style={'backgroundColor':'rgb(0,123,255)','height':42}),
        html.Div([
            html.H2('Category Inputs',
                    style={'color':'rgb(0,123,255)'}),
            
            html.Div([
                html.Div([html.Label('Product ID:',
                       style={'font-weight':'bold'}),
                         html.Br(),html.Br(),
                         html.Label('Product Name:',
                       style={'font-weight':'bold'}),
                         html.Br(),html.Br(),
                        html.Label('Category:',
                       style={'font-weight':'bold'}),
                        html.Br(),html.Br(),
                        html.Label('Size:',
                       style={'font-weight':'bold'}),
                        html.Br(),
                        html.Label('Order Date:',
                       style={'font-weight':'bold'}),
                        html.Br(),html.Br(),
                        html.Label('Order Year:',
                       style={'font-weight':'bold'}),
                        html.Br(),html.Br(),
                        html.Label('Stock:',
                       style={'font-weight':'bold'})],

                        style={'float':'left','display': 'inline-block'}),
                
                html.Div([
                    dcc.Input(id='hits',value=1, type='text'),
                    html.Br(),html.Br(),
                    dcc.Input(id='conversion',value='Toy', type='text'),
                    html.Br(),html.Br(),    
                    dcc.Input(id='revenue',value='Toy', type='text'),
                    html.Br(),html.Br(), 
                    dcc.Input(id='times',value='05/16/2024', type='text'),
                    html.Br(),html.Br(),
                    dcc.Input(id='sample',value=2024, type='text'),
                    html.Br(),html.Br(),
                    dcc.Input(id='percent',value=50, type='text'),
                    html.Br(),html.Br(),
                html.Button(
                    id='query-button3',
                    n_clicks=0,
                    children='Query',
                    style={'fontSize':28}
                ),    html.Button(
                    id='save-button3',
                    n_clicks=0,
                    children='Save',
                    style={'fontSize':28,'color':'rgb(255,255,255)',
                    'backgroundColor':'rgb(0,123,255)',
                    'borderRadius':5,
                    'height':42}
                ),
                dcc.Checklist(
                    options=[
                        {'label': 'Edit Mode', 'value': 1},
                    ],
                    id="mode3",
                    value=[],
                    labelStyle={'display': 'inline-block'}
                )  ,        
                        
                  html.Br(),

                
                dash_table.DataTable(
                id='thirddatatable',
                row_selectable='single',
                ),
                html.Div([dcc.Input(id='submitmode')
                    ], style={'display':'none'}),
            
            ], 
                      )
                      ]
                      )
                               ],style={'float':'left','display': 'inline-block',
                                              'margin-left':50}
                               )
                               ]
                               )

# orders callbacks
@app.callback(
    [
         Output('firstdatatable', 'data'),
         Output('firstdatatable', 'columns'),
         Output('submitmode','value')
     ],
    [Input('query-button', 'n_clicks'),
     Input('save-button', 'n_clicks'),
     Input('mode', 'value'),
     ],
    [
     State('orderdate', 'value'),
     State('productname', 'value'),
     State('firstdatatable','selected_rows'),     
     State('firstdatatable', 'data'),
     ])
def output(submit_button,save_button,mode, orderdate, productname, selected_rows,data):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="query-button":
           sql = "SELECT * FROM order"
           df = querydatafromdatabase(sql,[],["Order_ID","Order Date","Product Name"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           return [data,columns,2]
       elif eventid =="save-button":
           if 1 not in mode:
               sql = "SELECT max(Order_ID) as Order_ID FROM order"
               df = querydatafromdatabase(sql,[],["Order_ID"])
               Order_ID = int(df['Order_ID'][0])+1
               sqlinsert = "INSERT INTO order(Order_ID,Order Date,Product Name ) VALUES(%s, %s, %s)"
               modifydatabase(sqlinsert, [Order_ID,orderdate,productname])
               sql = "SELECT * FROM order"
               df = querydatafromdatabase(sql,[],["Order_ID","Order Date","Product Name"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")      
               return [data,columns,0]
           else:
               Order_ID=data[selected_rows[0]]['Order_ID']
               sqlinsert = "UPDATE order SET Order Date=%s,Product Name=%s WHERE Order_ID=%s"
               modifydatabase(sqlinsert, [orderdate,productname,Order_ID])
               sql = "SELECT * FROM order"
               df = querydatafromdatabase(sql,[],["Order_ID","Order Date","Product Name"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")      
               return [data,columns,0]
               
       elif eventid =="mode":
           sql = "SELECT * FROM order"
           df = querydatafromdatabase(sql,[],["Order_ID","Order Date","Product Name"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")          
           return [data,columns,2]
   else:
      raise PreventUpdate


@app.callback(
    [
     Output('orderdate', 'value'),
     Output('productname', 'value'),
     ],
    [
     Input('submitmode', 'value'),
     Input('firstdatatable','selected_rows')
     ],
    [
     State('orderdate', 'value'),
     State('productname', 'value'),
     State('firstdatatable', 'data'),
     ])
def clear(submitmode, selected_rows,orderdate, productname, data):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="submitmode" :
          if submitmode==0:
              return ["",""]
          elif submitmode==1:
              return [orderdate,productname]
          elif submitmode==2:
              if selected_rows:
                  
                  sql = "SELECT * FROM order WHERE Order_ID =%s"
                  df = querydatafromdatabase(sql,[data[selected_rows[0]]['Order_ID']],["Order_ID","Order Date","Product Name"])              
                          
                  return [df['Order Date'][0],df['Product Name'][0]]          
              else:
                  return ["",""]
       elif eventid =="firstdatatable":
           if selected_rows:
                sql = "SELECT * FROM order WHERE Order_ID =%s"
                df = querydatafromdatabase(sql,[data[selected_rows[0]]['Order_ID']],["Order_ID","Order Date","Product Name"])              
        
                return [df['Order Date'][0],df['Product Name'][0]]          
           else:
                return ["",""]      
   else:
      raise PreventUpdate
