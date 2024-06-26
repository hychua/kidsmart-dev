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

import pandas as pd
import numpy as np
import cufflinks as cf
from apps.analytics import( create_plot_metric, 
                                    YEARS_INVENTORY,
                                    INVENTORY_TABLE_COLUMNS,
                                    ALL_BRANDS,
                                    ALL_CAT,
                                    ALL_TEXT
                                    )




# Append 'All' to ALL_BRANDS
ALL_BRANDS.append('All')
ALL_CAT.append('All')
ALL_TEXT.append('All')

# will be dcc.Dropdown multi = True or checkbox
FILTERS = ['Order Year','Buyer Region','Category','Product Name','Size','City Name']

# will be dcc.Dropdown multi = False
METRIC_TYPES = [
    'total_sales',
    'count_sales',
    'avg_sales',
    'curr_inventory',
    'curr_inventory2',
    'top_performers',
    'bottom_performers',
    'avg_net_profit',
    'top_avg_net_profit',
    'bottom_avg_net_profit',
    'avg_inventory_turnover',
    'top_avg_inventory_turnover',
    'bottom_avg_inventory_turnover',
    'sales_over_time'
]
METRIC_DICT = {
    'total_sales': 'Total Sales',
    'count_sales':'Sales Count',
    'avg_sales':'Avg Sales',
    'curr_inventory':'Current Inventory',
    'curr_inventory2':'Current Inventory 2',
    'top_performers':'Total Sales',
    'bottom_performers':'Total Sales',
    'avg_net_profit':'Avg Net Profit',
    'top_avg_net_profit':'Avg Net Profit',
    'bottom_avg_net_profit':'Avg Net Profit',
    'avg_inventory_turnover':'Inventory Turnover',
    'top_avg_inventory_turnover':'Inventory Turnover',
    'bottom_avg_inventory_turnover':'Inventory Turnover',
    'sales_over_time': 'Sales Over Time',
    
}

# Create layout

layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.Img(id="logo", src=app.get_asset_url("logo.png")),
                html.H4(children="Sales Performance Dashboard"),
                html.P(
                    id="description",
                    children="† Retail Sales from inventory data by year, buyer region, and product type \
                    ",
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                
                # start second graph
                html.Div(
                    id="graph-container",
                    children=[
                        
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Drag the slider to change the year:",
                                ),
                                dcc.Slider(
                                    id="years-slider",
                                    min=min(YEARS_INVENTORY),
                                    max=max(YEARS_INVENTORY),
                                    value=min(YEARS_INVENTORY),
                                    marks={
                                        str(year): {
                                            "label": str(year),
                                            "style": {"color": "#7fafdf"},
                                        }
                                        for year in YEARS_INVENTORY
                                    },
                                ),
                            ],
                        ),
                        
                        html.P(id="chart-selector",children="Select chart:"),
                        dcc.Dropdown(
                            options = [
                                {
                                    "label": "Total Sales",
                                    "value":"total_sales"
                                },
 
                                {
                                    "label": "Average Sales",
                                    "value":"avg_sales",
                                },

                                {
                                    "label": "Top Performers",
                                    "value":"top_performers",
                                },
                                {
                                    "label": "Bottom Performers",
                                    "value":"bottom_performers",
                                },

                                {
                                    "label": "Top Net Profit",
                                    "value":"top_avg_net_profit",
                                },
                                {
                                    "label": "Bottom Net Profit",
                                    "value":"bottom_avg_net_profit",
                                },
                                

                            ],
                            value = "total_sales",
                            id="chart-dropdown",
                            multi = False
                        ), # End Dropdown
                
                html.Div(className="row",
                    children=[
                    # Start changing graph
                        dcc.Graph(className="six columns",
                            id="selected-data",
                            figure = dict(
                                data=[dict(x=0, y=0)],
                                layout=dict(
                                    paper_bgcolor="#1f2630",
                                    plot_bgcolor="#1f2630",
                                    autofill=True,
                                    #margin=dict(t=75, r=50, b=100, l=50),
                                )
                            )

                        ), # end changing graph
                        
                # Start changing graph 2                      
                        dcc.Graph(className="six columns",
                            id="selected-data2",
                            figure = dict(
                                data=[dict(x=0, y=0)],
                                layout=dict(
                                    paper_bgcolor="#1f2630",
                                    plot_bgcolor="#1f2630",
                                    autofill=True,
                                    #margin=dict(t=75, r=50, b=100, l=50),
                                )
                            ) 

                        ) # end changing graph2
                        
                        ]
                        
                        ), # end div of graph1 and graph2
                
                # Start changing graph3
                        dcc.Graph(id="selected-data3",
                            figure = dict(
                                data=[dict(x=0, y=0)],
                                layout=dict(
                                    paper_bgcolor="#1f2630",
                                    plot_bgcolor="#1f2630",
                                    autofill=True,
                                    #margin=dict(t=75, r=50, b=100, l=50),
                                )
                            )

                        ), # end changing graph3
                    ],

                ),
                # end second graph

            ],
        ),
        
    ],
)


