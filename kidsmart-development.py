# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 22:08:51 2021

@author: HowardYsmaelLChua
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64
import pandas as pd
import dash_table
import time

df = pd.read_csv("product_table.csv")
columns=[{"name": i, "id": i} for i in df.columns]
data=df.to_dict("rows")
name = df.name.unique().tolist()

app = dash.Dash(__name__)
server = app.server

app.title = "KIDSMART Online Catalogue (DEV)"

image_filename = 'kidsmart_logo_red.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# carousel pictures
img0_icon = 'img0.png' 
img0 = base64.b64encode(open(img0_icon, 'rb').read())
img1_icon = 'img1.png' 
img1 = base64.b64encode(open(img1_icon, 'rb').read())
img5_icon = 'img5.png' 
img5 = base64.b64encode(open(img5_icon, 'rb').read())

# product pictures
bear_icon = 'bear.jpg' 
bear_encoded = base64.b64encode(open(bear_icon, 'rb').read())
dragon_icon = 'dragon.jpg' 
dragon_encoded = base64.b64encode(open(dragon_icon, 'rb').read())
elephant_icon = 'elephant.jpg' 
elephant_encoded = base64.b64encode(open(elephant_icon, 'rb').read())
zebra_icon = 'zebra.jpg' 
zebra_encoded = base64.b64encode(open(zebra_icon, 'rb').read())
tinker_icon = 'tinker.jpg' 
tinker_encoded = base64.b64encode(open(tinker_icon, 'rb').read())
fuchsia_icon = 'fuchsiadress.jpg' 
fuchsia_encoded = base64.b64encode(open(fuchsia_icon, 'rb').read())

# create a product div
def product_div(image, name, price, view):
    return html.Div([
        html.Div([
            
        html.Img(src='data:image/png;base64,{}'.format(image.decode()),
                                 style={'width':300}),

        
        ],
                                 style={'display':'inline-block','backgroundColor':'rgb(255,255,255)',
                                        'margin':10,}),
        html.Div([
            
            html.H1(name, style={'font-family':'calibri'}),
            html.H1(price ,style={'color':'green','font-family':'calibri'}),
            html.H1("Sizes Available: Ⓢ / Ⓜ / Ⓛ", style={'font-family':'calibri'}),
            html.H1("Recommended Age: 1-8 yrs", style={'font-family':'calibri'})
            
        ],
                                 style={'display':'inline-block','margin-left':25,
                                        }
                                 ),
        
        html.Div([
                html.Button(
                            id=view,
                            n_clicks=0,
                            children='View',
                            style={'fontSize':36,
                                   'color':'white',
                                   'backgroundColor':'green',
                                   'borderRadius':5,
                                   'height':75,'width':150,
                                   'font-family':'calibri', 'display':'inline-block',
                                   'margin':10}),
                html.Button(
                            id='fav-button',
                            n_clicks=0,
                            children='❤',
                            style={'fontSize':24,
                                   'color':'rgb(255,123,0)',
                                   'backgroundColor':'rgb(255,255,255)',
                                   'borderRadius':5,
                                   'height':50,'width':50,
                                   'font-family':'minion', 'display':'none',
                                   'margin':10,}),
                ],
                style={'float':'right'}),
        
        ],
        style = {'border':'1px black solid','margin':3,'borderRadius':5,
                 'backgroundColor':'rgb(255,255,255)'})

# create a product div
def product_page(image, name, price, view):
    return html.Div([
        html.Div([
            
        html.Img(src='data:image/png;base64,{}'.format(image.decode()),
                                 style={'width':500}),

        
        ],
                                 style={'display':'inline-block','backgroundColor':'rgb(255,255,255)',
                                        'margin':10,}),
        html.Div([
            
            html.H1(name, style={'font-family':'calibri'}),
            html.H1(price ,style={'color':'green','font-family':'calibri'}),
            html.H1("Sizes Available: Ⓢ / Ⓜ / Ⓛ", style={'font-family':'calibri'}),
            html.H1("Recommended Age: 1-8 yrs", style={'font-family':'calibri'}),
            html.P("Description")
            
        ],
                                 style={'display':'inline-block','margin-left':25,
                                        }
                                 ),
        
        html.Div([
                
                html.Button(
                            id='fav-button',
                            n_clicks=0,
                            children='❤',
                            style={'fontSize':24,
                                   'color':'rgb(255,123,0)',
                                   'backgroundColor':'rgb(255,255,255)',
                                   'borderRadius':5,
                                   'height':50,'width':50,
                                   'font-family':'minion', 'display':'none',
                                   'margin':10,}),
                ],
                style={'float':'right'}),
        
        ],
        style = {'border':'1px black solid','margin':3,'borderRadius':5,
                 'backgroundColor':'rgb(255,255,255)'})

bear_div = product_div(bear_encoded,"Bear Hooded Costume", "₱380.00","bear-button")
dragon_div = product_div(dragon_encoded,"Dragon Hooded Costume", "₱380.00","dragon-button")
elephant_div = product_div(elephant_encoded,"Elephant Hooded Costume", "₱380.00","elephant-button")
zebra_div = product_div(zebra_encoded,"Zebra Hooded Costume", "₱380.00","zebra-button")
fairy_div = product_div(tinker_encoded,"Forest Fairy Costume", "₱540.00","fairy-button")
fuchsia_div = product_div(fuchsia_encoded,"Fuchsia Floral Dress", "₱540.00","fuchsia-button")

