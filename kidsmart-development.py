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
                                 style={'width':200}),

        
        ],
                                 style={'display':'inline-block','backgroundColor':'rgb(255,255,255)',
                                        'margin':10,}),
        html.Div([
            
            html.H2(name),
            html.H1(price ,style={'color':'green'}),
            html.H3("Sizes Available: Ⓢ / Ⓜ / Ⓛ"),
            html.H3("Recommended Age: 1-8 yrs")
            
        ],
                                 style={'display':'inline-block','margin-left':25,
                                        }
                                 ),
        
        html.Div([
                html.Button(
                            id=view,
                            n_clicks=0,
                            children='View',
                            style={'fontSize':24,
                                   'color':'white',
                                   'backgroundColor':'green',
                                   'borderRadius':5,
                                   'height':50,'width':150,
                                   'font-family':'minion', 'display':'inline-block',
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

header_page = html.Div([
    
    html.Div([
                        html.Br(),
                        
                        html.Div([html.Button(
                        id='help-button',
                        n_clicks=0,
                        children='Help',
                        style={'fontSize':18,
                               'color':'rgb(255,123,0)',
                               'backgroundColor':'rgb(255,255,255)',
                               'borderRadius':5,
                               'height':42,'width':100,
                               'font-family':'minion', 'display':'none','float':'right',
                               'margin-right':10}),
                    
                    html.Button(
                        id='login-button',
                        n_clicks=0,
                        children='Login',
                        style={'fontSize':18,
                               'color':'rgb(255,123,0)',
                               'backgroundColor':'rgb(255,255,255)',
                               'borderRadius':5,
                               'height':42,'width':100,
                               'font-family':'minion', 'display':'none','float':'right',
                               'margin-left':10}),
                    ],
                            style={'float':'right'}),
                    

                        html.Div([
                            html.Br(),
                            html.H1("KIDSMART Online Catalog",style={'fontSize':'300%','text-align':'center',
                                                      'color':'rgb(255,255,255)','font-family':'calibri'}),
                            html.Br(),
                            dcc.Input(id='search-bar', type = 'search',
                                         placeholder='Search for Products',
                                         style={'fontSize':'150%','width':'75%',
                                                'text-align':'center', 'borderRadius':5,}),
                                                  
                            
                            ],
                                 style={'width': '75%', 'align-items': 'center',
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
                
                html.Div(id='products-content'),
                
                
                ])


fuchsia_page = html.Div([html.Div([
        html.Div([
        html.Img(src='data:image/png;base64,{}'.format(fuchsia_encoded.decode()),
                                 style={'height':300}),

        
        ],
                                 style={'display':'inline-block','backgroundColor':'rgb(255,255,255)',
                                        'margin':10,}),
        html.Div([
            
            html.H2("Fuchsia Floral Dress"),
            html.H1("₱540.00" ,style={'color':'green'}),
            html.H3("Sizes Available: Ⓢ / Ⓜ / Ⓛ"),
            html.H3("Recommended Age: 1-8 yrs"),
            html.H3("Description:"),
            html.P("Fuchsia floral dress for kids..."),
            html.H3("Size Chart")
            
            
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
                                   'height':42,'width':100,
                                   'font-family':'minion', 'display':'inline-block',
                                   'margin':10}),
                ],
                style={'float':'right'}),
        
        ],
        style = {'border':'1px black solid','margin':3,'borderRadius':5,})])

app.layout = html.Div([
    html.Div([
                    

        html.Div([
            
            header_page,
    
            ]),
            
        
        html.Div([
            
    
            html.H3('About Us:', style={'font-family':'avenir',}),
            html.P("Welcome to KIDSMART, where you can shop for the best clothes for your kids! "),
            
            html.P("We sell children's clothes and costumes from infant to early teens.") ,
            
            html.P("We hope you enjoy our products as much as we enjoy offering them to you. ʕ•́ᴥ•̀ʔっ♡ Happy Shopping! ♡"),
            
            html.Div([
                html.H3('Where We Are:'),
                html.Div([
                    html.P('Tutuban Center Mall, C.M. Recto cor. R Antonio St., Binondo, Manila'),
                    #html.Iframe(src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3860.82211922851!2d120.97065481432026!3d14.609206880783512!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3397ca0ce2555559%3A0x322c377e80b267e8!2sTutuban%20Shopping%20Mall!5e0!3m2!1sen!2sph!4v1624427880406!5m2!1sen!2sph",
                    #    ),
                ],
                         style={'display':'inline-block'}),
                
                html.Div([
                    html.P('168 Shopping Mall, 918 Soler St, Binondo, Manila, 1006 Metro Manila'),
                    #html.Iframe(src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d61776.1681570088!2d120.9600329777667!3d14.598476951293357!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3397ca0ec391ad93%3A0x510fd5abc4fc32b8!2s168%20Shopping%20Mall!5e0!3m2!1sen!2sph!4v1624431949045!5m2!1sen!2sph", 
                    #    ),
                    ],
                        style={'display':'inline-block','margin-left':25}),
                
            ]),
            
            html.Div(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                         style={'height':125,'float':'right','margin-right':20,
                                'display':'inline-block'}),
                 ),
                  ],
                     ),
            
            html.Div([
                html.H3('Contact Us:'),
                html.P('8123-4567'),
                html.P('example@gmail.com'),
            ],
                ),
    
    ],
    style={'backgroundColor':'rgb(203,183,162)'})
    
    ],
    )

# Search callbacks
@app.callback(Output('products-content', 'children'),
              
              [Input('search-bar', 'value'),
               ])
def costumes_content(search):
    div_list = list()
    if search == None:
        return [html.Br(),
                product_div(bear_encoded,"Bear Hooded Costume", "₱380.00","bear-button"),
                product_div(dragon_encoded,"Dragon Hooded Costume", "₱380.00","dragon-button"),
                product_div(elephant_encoded,"Elephant Hooded Costume", "₱380.00","elephant-button"),
                product_div(zebra_encoded,"Zebra Hooded Costume", "₱380.00","zebra-button"),
                product_div(tinker_encoded,"Forest Fairy Costume", "₱540.00","fairy-button"),
                product_div(fuchsia_encoded,"Fuchsia Floral Dress", "₱540.00","fuchsia-button"),
                ]
    else:
        if search in "bear hooded costume":
            div_list.append(product_div(bear_encoded,"Bear Hooded Costume", "₱380.00","bear-button"))
        if search in "dragon hooded costume":
            div_list.append(product_div(dragon_encoded,"Dragon Hooded Costume", "₱380.00","dragon-button"))
        if search in "elephant hooded costume":
            div_list.append(product_div(elephant_encoded,"Elephant Hooded Costume", "₱380.00","elephant-button"))
        if search in "zebra hooded costume":
            div_list.append(product_div(zebra_encoded,"Zebra Hooded Costume", "₱380.00","zebra-button"))
        if search in "forest fairy costume":
            div_list.append(product_div(tinker_encoded,"Forest Fairy Costume", "₱540.00","fairy-button"))
        if search in "fuchsia floral dress":
            div_list.append(product_div(fuchsia_encoded,"Fuchsia Floral Dress", "₱540.00","fuchsia-button"))
    
    if div_list == []:
        return [html.H1('No items match your search.')]
    else:
        return div_list


if __name__ == '__main__':
    app.run_server(debug=False)