layout2 = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.Img(id="logo", src=app.get_asset_url("logo.png")),
                html.H4(children="Inventory Monitoring Dashboard"),
                html.P(
                    id="description",
                    children="† Inventory data and turnover rates based on sales data \
                    ",
                ),
            ],
        ),
            html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Drag the slider to change the year:",
                                ),
                                dcc.Slider(
                                    id="years-slider",
                                    min=min(YEARS_INVENTORY),
                                    max=max(YEARS_INVENTORY),
                                    value=min(YEARS_INVENTORY),
                                    marks={
                                        str(year): {
                                            "label": str(year),
                                            "style": {"color": "#7fafdf"},
                                        }
                                        for year in YEARS_INVENTORY
                                    },
                                ),
                            ],
                        ),
        
        # START BOTTOM DIV 1 
        html.Div(
            id="app-container-2",
            children=[
                html.Div(
                    children=[
                        html.P(id="brands-radio-text",
                        children="Choose Category: "),
                        dcc.RadioItems(
                            id="brands-radio",
                            options=[{'label': j, 'value':k} for j,k in zip(ALL_CAT,ALL_TEXT)],
                            value='All',
                            labelStyle={'display': 'inline-block'},                           
                        ),

                    ],className='three columns',
                ),
                html.Div(
                    children=[
                        html.P(id="product-dropdown-text",
                        children="Choose Product: "),
                        dcc.Dropdown(
                            id="product-dropdown",
                            options = [],   
                            value=[],
                            multi= True ,                           
                        ),

                    ],className='three columns',
                ),

                html.Div(
                    children=[
                        html.P(id="regions-dropdown-text",
                        children="Choose Region: "),
                        dcc.Dropdown(
                            id="region-dropdown",
                            #options=[{'label': k, 'value':k} for k in ALL_REGIONS],
                            value=[],
                            multi= True ,                           
                        ),

                    ],className='three columns',
                ),
                html.Div(
                    children=[
                        html.P(id="shoe-sizes-dropdown-text",
                        children="Choose Size: "),
                        dcc.Dropdown(
                            id="shoe-size-dropdown",
                            options=[], 
                            value=[],
                            multi= True ,                           
                        ),

                    ],className='three columns',
                ),

            ],className='row'

        ), # end bottom div 1

        # START BOTTOM DIV 2
        html.Div(
            id="app-container-3",
            children=[
                html.Div(
                    children=[
                        html.P(id="inventory-table-title",
                        children=["Inventory Management Table"],
                        ),
                        dash_table.DataTable(
                            id='inventory-table',
                            columns=[{"name": i, "id": i} for i in INVENTORY_TABLE_COLUMNS],
                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'fontWeight': 'bold',
                                'textAlign': 'left',
                                'font_size': '16px',
                                'border': '1px solid black',

                                },

                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': '#1f2630',
                                    'border': '1px solid grey' ,
                                },
                            ],

                            style_cell={
                                'backgroundColor': "#7fafdf",
                                'color': 'white',
                                'font_size': '15px',
                                'minWidth': '120px', 'width': '120px', 'maxWidth': '180px',
                                'whiteSpace': 'normal',
                            },
                            page_size=18,
                            style_table={'overflowX': '120px', 'overflowY':'auto'},
                            editable=True,
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            #column_selectable="single",
                            #row_selectable="multi",
                            
                        ),

                    ], className='six columns',

                ),

                html.Div(
                    id = "no-id",
                    children=[
                        html.P(id="inventory-gauage-title",
                        children=["Current Inventory"],
                        ),
                        html.Div(
                            id='curr-inventory-gauage-container',
                            children=[
                                daq.GraduatedBar(
                                    id="curr-inventory-gauage",
                                    color={
                                        "gradient":True,
                                        "ranges":{"green":[20,50],"yellow":[5,19],"red":[0,4]}
                                        },
                                    min = 0,
                                    max=50,
                                    step=1,
                                    labelPosition= 'bottom',
                                    showCurrentValue=True,
                                    size=800,
                                    value=15,
                                    vertical=False,
                                    theme={
                                        'dark': True,
                                    },
                                    
                                ), 

                            ],className='row'

                            
                        ),
                        html.Div(
                            id='curr-inventory-gauage-2-container',
                            children=[
                                daq.GraduatedBar(
                                    id ='curr-inventory-gauage-2',
                                    color={
                                        "gradient":True,
                                        "ranges":{"green":[20,50],"yellow":[5,19],"red":[0,4]}
                                        },
                                    min = 0,
                                    max=50,
                                    step=1,
                                    labelPosition= 'bottom',
                                    showCurrentValue=True,
                                    size=800,
                                    #value=15,
                                    vertical=False,
                                    theme={
                                        'dark': True,
                                    },
                                    
                                ), 

                            ],className='row'

                            
                        ),
                        html.Br(),
                        html.Br(),
                        html.Div(
                            id='current-inventory-led-container',
                            children=[
                                html.P(
                                    id='inventory-current-led-header',
                                    children=["Current Inventory"]
                                ),

                            ],className='row',
                        ),
                        daq.LEDDisplay(
                            id="inventory-current-led",
                            label="Total Inventory Available",
                            #value=5,
                            #backgroundColor="#FF5E5E",
                            size=90,
                        ), 
                
                        html.Br(),
                        html.Br(),
                        html.Div(
                            id='turnover-led-container',
                            children=[
                                html.P(
                                    id='inventory-turnover-led-header',
                                    children=["Inventory Turnover"]
                                ),

                            ],className='row',
                        ),

                        daq.LEDDisplay(
                            id="inventory-turnover-led",
                            label="Average Inventory Turnover ( in days )",
                            #value=5,
                            backgroundColor="#FF5E5E",
                            size=90,
                        ), 
                        html.Br(),
                        html.Br(),
                        dcc.Graph(
                            id="best-turnover-graph",
                            figure = dict(
                                data=[dict(x=0, y=0)],
                                layout=dict(
                                    paper_bgcolor="#1f2630",
                                    plot_bgcolor="#1f2630",
                                    autofill=True,
                                    margin=dict(t=75, r=50, b=100, l=50),
                                ),
                            ),

                        ), # end area graph

                        html.Br(),
                        html.Br(),
                        dcc.Graph(
                            id="worse-turnover-graph",
                            figure = dict(
                                data=[dict(x=0, y=0)],
                                layout=dict(
                                    paper_bgcolor="#1f2630",
                                    plot_bgcolor="#1f2630",
                                    autofill=True,
                                    margin=dict(t=75, r=50, b=100, l=50),
                                ),
                            ),

                        ), # end area graph                            

                    ], className='six columns',

                ),

            ],className='row'

        ), # end bottom div 2


    ],
)

