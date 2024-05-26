
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server


# Connect to your app pages
from apps import dashboard
from apps import query


app.layout = html.Div([
    dcc.Location(id='url', refresh=False, pathname = '/apps/sales-dashboard'),
    html.Div([
        dcc.Link('Sales Dashboard|', href='/apps/sales-dashboard'),
        dcc.Link('Inventory Dashboard   |   ', href='/apps/inventory-dashboard'),
        dcc.Link('Orders|', href='/apps/orders'),
        dcc.Link('Inventory|', href='/apps/inventory'),
        dcc.Link('Category', href='/apps/category'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/sales-dashboard':
        return dashboard.layout
    if pathname == '/apps/inventory-dashboard':
        return dashboard.layout2
    if pathname == '/apps/orders':
        return query.layout3
    if pathname == '/apps/inventory':
        return query.layout4
    if pathname == '/apps/category':
        return query.layout5
    else:
        return "404 Page Error! Please choose a link"
    


if __name__ == '__main__':
    app.run_server(debug=False)