bear_page = product_page(bear_encoded,"Bear Hooded Costume", "₱380.00","bear-button")
dragon_page = product_page(dragon_encoded,"Dragon Hooded Costume", "₱380.00","dragon-button")
elephant_page = product_page(elephant_encoded,"Elephant Hooded Costume", "₱380.00","elephant-button")
zebra_page = product_page(zebra_encoded,"Zebra Hooded Costume", "₱380.00","zebra-button")
fairy_page = product_page(tinker_encoded,"Forest Fairy Costume", "₱540.00","fairy-button")
fuchsia_page = product_page(fuchsia_encoded,"Fuchsia Floral Dress", "₱540.00","fuchsia-button")

header_page = html.Div([
    
    html.Div([
                        
                        html.Div([
                            html.Br(),
                            html.H1("KIDSMART Online Catalog",style={'fontSize':'350%','text-align':'center',
                                                      'color':'rgb(255,255,255)','font-family':'calibri'}),

                            dcc.Input(id='search-bar', type = 'search',
                                         placeholder='Search for Products',
                                         style={'fontSize':'275%','width':'80%',
                                                'text-align':'center', 'borderRadius':20,}),

                            ],
                                 style={'align-items': 'center',
                                        'justify-content': 'center'}),
                        html.Br(),
                    ],
                                 style={'text-align':'center','backgroundColor':'rgb(255,0,0)',}),
                    
                html.Div([
                    
                    dash_table.DataTable(
                    id='producttable',
                    row_selectable='single',
                    columns=columns,
                    data=data
                    ),
                    ],
                    style={'display':'none'}),

                ])

product_page = html.Div([dcc.Loading(
                                id="loading-2",
                                children=[html.Div([html.Div(id='products-content')])],
                                type="circle",
                            ),
    ]
    )

about_page = html.Div([
            
            
            html.H3('About Us:', style={'font-family':'avenir',}),
            html.P("Welcome to KIDSMART, where you can shop for the best clothes for your kids! "),
            
            html.P("We sell children's clothes and costumes from infant to early teens.") ,
            
            html.P("We hope you enjoy our products as much as we enjoy offering them to you. ʕ•́ᴥ•̀ʔっ♡ Happy Shopping! ♡"),
            
            html.Div([
                html.H3('Where We Are:'),
                
                html.P('Tutuban Center Mall, C.M. Recto cor. R Antonio St., Binondo, Manila'),
                    #html.Iframe(src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3860.82211922851!2d120.97065481432026!3d14.609206880783512!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3397ca0ce2555559%3A0x322c377e80b267e8!2sTutuban%20Shopping%20Mall!5e0!3m2!1sen!2sph!4v1624427880406!5m2!1sen!2sph"),
                
                html.P('168 Shopping Mall, 918 Soler St, Binondo, Manila, 1006 Metro Manila'),
                    #html.Iframe(src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d61776.1681570088!2d120.9600329777667!3d14.598476951293357!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3397ca0ec391ad93%3A0x510fd5abc4fc32b8!2s168%20Shopping%20Mall!5e0!3m2!1sen!2sph!4v1624431949045!5m2!1sen!2sph"),

            html.Div([
                html.H3('Contact Us:'),
                html.P('8123-4567'),
                html.P('example@gmail.com'),
            ],
                ),
            html.Div(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                         style={'height':125}),
                 ),        
                
            ]),

                  ],
                     style={'text-align':'center'}),

account_page = html.Div([
    html.H1("Coming Soon..."),
    html.P("This feature is not yet available. Check back soon for updates!"),
    html.Div([
                html.H3('Contact Us:'),
                html.P('8123-4567'),
                html.P('example@gmail.com'),
            ],
                ),
    ]
    )

tabs_styles = {
    'height': '20%'
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontSize':36,
    'font-family':'avenir'
    
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'fontWeight': 'bold',
    'color': 'red',
    'padding': '6px',
    'fontSize':36,
    'font-family':'avenir'
}

app.layout = html.Div([
    html.Div([
        
        header_page,
                    
        html.Div([
            dcc.Tabs(id='tabs', value='search', children=[
            dcc.Tab(label='🔎 Search', value='search',style=tab_style, 
                    selected_style=tab_selected_style,
                    ),
            dcc.Tab(label='📕 About Us', value='about',style=tab_style, 
                    selected_style=tab_selected_style,
                    ),
            dcc.Tab(label='💻 Account', value='account',style=tab_style, 
                    selected_style=tab_selected_style,),
        ],
            style=tabs_styles),
            
            html.Div(id='tabs-content', style={}),
            ]),
  
    ],
    style={})
    
    ],
    )

# Tab callbacks
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'about':
        return about_page
    elif tab == 'search':
        return product_page
    elif tab == 'account':
        return account_page

# Search callbacks
@app.callback(Output('products-content', 'children'),
              
              [Input('search-bar', 'value'),
               ])
def products_content(search):
    div_list = list()
    if search == None:
        return [html.Br(),
                bear_div, dragon_div, elephant_div, zebra_div,
                fairy_div, fuchsia_div,
                ]
    else:
        if search in "bear hooded costume":
            div_list.append(bear_div)
        if search in "dragon hooded costume":
            div_list.append(dragon_div)
        if search in "elephant hooded costume":
            div_list.append(elephant_div)
        if search in "zebra hooded costume":
            div_list.append(zebra_div)
        if search in "forest fairy costume":
            div_list.append(fairy_div)
        if search in "fuchsia floral dress":
            div_list.append(fuchsia_div)
    
    if div_list == []:
        return [html.H1('No items match your search.')]
    else:
        return div_list
    
@app.callback(Output("loading-output-2", "children"), Input("search-bar", "value"))
def input_triggers_nested(value):
    time.sleep(1)
    return value

if __name__ == '__main__':
    app.run_server(debug=False)