layout3 = html.Div([    html.Div(' ',
        style={'backgroundColor':'rgb(0,123,255)','height':42}),
        html.Div([
            html.H2('Sales Inputs',
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
                id='submit-button',
                n_clicks=0,
                children='Submit',
                style={'fontSize':18,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':42})],
                    style={'float':'left','display':'inline-block',
                           'margin-left':20}
                     )],
            style={'float':'left','display':'inline-block'}
            )],
                    style={'float':'left','display': 'inline-block',
                           'margin-left':50})
            ])
        
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
                id='submit-button',
                n_clicks=0,
                children='Submit',
                style={'fontSize':18,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':42})],
                    style={'float':'left','display':'inline-block',
                           'margin-left':20}
                     )],
            style={'float':'left','display':'inline-block'}
            )],
                    style={'float':'left','display': 'inline-block',
                           'margin-left':50})
            ])

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
                id='submit-button',
                n_clicks=0,
                children='Submit',
                style={'fontSize':18,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':42})],
                    style={'float':'left','display':'inline-block',
                           'margin-left':20}
                     )],
            style={'float':'left','display':'inline-block'}
            )],
                    style={'float':'left','display': 'inline-block',
                           'margin-left':50})
            ])


# Create call back functions

# sales graphs
@app.callback(
    Output("selected-data", "figure"),
    [
        Input("chart-dropdown", "value"),
        Input("years-slider", "value"),
    ],
)
def display_selected_data(selected_data, year):

    filters = ['Order Year','Buyer Region']
    metric_type = selected_data
    curr_metric_col = METRIC_DICT[metric_type]
    curr_year = year

    df = create_plot_metric(filters,metric_type)
    dff = df[df['Order Year'] == curr_year]
    

    if selected_data == "total_sales":

        dff['Size'] = np.sqrt(dff[curr_metric_col])
        dff['Size'] = np.sqrt(dff['Size']).round(0)

        fig = px.scatter(dff, x="Buyer Region", y=curr_metric_col, color="Buyer Region",
                         size ="Size", hover_data=[curr_metric_col])



        fig.update_layout(
            title = f'Regional Retail: {curr_metric_col} {curr_year}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig


    if selected_data == "count_sales":
        pass

    if selected_data == "avg_sales":

        fig = px.histogram(dff, x='Buyer Region', y=curr_metric_col,
                    #title='Histogram of bills',
                    labels={'x':'Buyer Region', 'y':curr_metric_col }, # can specify one label per df column
                    opacity=.8,
                    log_y=True, # represent bars with log scale
                    color_discrete_sequence=['deepskyblue'] # color of histogram bars
                    )


        fig.update_layout(
            title = f'Regional Retail: {curr_metric_col}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig

    # will be a table and gauge
    if selected_data == "curr_inventory":
        pass


    if selected_data == "top_performers":

        values = dff[curr_metric_col]
        names = dff['Buyer Region'].unique()
  
        fig = px.pie(dff, values=values, names=names, color=names,)




        fig.update_layout(
            title = f'Regional Retail: {curr_metric_col}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig


    if selected_data == "bottom_performers":

        fig = px.bar(dff, x='Buyer Region', y =curr_metric_col , color=curr_metric_col,
                     hover_data = ['Buyer Region']
        
        )




        fig.update_layout(
            title = f'Regional Retail: {curr_metric_col}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig



    if selected_data == "avg_net_profit":
        pass


    if selected_data == "top_avg_net_profit":

        fig = px.density_heatmap(dff, x="Buyer Region", y=curr_metric_col)
     
        fig.update_layout(
            title = f'Regional Retail: {curr_metric_col}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig


    if selected_data == "bottom_avg_net_profit":

        fig = px.bar(dff, x='Buyer Region', y =curr_metric_col , color=curr_metric_col,
                     hover_data = ['Buyer Region']
        
        )




        fig.update_layout(
            title = f'Regional Retail: {curr_metric_col}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig





    if selected_data == "avg_inventory_turnover":
        pass


    if selected_data == "top_avg_inventory_turnover":
        pass

    if selected_data == "bottom_avg_inventory_turnover":
        pass



# sales graph 2
@app.callback(
    Output("selected-data2", "figure"),
    [
        Input("chart-dropdown", "value"),
        Input("years-slider", "value"),
    ],
)
def display_selected_data2(selected_data, year):

    filters = ['Order Year','Category']
    metric_type = selected_data
    curr_metric_col = METRIC_DICT[metric_type]
    curr_year = year

    df = create_plot_metric(filters,metric_type)
    dff = df[df['Order Year'] == curr_year]
    

    if selected_data == "total_sales":

        APP_PATH = pathlib.Path(__file__).parent
        DATA_PATH = APP_PATH.joinpath("../data").resolve()
        df_cat_data = pd.read_csv(DATA_PATH.joinpath("cat_text.csv"),parse_dates=True)
        
        dff['Size'] = np.sqrt(dff[curr_metric_col])
        dff['Size'] = np.sqrt(dff['Size']).round(0)
        merged_df = pd.merge(dff,df_cat_data, on='Category')

        fig2 = px.scatter(merged_df, x='Category_text', y=curr_metric_col, color='Category_text',
                         size ="Size", hover_data=[curr_metric_col])



        fig2.update_layout(
            title = f'Product Category: {curr_metric_col} {curr_year}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig2


    if selected_data == "count_sales":
        pass

    if selected_data == "avg_sales":

        fig = px.histogram(dff, x='Category', y=curr_metric_col,
                    #title='Histogram of bills',
                    labels={'x':'Category', 'y':curr_metric_col }, # can specify one label per df column
                    opacity=.8,
                    log_y=True, # represent bars with log scale
                    color_discrete_sequence=['deepskyblue'] # color of histogram bars
                    )


        fig.update_layout(
            title = f'Product Category: {curr_metric_col}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig

    # will be a table and gauge
    if selected_data == "curr_inventory":
        pass


    if selected_data == "top_performers":

        values = dff[curr_metric_col]
        names = dff['Category'].unique()
  
        fig = px.pie(dff, values=values, names=names, color=names,)




        fig.update_layout(
            title = f'Product Category: {curr_metric_col}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig


    if selected_data == "bottom_performers":

        fig = px.bar(dff, x='Category', y =curr_metric_col , color=curr_metric_col,
                     hover_data = ['Category']
        
        )




        fig.update_layout(
            title = f'Product Category: {curr_metric_col}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig



    if selected_data == "avg_net_profit":
        pass


    if selected_data == "top_avg_net_profit":

        fig = px.density_heatmap(dff, x='Category', y=curr_metric_col)
     
        fig.update_layout(
            title = f'Product Category: {curr_metric_col}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig


    if selected_data == "bottom_avg_net_profit":

        fig = px.bar(dff, x='Category', y =curr_metric_col , color=curr_metric_col,
                     hover_data = ['Category']
        
        )




        fig.update_layout(
            title = f'Product Category: {curr_metric_col}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig





    if selected_data == "avg_inventory_turnover":
        pass


    if selected_data == "top_avg_inventory_turnover":
        pass

    if selected_data == "bottom_avg_inventory_turnover":
        pass

# sales graph 3
@app.callback(
    Output("selected-data3", "figure"),
    [
        Input("chart-dropdown", "value"),
        Input("years-slider", "value"),
    ],
)
def display_selected_data3(selected_data, year):

    filters = ['Order Year','City Name']
    metric_type = selected_data
    curr_metric_col = METRIC_DICT[metric_type]
    curr_year = year

    df = create_plot_metric(filters,metric_type)
    dff = df[df['Order Year'] == curr_year]
    

    if selected_data == "total_sales":

        dff['Size'] = np.sqrt(dff[curr_metric_col])
        dff['Size'] = np.sqrt(dff['Size']).round(0)

        fig3 = px.scatter(dff, x='City Name', y=curr_metric_col, color='City Name',
                         size ="Size", hover_data=[curr_metric_col])



        fig3.update_layout(
            title = f'Sales by City: {curr_metric_col} {curr_year}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig3


    if selected_data == "count_sales":
        pass

    if selected_data == "avg_sales":

        fig = px.histogram(dff, x='City Name', y=curr_metric_col,
                    #title='Histogram of bills',
                    labels={'x':'City Name', 'y':curr_metric_col }, # can specify one label per df column
                    opacity=.8,
                    log_y=True, # represent bars with log scale
                    color_discrete_sequence=['deepskyblue'] # color of histogram bars
                    )


        fig.update_layout(
            title = f'Sales by City: {curr_metric_col}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig

    # will be a table and gauge
    if selected_data == "curr_inventory":
        pass


    if selected_data == "top_performers":

        values = dff[curr_metric_col]
        names = dff['City Name'].unique()
  
        fig = px.pie(dff, values=values, names=names, color=names,)




        fig.update_layout(
            title = f'Sales by City: {curr_metric_col}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig


    if selected_data == "bottom_performers":

        fig = px.bar(dff, x='City Name', y =curr_metric_col , color=curr_metric_col,
                     hover_data = ['City Name']
        
        )




        fig.update_layout(
            title = f'Sales by City: {curr_metric_col}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig



    if selected_data == "avg_net_profit":
        pass


    if selected_data == "top_avg_net_profit":

        fig = px.density_heatmap(dff, x='City Name', y=curr_metric_col)
     
        fig.update_layout(
            title = f'Regional Retail: {curr_metric_col}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig


    if selected_data == "bottom_avg_net_profit":

        fig = px.bar(dff, x='City Name', y =curr_metric_col , color=curr_metric_col,
                     hover_data = ['City Name']
        
        )




        fig.update_layout(
            title = f'Sales by City: {curr_metric_col}',
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            #margin=dict(t=75, r=50, b=100, l=50),
            font=dict(color="#2cfec1")

        )
        return fig





    if selected_data == "avg_inventory_turnover":
        pass


    if selected_data == "top_avg_inventory_turnover":
        pass

    if selected_data == "bottom_avg_inventory_turnover":
        pass

# Product and Brand
@app.callback(
    Output("product-dropdown", "options"),
    [
        Input("years-slider", "value"),
        Input("brands-radio", "value"),
    ],
)


def set_products_options(year, selected_brand):
    filters = ['Order Year','Buyer Region','Category','Product Name']
    metric_type = 'curr_inventory'
    curr_metric_col = METRIC_DICT[metric_type]
    curr_year = year

    df = create_plot_metric(filters,metric_type)

    if selected_brand != 'All':
        dff = df[(df['Order Year']==curr_year) & (df['Category']==selected_brand)]

    elif selected_brand == 'All':
        dff = df.copy()

    products = dff['Product Name'].unique().tolist()

    return [{'label':i, 'value':i} for i in products]



# Products from selected Brand
@app.callback(
    Output("region-dropdown", "options"),
    [
        Input("years-slider", "value"),
        Input("product-dropdown", "value"),
    ],
)


def set_brands_options(year, selected_product):

    filters = ['Order Year','Buyer Region','Category','Product Name']
    metric_type = 'curr_inventory'
    curr_metric_col = METRIC_DICT[metric_type]
    curr_year = year

    curr_products = [product for product in selected_product]
    
   

    df = create_plot_metric(filters,metric_type)
    if (len(curr_products)>=1):
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products))]
    
    else:
        dff = df.copy()


    regions = dff['Buyer Region'].unique().tolist()

    regions = sorted(regions)


    return [{'label':i, 'value':i} for i in regions]



# Get Shoe Size from Selected Region
@app.callback(
    Output("shoe-size-dropdown", "options"),
    [
        Input("years-slider", "value"),
        Input("product-dropdown", "value"),
        Input("region-dropdown", "value"),
    ],
)


def set_shoe_size_options(year, selected_product, selected_region):

    filters = ['Order Year','Buyer Region','Category','Product Name','Size']
    metric_type = 'curr_inventory'
    curr_metric_col = METRIC_DICT[metric_type]
    curr_year = year

    curr_regions = [region for region in selected_region]
    curr_products = [product for product in selected_product]
   

    df = create_plot_metric(filters,metric_type)

    # If Product is blank and regions is blank, show all shoe sizes
    if (len(curr_products)==0) and (len(curr_regions)==0):
        dff = df.copy()

    # If product is blank but region populated, show avail sizes
    elif (len(curr_products)==0) and (len(curr_regions)>=1):
        dff = df[(df['Order Year']==curr_year) & (df['Buyer Region'].isin(curr_regions))]

    # If product is populated but region is blank, show avail sizes
    elif(len(curr_products)>=1) and (len(curr_regions)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products))]

    # Other wise if product is populated and region is populated, show avail sizes
    else:
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products)) &(df['Buyer Region'].isin(curr_regions))]


    shoe_sizes = dff['Size'].unique().tolist()

    shoe_sizes = sorted(shoe_sizes)


    return [{'label':i, 'value':i} for i in shoe_sizes]


# Inventory management table
@app.callback(
    Output("inventory-table", "data"),
    [
        Input("years-slider", "value"),
        Input("brands-radio", "value"),
        Input("product-dropdown", "value"),
        Input("region-dropdown", "value"),
        Input("shoe-size-dropdown", "value"),
    ],
)


def set_shoe_size_options(year, selected_brand, selected_product, selected_region, selected_shoe_size):

    filters = ['Order Year','Buyer Region','Category','Product Name','Size']
    metric_type = 'curr_inventory'
    curr_metric_col = METRIC_DICT[metric_type]
    curr_year = year
    curr_brand = selected_brand
    curr_regions = [region for region in selected_region]
    curr_products = [product for product in selected_product]
    curr_shoe_sizes = [shoe for shoe in selected_shoe_size]

    df = create_plot_metric(filters,metric_type)
    # If Brand is All

    if curr_brand == 'All' and (len(curr_products)==0):
        dff = df[(df['Order Year']==curr_year)]

    elif curr_brand == 'All' and (len(curr_shoe_sizes)==0) and (len(curr_products)>=1) and (len(curr_regions)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products))]

    elif curr_brand != 'All' and (len(curr_shoe_sizes)==0) and (len(curr_products)==0) and (len(curr_regions)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Category']== selected_brand )]

    elif curr_brand != 'All' and (len(curr_shoe_sizes)==0) and (len(curr_products)>=1) and (len(curr_regions)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Category']== selected_brand ) & (df['Product Name'].isin(curr_products))]

    elif curr_brand != 'All' and (len(curr_shoe_sizes)==0) and (len(curr_products)>=1) and (len(curr_regions)>=1):
        dff = df[(df['Order Year']==curr_year) & (df['Category']== selected_brand ) & (df['Product Name'].isin(curr_products)) & (df['Buyer Region'].isin(curr_regions))]

    elif curr_brand != 'All' and (len(curr_shoe_sizes)==0) and (len(curr_products)>=1) and (len(curr_regions)==0) and(len(curr_shoe_sizes)>=1):
        dff = df[(df['Order Year']==curr_year) & (df['Category']== selected_brand ) & (df['Product Name'].isin(curr_products)) & (df['Size'].isin(curr_shoe_sizes))]

    elif curr_brand != 'All' and (len(curr_shoe_sizes)==0) and (len(curr_products)==0) and (len(curr_regions)>=1):
        dff = df[(df['Order Year']==curr_year) & (df['Buyer Region'].isin(curr_regions))]

    elif curr_brand != 'All' and (len(curr_shoe_sizes)>=1) and (len(curr_products)==0) and (len(curr_regions)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Category']== selected_brand ) & (df['Size'].isin(curr_shoe_sizes))]

    else:
        dff = df[(df['Order Year']==curr_year) &(df['Category']==selected_brand) & (df['Product Name'].isin(curr_products)) & (df['Buyer Region'].isin(curr_regions)) & (df['Size'].isin(curr_shoe_sizes))]
 


    data = dff.to_dict('records')

    return data


# Get Led Display
@app.callback(
    Output("inventory-turnover-led", "value"),
    [
        Input("years-slider", "value"),
        Input("region-dropdown", "value"),
        Input("brands-radio", "value"),
        Input("product-dropdown", "value"),

 
    ],
)


def set_led_display(year,selected_region,selected_brand,selected_product):

    filters = ['Order Year','Buyer Region','Category','Product Name']
    metric_type = 'avg_inventory_turnover'
    df = create_plot_metric(filters,metric_type)
   
    curr_metric_col = METRIC_DICT[metric_type]
    curr_year = year
    curr_brand = selected_brand
    curr_regions = [region for region in selected_region]
    curr_products = [product for product in selected_product]

    # If Brand is All, region is blank, and product is blank
    if curr_brand != 'All' and (len(curr_regions)==0) and (len(curr_products)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand)]

    elif curr_brand != 'All' and (len(curr_regions)==0) and (len(curr_products)>=1):
        dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand) &(df['Product Name'].isin(curr_products))]

    elif curr_brand == 'All' and (len(curr_regions)==0) and (len(curr_products)==0):
        dff = df[(df['Order Year']==curr_year)]
    
    elif curr_brand == 'All' and (len(curr_regions)==0) and (len(curr_products)>=1):
        dff = df[(df['Order Year']==curr_year) &  (df['Product Name'].isin(curr_products))]
    
    elif curr_brand == 'All' and (len(curr_regions)>=1) and (len(curr_products)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Buyer Region'].isin(curr_regions))]

    else:
        dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand) & (df['Buyer Region'].isin(curr_regions)) & (df['Product Name'].isin(curr_products))]
  


    return (round(dff[curr_metric_col].mean(),2))


@app.callback(
    Output("inventory-current-led", "value"),
    [
        Input("years-slider", "value"),
        Input("brands-radio", "value"),
        Input("product-dropdown", "value"),
        Input("region-dropdown", "value"),
        Input("shoe-size-dropdown", "value"),
    ],
)


def set_current_inventory_led(year, selected_brand, selected_product, selected_region, selected_shoe_size):

    filters = ['Order Year','Buyer Region','Category','Product Name','Size']
    filters2 = ['Order Year','Category','Product Name']
    metric_type = 'curr_inventory'
    metric_type2 = 'curr_inventory2'
    curr_metric_col = METRIC_DICT[metric_type]
    curr_metric_col2 = METRIC_DICT[metric_type2]
    curr_year = year
    curr_brand = selected_brand
    curr_regions = [region for region in selected_region]
    curr_products = [product for product in selected_product]
    curr_shoe_sizes = [shoe for shoe in selected_shoe_size]

    df = create_plot_metric(filters,metric_type)
    df2 = create_plot_metric(filters2,metric_type2)
    # If Brand is All

    if curr_brand == 'All' and (len(curr_products)==0) and (len(curr_regions)==0) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year)]

    elif curr_brand == 'All' and (len(curr_products)>=1) and (len(curr_regions)==0) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products))]

    elif curr_brand == 'All' and (len(curr_products)>=1) and (len(curr_regions)>=1) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products)) & (df['Buyer Region'].isin(curr_regions))]

    elif curr_brand == 'All' and (len(curr_products)>=1) and (len(curr_regions)>=1) and (len(curr_shoe_sizes)>=1):
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products)) & (df['Buyer Region'].isin(curr_regions)) & (df['Size'].isin(curr_shoe_sizes))]
        

    elif curr_brand != 'All' and (len(curr_products)==0) and (len(curr_regions)==0) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand)]


    elif curr_brand != 'All' and (len(curr_products)>=1) and (len(curr_regions)==0) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand) & (df['Product Name'].isin(curr_products))]


    elif curr_brand != 'All' and (len(curr_products)>=1) and (len(curr_regions)>=1) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand) & (df['Product Name'].isin(curr_products)) & (df['Buyer Region'].isin(curr_regions))]

    else:
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products)) & (df['Buyer Region'].isin(curr_regions)) & (df['Size'].isin(curr_shoe_sizes))]

    # if statements for curr_inventory2
    if curr_brand == 'All' and (len(curr_products)==0):
        dff2 = df2[(df2['Order Year']==curr_year)]
    
    elif curr_brand == 'All' and (len(curr_products)>=1):
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Product Name'].isin(curr_products))]
    
    elif curr_brand == 'All' and (len(curr_products)>=1) and len(curr_shoe_sizes)==0:
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Product Name'].isin(curr_products))]
    
    elif curr_brand == 'All' and (len(curr_products)>=1) and (len(curr_regions)>=1) and (len(curr_shoe_sizes)>=1):
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Product Name'].isin(curr_products))]
        
    
    elif curr_brand != 'All' and (len(curr_products)==0):
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Category']==curr_brand)]
    
    
    elif curr_brand != 'All' and (len(curr_products)>=1):
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Category']==curr_brand) & (df2['Product Name'].isin(curr_products))]
    
    
    elif curr_brand != 'All' and (len(curr_products)>=1):
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Category']==curr_brand) & (df2['Product Name'].isin(curr_products))]
    
    else:
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Product Name'].isin(curr_products))]
    
    
    curr_inventory = dff2[curr_metric_col2].sum() - dff[curr_metric_col].sum()


    return curr_inventory



