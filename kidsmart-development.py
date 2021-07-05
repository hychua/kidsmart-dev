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

app = dash.Dash(__name__, suppress_callback_exceptions=True)
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
army_icon = 'army.png' 
army_encoded = base64.b64encode(open(army_icon, 'rb').read())

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col, style={'border':'1px black solid','padding':5}) for col in dataframe.columns]) ] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col], style={'border':'1px black solid','padding':5}) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))
            ], 
        style={'font-size':28, 'border-collapse':'collapse', 'font-family':'calibri'}
)

# create a product div
def product_div(image, name, price, view, link, age):
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
            html.H1("Recommended Age: " + age, style={'font-family':'calibri'})
            
        ],
                                 style={'display':'inline-block','margin-left':25,
                                        }
                                 ),
        
        html.Div([
            dcc.Link('View Item', href=link, style={'display':'inline-block',
                                               'fontSize':32, 'margin':20}),
            
                html.Button(
                            id=view,
                            n_clicks=0,
                            children='View',
                            style={'fontSize':36,
                                   'color':'white',
                                   'backgroundColor':'green',
                                   'borderRadius':5,
                                   'height':75,'width':150,
                                   'font-family':'calibri', 'display':'none',
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
def product_page(image, name, price, slides, nxt, description, size, dim, age):
    # sizes data
    data_size = {'Size' : size, 'Dimensions' : dim, 'Age' : age}
    df_size = pd.DataFrame(data_size)
    return html.Div([
        html.Div([

        html.Div([

            html.Section(id="slideshow", children=[
                html.Div(id="slideshow-container", children=[
                    html.Div(id=slides),
                    html.Button(
                            id=nxt,
                            n_clicks=0,
                            children='Next Image',
                            style={'fontSize':32,
                                   'color':'rgb(255,123,0)',
                                   'backgroundColor':'rgb(255,255,255)',
                                   'borderRadius':5,
                                   'height':75,'width':200,
                                   'font-family':'minion',
                                   'margin':10,}),
                ])
            ])
        
        ])

        ],
                                 style={'backgroundColor':'rgb(255,255,255)',
                                        'margin':10,}),
        html.Div([
            
            html.H1(name, style={'font-family':'calibri'}),
            html.H1(price ,style={'color':'green','font-family':'calibri'}),
            
            
            html.Div([
                html.H1("Sizes Available:", style={'font-family':'calibri'}),
                generate_table(df_size),
                ], style={} ),
           

            html.P(description)
            
        ],
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
        html.Br(),
        dcc.Link('Go back to Search', href='/',
                 style={'fontSize':36}),
        
        ],
        style = {'border':'1px black solid','margin':3,'borderRadius':5,
                 'backgroundColor':'rgb(255,255,255)','padding':25})

bear_div = product_div(bear_encoded,"Bear Hooded Costume", "₱380.00","bear-button","/bear","2-8 yrs")
dragon_div = product_div(dragon_encoded,"Dragon Hooded Costume", "₱380.00","dragon-button","/dragon","2-8 yrs")
elephant_div = product_div(elephant_encoded,"Elephant Hooded Costume", "₱380.00","elephant-button","/elephant","2-8 yrs")
zebra_div = product_div(zebra_encoded,"Zebra Hooded Costume", "₱380.00","zebra-button","/zebra","2-8 yrs")
fairy_div = product_div(tinker_encoded,"Forest Fairy Costume", "₱540.00","fairy-button","/fairy","2-7 yrs")
army_div = product_div(army_encoded,"Army Costume", "₱540.00","army-button","/army","1-8 yrs")

bear_page = product_page(bear_encoded,"Bear Hooded Costume", "₱380.00","bear-image","bear-next",
                         "Brown bear costume for kids onesie/romper type with hood of animal for use in parties or pajama sleepwear. when washing, do not use bleach. Sizes may seem large for the age because the onesie type clothing is meant to be loose and breathable when worn. Other animal costumes are also available. Please check out our shop for the other costumes!",
                         ['S', 'M', 'L'],['14"x30"','15"x35"','16"x40"'],['2-4 yrs', '4-6 yrs', '6-8 yrs'])
dragon_page = product_page(dragon_encoded,"Dragon Hooded Costume", "₱380.00","dragon-image","dragon-next",
                         "Dragon costume for kids onesie/romper type with hood of animal for use in parties or pajama sleepwear. when washing, do not use bleach. Sizes may seem large for the age because the onesie type clothing is meant to be loose and breathable when worn. Other animal costumes are also available. Please check out our shop for the other costumes!",
                         ['S', 'M', 'L'],['14"x30"','15"x35"','16"x40"'],['2-4 yrs', '4-6 yrs', '6-8 yrs'])
elephant_page = product_page(elephant_encoded,"Elephant Hooded Costume", "₱380.00","elephant-image","elephant-next",
                         "Elephant costume for kids onesie/romper type with hood of animal for use in parties or pajama sleepwear. when washing, do not use bleach. Sizes may seem large for the age because the onesie type clothing is meant to be loose and breathable when worn. Other animal costumes are also available. Please check out our shop for the other costumes!",
                         ['S', 'M', 'L'],['14"x30"','15"x35"','16"x40"'],['2-4 yrs', '4-6 yrs', '6-8 yrs'])
zebra_page = product_page(zebra_encoded,"Zebra Hooded Costume", "₱380.00","zebra-image","zebra-next",
                         "Zebra costume for kids onesie/romper type with hood of animal for use in parties or pajama sleepwear. when washing, do not use bleach. Sizes may seem large for the age because the onesie type clothing is meant to be loose and breathable when worn. Other animal costumes are also available. Please check out our shop for the other costumes!",
                         ['S', 'M', 'L'],['14"x30"','15"x35"','16"x40"'],['2-4 yrs', '4-6 yrs', '6-8 yrs'])
fairy_page = product_page(tinker_encoded,"Forest Fairy Costume", "₱540.00","fairy-image","fairy-next",
                          "Tinkerbell or forest fairy costume for kids. Comes with: Detachable wings (via velcro)",
                          ['5','7','9','11','13'],['12"x19"','13"x21"','14"x23"','15"x25"','16"x27"'],['2-3 yrs','3-4 yrs','4-5 yrs','5-6 yrs','6-7 yrs'])
army_page = product_page(army_encoded,"Army Costume", "₱560.00","army-image","army-next",
                         "Army military fatigues costume set for kids with cap, polo, and shorts.",
                         ['0','2','4','6','8','10','12'],['24"x34"','25"x35"','26"x37"','27"x39"','28"x41"','29"x43"','30"x45"'],
                         ['1-2 yrs','2-3 yrs','3-4 yrs','4-5 yrs','5-6 yrs','6-7 yrs','7-8 yrs'])

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

product_page = html.Div([
                    dcc.Loading(
                                id="loading-2",
                                children=[html.Div([html.Div(id='products-content')])],
                                type="circle",
                            ),
    ])

about_page = html.Div([html.Br(),
    
                html.Div([
                    html.H2('Where We Are:'),
                    html.P('Tutuban Center Mall, C.M. Recto cor. R Antonio St., Binondo, Manila'),
                        html.Iframe(src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3860.82211922851!2d120.97065481432026!3d14.609206880783512!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3397ca0ce2555559%3A0x322c377e80b267e8!2sTutuban%20Shopping%20Mall!5e0!3m2!1sen!2sph!4v1624427880406!5m2!1sen!2sph"),
                    
                    html.P('168 Shopping Mall, 918 Soler St, Binondo, Manila, 1006 Metro Manila'),
                        html.Iframe(src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d61776.1681570088!2d120.9600329777667!3d14.598476951293357!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3397ca0ec391ad93%3A0x510fd5abc4fc32b8!2s168%20Shopping%20Mall!5e0!3m2!1sen!2sph!4v1624431949045!5m2!1sen!2sph"),
                    
                        ],
                    style={'display':'inline-block','margin-left':10}),
                
                html.Div([
                    html.H2('About Us:'),
                    html.P("Welcome to KIDSMART, where you can shop for the best clothes for your kids! "),
                    
                    html.P("We sell children's clothes and costumes from infant to early teens.") ,
                    
                    html.P("We hope you enjoy our products as much as we enjoy offering them to you. ʕ•́ᴥ•̀ʔっ♡ Happy Shopping! ♡"),
                    html.Br(),
                    html.H2('Contact Us:'),
                    html.P('8123-4567'),
                    html.P('example@gmail.com'),
                    
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                         style={'height':125}),
                    
                        ],
                    style={'display':'inline-block','margin-left':10})
                
                
                
                ],
    style={'color':'rgb(255,255,255)','backgroundColor':'rgb(0,0,0)',
           'font-family':'calibri','text-align':'center',
                           'fontSize':'110%'})

app.layout = html.Div([
    html.Div([
        
        header_page,
                    
        html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content')
        ]),
        
        about_page
  
    ],
    style={})
    
    ],
    )

# Search callbacks
@app.callback(Output('products-content', 'children'),
              
              [Input('search-bar', 'value'),
               ])
def products_content(search):
    div_list = list()
    if search == None:
        return [html.Br(),
                bear_div, dragon_div, elephant_div, zebra_div,
                fairy_div, army_div
                ]
    else:
        if search.lower() in "bear hooded costume":
            div_list.append(bear_div)
        if search.lower() in "dragon hooded costume":
            div_list.append(dragon_div)
        if search.lower() in "elephant hooded costume":
            div_list.append(elephant_div)
        if search.lower() in "zebra hooded costume":
            div_list.append(zebra_div)
        if search.lower() in "forest fairy costume":
            div_list.append(fairy_div)
        if search.lower() in "army costume":
            div_list.append(army_div)
    
    if div_list == []:
        return [html.H1('No items match your search.')]
    else:
        return div_list
    
# loading callback
@app.callback(Output("loading-output-2", "children"), Input("search-bar", "value"))
def input_triggers_nested(value):
    time.sleep(1)
    return value

# carousel image callbacks
@app.callback(Output('image', 'children'),
              [Input('next-button', 'n_clicks')])
def display_image(n):
    if n % 3 == 0:
        img = html.Img(src="http://placeimg.com/625/225/arch")
    elif n % 3 == 1:
        img = html.Img(src="http://placeimg.com/625/225/any")
    elif n % 3 == 2:
        img = html.Img(src="http://placeimg.com/625/225/animals")
    else:
        img = "None"
    return img

# carousel callbacks
def define_carousel(output, nxt, image, image1, image2, image3, image4):
    @app.callback(Output(output, 'children'),
                  [Input(nxt, 'n_clicks')])
    def display_carousel(n):
        # army pics
        icon = image
        encoded = base64.b64encode(open(icon, 'rb').read())
        icon1 = image1
        encoded1 = base64.b64encode(open(icon1, 'rb').read())
        icon2 = image2
        encoded2 = base64.b64encode(open(icon2, 'rb').read())
        icon3 = image3
        encoded3 = base64.b64encode(open(icon3, 'rb').read())
        icon4 = image4
        encoded4 = base64.b64encode(open(icon4, 'rb').read())
        if n % 5 == 0:
            img = html.Img(src='data:image/png;base64,{}'.format(encoded.decode()),
                                     style={'width':500})
        elif n % 5 == 1:
            img = html.Img(src='data:image/png;base64,{}'.format(encoded1.decode()),
                                     style={'width':500})
        elif n % 5 == 2:
            img = html.Img(src='data:image/png;base64,{}'.format(encoded2.decode()),
                                     style={'width':500})
        elif n % 5 == 3:
            img = html.Img(src='data:image/png;base64,{}'.format(encoded3.decode()),
                                     style={'width':500})
        elif n % 5 == 4:
            img = html.Img(src='data:image/png;base64,{}'.format(encoded4.decode()),
                                     style={'width':500})
        else:
            img = "None"
        return img

define_carousel('bear-image', 'bear-next', 'bear.jpg', 'bear1.jpg', 'bear2.jpg', 'bear3.jpg', 'bear4.jpg')
define_carousel('dragon-image', 'dragon-next', 'dragon.jpg', 'dragon1.jpg', 'dragon2.jpg', 'dragon3.jpg', 'dragon4.jpg')
define_carousel('elephant-image', 'elephant-next', 'elephant.jpg', 'elephant1.jpg', 'elephant2.jpg', 'elephant3.jpg', 'elephant4.jpg')
define_carousel('zebra-image', 'zebra-next', 'zebra.jpg', 'zebra1.jpg', 'zebra2.jpg', 'zebra3.jpg', 'zebra4.jpg')
define_carousel('fairy-image', 'fairy-next', 'tinker.jpg', 'tinker1.jpg', 'tinker2.jpg',
                'tinker3.jpg', 'tinker4.jpg')
define_carousel('army-image', 'army-next', 'army.png', 'army1.png', 'army2.png', 'army3.png', 'army4.png')

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/bear':
        return bear_page
    elif pathname == '/dragon':
        return dragon_page
    elif pathname == '/elephant':
        return elephant_page
    elif pathname == '/zebra':
        return zebra_page
    elif pathname == '/fairy':
        return fairy_page
    elif pathname == '/army':
        return army_page
    else:
        return product_page
    # You could also return a 404 "URL not found" page here

if __name__ == '__main__':
    app.run_server(debug=False)