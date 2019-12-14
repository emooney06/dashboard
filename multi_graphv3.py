import plotly.graph_objects as go
import html
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#app = dash.Dash()

# Alternate Path
df = pd.read_excel(r'C:\Test_Data\NDNQI_raw.xlsx')

#df = pd.read_excel(r'C:\Users\ejmooney\Desktop\testData\NDNQI_raw.xlsx')
df = df[['Unit - Clinical ID', 'Unit - Clinical DESC', 'Clinical Unit Type DESC', 'Measure Long Desc', \
    'Quarter', 'Unit', 'PGUnit Mean', 'PG Unit SD', 'PG Unit P10', 'PG Unit P25', 'PG Unit P50', \
    'PG Unit P75', 'PG Unit P90', 'PG Unit N']]
df = df.rename(columns={'Unit - Clinical DESC': 'unit_name', 'PG Unit P10':'PG_Unit_P10', \
    'PG Unit P25':'PG_Unit_P25', 'PG Unit P50':'PG_Unit_P50', 'PG Unit P75':'PG_Unit_P75', \
                        'PG Unit P90':'PG_Unit_P90'  })
df['Quarter'] = df['Quarter'].astype(str)
df['Quarter'] = df['Quarter'].str[:4] + 'Q' + df['Quarter'].str[4:5]
available_units = df['unit_name'].unique()
quarters = df['Quarter'].unique()
quarters = sorted(quarters)

micu = df[df['unit_name'] == 'MICU 12120']

app.layout = html.Div([
        html.Div([
        html.Label('Clinical Units'),
        dcc.Dropdown(
            id = 'units',
            options=[
            {'label': i, 'value': i} for i in available_units
            ],
            value ='',
            searchable= False,
            multi=True,
            style={'width': '75%'}
            ),
        ]),
        html.Div([
            html.Button(id='button', n_clicks=0, children='Add graph'),
            html.Div(id='container', 
                    children=dcc.Graph(figure={
                        'data': []
                        }, 
                    style={'display': 'none'}
                )),
        ])
])


@app.callback(
    Output('container', 'children'), 
    [Input('button', 'n_clicks')], 
    [State('units', 'value')])
def display_graphs(n_clicks, value):

    graphs = []
    for i in value:
        filtered_df = df[df.unit_name == i]
        min_y = filtered_df['PG_Unit_P10'].min() * .75
        max_y = filtered_df['PG_Unit_P90'].max() 
        tmp_df = df[df['unit_name'] == i]
        graphs.append(dcc.Graph(
            id='graph-{}'.format(i),
            figure={
                'data': [(go.Scatter(x=tmp_df['Quarter'], y=tmp_df['Unit'].round(2),
                               hovertemplate= 'Unit Score: %{y}', name= i,
                               showlegend= False,
                               line=dict(width=2.5, color='rgb(0,0,0)'))),
                      go.Scatter(
                                x=tmp_df['Quarter'], y=tmp_df['PG_Unit_P10'].round(2),
                                hovertemplate= '10th Pctl: %{y}',
                                showlegend= False,
                                name='PG 10th Pctl',
                                fill='tozeroy',
                                line=dict(width=0.5, color='rgb(151, 204, 255)')
                   ),
                      go.Scatter(
                                x=tmp_df['Quarter'], y=tmp_df['PG_Unit_P25'].round(2),
                                hovertemplate= '25th Pctl: %{y}',
                                showlegend= False,
                                name='PG 25th Pctl',
                                fill='tonexty',
                                line=dict(width=0.5, color='rgb(153, 255, 153)')
                    ),
                      go.Scatter(
                                x=tmp_df['Quarter'], y=tmp_df['PG_Unit_P50'].round(2),
                                hovertemplate= '50th Pctl: %{y}',
                                showlegend= False,
                                name='PG 50th Pctl',
                                fill='tonexty',
                                line=dict(width=0.5, color='rgb(255, 255, 102)')
                    ),
                       go.Scatter(
                                x=tmp_df['Quarter'], y=tmp_df['PG_Unit_P75'].round(2),
                                hovertemplate= '75th Pctl: %{y}',
                                showlegend= False,
                                name='PG 75th Pctl',
                                fill='tonexty',
                                line=dict(width=0.5, color='rgb(255, 204, 153)')
                    ),
                       go.Scatter(
                                x=tmp_df['Quarter'], y=tmp_df['PG_Unit_P90'].round(2),
                                hovertemplate= '90th Pctl: %{y}',
                                showlegend= False,
                                name='PG 90th Pctl',
                                fill='tonexty',
                                line=dict(width=0.5, color='rgb(255, 102, 102)')
                    )
                ],
                 'layout': 
                 {
                     'title': 'HOC/Pt Day {}'.format(i),
                     'yaxis': {'range': [min_y, max_y]}
                },
        },
           style={'height': '50vh', 'width': '90%'}))
    return html.Div(graphs)

if __name__ == '__main__':
    app.run_server(debug=True)