# Get Shoe Size from Selected Region
@app.callback(
    Output("curr-inventory-gauage", "value"),
    [
        Input("years-slider", "value"),
        Input("brands-radio", "value"),
        Input("product-dropdown", "value"),
        Input("region-dropdown", "value"),
        Input("shoe-size-dropdown", "value"),
    ],
)


def set_gauge_value(year, selected_brand, selected_product, selected_region, selected_shoe_size):
    max_inventory = 50

    filters = ['Order Year','Buyer Region','Category','Product Name','Size']
    filters2 = ['Order Year','Category','Product Name']
    metric_type = 'curr_inventory'
    metric_type2 = 'curr_inventory2'
    curr_metric_col = METRIC_DICT[metric_type]
    curr_metric_col2 = METRIC_DICT[metric_type2]
    curr_year = year
    curr_brand = selected_brand
    curr_regions = [region for region in selected_region]
    curr_products = [product for product in selected_product]
    curr_shoe_sizes = [shoe for shoe in selected_shoe_size]

    df = create_plot_metric(filters,metric_type)
    df2 = create_plot_metric(filters2,metric_type2)
    # If Brand is All

    if curr_brand == 'All' and (len(curr_products)==0) and (len(curr_regions)==0) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year)]

    elif curr_brand == 'All' and (len(curr_products)>=1) and (len(curr_regions)==0) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products))]

    elif curr_brand == 'All' and (len(curr_products)>=1) and (len(curr_regions)>=1) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products)) & (df['Buyer Region'].isin(curr_regions))]

    elif curr_brand == 'All' and (len(curr_products)>=1) and (len(curr_regions)>=1) and (len(curr_shoe_sizes)>=1):
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products)) & (df['Buyer Region'].isin(curr_regions)) & (df['Size'].isin(curr_shoe_sizes))]
        

    elif curr_brand != 'All' and (len(curr_products)==0) and (len(curr_regions)==0) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand)]


    elif curr_brand != 'All' and (len(curr_products)>=1) and (len(curr_regions)==0) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand) & (df['Product Name'].isin(curr_products))]


    elif curr_brand != 'All' and (len(curr_products)>=1) and (len(curr_regions)>=1) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand) & (df['Product Name'].isin(curr_products)) & (df['Buyer Region'].isin(curr_regions))]

    else:
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products)) & (df['Buyer Region'].isin(curr_regions)) & (df['Size'].isin(curr_shoe_sizes))]

    # if statements for curr_inventory2
    if curr_brand == 'All' and (len(curr_products)==0):
        dff2 = df2[(df2['Order Year']==curr_year)]

    elif curr_brand == 'All' and (len(curr_products)>=1):
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Product Name'].isin(curr_products))]

    elif curr_brand == 'All' and (len(curr_products)>=1) and len(curr_shoe_sizes)==0:
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Product Name'].isin(curr_products))]

    elif curr_brand == 'All' and (len(curr_products)>=1) and (len(curr_regions)>=1) and (len(curr_shoe_sizes)>=1):
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Product Name'].isin(curr_products))]
        

    elif curr_brand != 'All' and (len(curr_products)==0):
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Category']==curr_brand)]


    elif curr_brand != 'All' and (len(curr_products)>=1):
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Category']==curr_brand) & (df2['Product Name'].isin(curr_products))]


    elif curr_brand != 'All' and (len(curr_products)>=1):
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Category']==curr_brand) & (df2['Product Name'].isin(curr_products))]

    else:
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Product Name'].isin(curr_products))]


    curr_inventory = dff2[curr_metric_col2].sum() - dff[curr_metric_col].sum()

    if curr_inventory > max_inventory:
        return max_inventory
    else:
        return curr_inventory

# Get Shoe Size from Selected Region
@app.callback(
    Output("curr-inventory-gauage-2", "value"),
    [
        Input("years-slider", "value"),
        Input("brands-radio", "value"),
        Input("product-dropdown", "value"),
        Input("region-dropdown", "value"),
        Input("shoe-size-dropdown", "value"),
    ],
)


def set_gauge_2_value(year, selected_brand, selected_product, selected_region, selected_shoe_size):
    max_inventory = 50

    filters = ['Order Year','Buyer Region','Category','Product Name','Size']
    filters2 = ['Order Year','Category','Product Name']
    metric_type = 'curr_inventory'
    metric_type2 = 'curr_inventory2'
    curr_metric_col = METRIC_DICT[metric_type]
    curr_metric_col2 = METRIC_DICT[metric_type2]
    curr_year = year
    curr_brand = selected_brand
    curr_regions = [region for region in selected_region]
    curr_products = [product for product in selected_product]
    curr_shoe_sizes = [shoe for shoe in selected_shoe_size]

    df = create_plot_metric(filters,metric_type)
    df2 = create_plot_metric(filters2,metric_type2)
    # If Brand is All

    if curr_brand == 'All' and (len(curr_products)==0) and (len(curr_regions)==0) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year)]

    elif curr_brand == 'All' and (len(curr_products)>=1) and (len(curr_regions)==0) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products))]

    elif curr_brand == 'All' and (len(curr_products)>=1) and (len(curr_regions)>=1) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products)) & (df['Buyer Region'].isin(curr_regions))]

    elif curr_brand == 'All' and (len(curr_products)>=1) and (len(curr_regions)>=1) and (len(curr_shoe_sizes)>=1):
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products)) & (df['Buyer Region'].isin(curr_regions)) & (df['Size'].isin(curr_shoe_sizes))]
        

    elif curr_brand != 'All' and (len(curr_products)==0) and (len(curr_regions)==0) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand)]


    elif curr_brand != 'All' and (len(curr_products)>=1) and (len(curr_regions)==0) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand) & (df['Product Name'].isin(curr_products))]


    elif curr_brand != 'All' and (len(curr_products)>=1) and (len(curr_regions)>=1) and (len(curr_shoe_sizes)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand) & (df['Product Name'].isin(curr_products)) & (df['Buyer Region'].isin(curr_regions))]

    else:
        dff = df[(df['Order Year']==curr_year) & (df['Product Name'].isin(curr_products)) & (df['Buyer Region'].isin(curr_regions)) & (df['Size'].isin(curr_shoe_sizes))]
    
    # if statements for curr_inventory2
    if curr_brand == 'All' and (len(curr_products)==0):
        dff2 = df2[(df2['Order Year']==curr_year)]

    elif curr_brand == 'All' and (len(curr_products)>=1):
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Product Name'].isin(curr_products))]

    elif curr_brand == 'All' and (len(curr_products)>=1) and len(curr_shoe_sizes)==0:
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Product Name'].isin(curr_products))]

    elif curr_brand == 'All' and (len(curr_products)>=1) and (len(curr_regions)>=1) and (len(curr_shoe_sizes)>=1):
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Product Name'].isin(curr_products))]
        

    elif curr_brand != 'All' and (len(curr_products)==0):
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Category']==curr_brand)]


    elif curr_brand != 'All' and (len(curr_products)>=1):
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Category']==curr_brand) & (df2['Product Name'].isin(curr_products))]


    elif curr_brand != 'All' and (len(curr_products)>=1):
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Category']==curr_brand) & (df2['Product Name'].isin(curr_products))]

    else:
        dff2 = df2[(df2['Order Year']==curr_year) & (df2['Product Name'].isin(curr_products))]


    curr_inventory = dff2[curr_metric_col2].sum() - dff[curr_metric_col].sum()

    if curr_inventory > max_inventory:
        return max_inventory
    else:
        return curr_inventory





# Get Shoe Size from Selected Region
@app.callback(
    Output("best-turnover-graph", "figure"),
    [
        Input("years-slider", "value"),
        Input("brands-radio", "value"),
        Input("region-dropdown", "value"),
  
    ],
)


def set_best_turnover_graph(year, selected_brand,selected_region):

    filters = ['Order Year','Buyer Region','Category','Product Name']
    metric_type = 'avg_inventory_turnover'
    curr_metric_col = METRIC_DICT[metric_type]
    curr_year = year
    curr_brand = selected_brand
    curr_regions = [region for region in selected_region]

  

    df = create_plot_metric(filters,metric_type)


    if curr_brand == 'All' and (len(curr_regions)==0):
        dff = df[(df['Order Year']==curr_year)]


    elif curr_brand == 'All' and (len(curr_regions)>=1):
        dff = df[(df['Order Year']==curr_year) & (df['Buyer Region'].isin(curr_regions))]

    elif curr_brand != 'All' and (len(curr_regions)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand)]


    elif curr_brand != 'All' and (len(curr_regions)>=1):
     dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand) & (df['Buyer Region'].isin(curr_regions))]

    else:
        dff = df.copy()


    dff = dff.head()





    fig = px.bar(dff, x='Product Name', y =curr_metric_col , color=curr_metric_col,
                    hover_data = ['Product Name','Buyer Region']
    
    )




    fig.update_layout(
        title = f'Best Turnover Rate',
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        margin=dict(t=75, r=50, b=100, l=50),
        font=dict(color="#2cfec1")

    )
    return fig





    
# Get Shoe Size from Selected Region
@app.callback(
    Output("worse-turnover-graph", "figure"),
    [
        Input("years-slider", "value"),
        Input("brands-radio", "value"),
        Input("region-dropdown", "value"),
  
    ],
)


def set_worse_turnover_graph(year, selected_brand,selected_region):

    filters = ['Order Year','Buyer Region','Category','Product Name']
    metric_type = 'avg_inventory_turnover'
    curr_metric_col = METRIC_DICT[metric_type]
    curr_year = year
    curr_brand = selected_brand
    curr_regions = [region for region in selected_region]

  

    df = create_plot_metric(filters,metric_type)


    if curr_brand == 'All' and (len(curr_regions)==0):
        dff = df[(df['Order Year']==curr_year)]


    elif curr_brand == 'All' and (len(curr_regions)>=1):
        dff = df[(df['Order Year']==curr_year) & (df['Buyer Region'].isin(curr_regions))]

    elif curr_brand != 'All' and (len(curr_regions)==0):
        dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand)]


    elif curr_brand != 'All' and (len(curr_regions)>=1):
     dff = df[(df['Order Year']==curr_year) & (df['Category']==curr_brand) & (df['Buyer Region'].isin(curr_regions))]

    else:
        dff = df.copy()


    dff = dff.tail()



    fig = px.bar(dff, x='Product Name', y =curr_metric_col , color=curr_metric_col,
                    hover_data = ['Product Name','Buyer Region']
    
    )




    fig.update_layout(
        title = f'Worse Turnover Rate',
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        margin=dict(t=75, r=50, b=100, l=50),
        font=dict(color="#2cfec1")

    )
    return fig         

