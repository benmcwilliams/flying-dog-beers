import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Data cleaning

df=pd.read_csv('bruegel_electricity_data_2.csv')
df['date_20'] = pd.to_datetime(df['date_20'])
df['Week_Number'] = df['date_20'].dt.week
df = df[df.holiday != 1]
df_week=df['adj_ratio'].groupby([df['ccode'],df['Week_Number']]).mean()
df_week=df_week.unstack()
df_week=df_week.mul(100)

df_default=df_week[df_week.index.isin(['FR','DE','IT','PL','ES','GB'])]

x_labels=['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8',
          'Week 9', 'Week 10']

# - - - - - - - - - 

app = dash.Dash(__name__)
server = app.server

# - - - - - - - 

app.layout = html.Div([
    html.H1('Weekly Electricity Consumption as % of 2019'),
    html.Div([
    html.Label('Select regions:'),
    dcc.Dropdown(
        id = 'dropdown',
        options=[{'label': i, 'value': i} for i in df_week.index],
        value=['FR','DE','IT','PL','ES','GB'],
        multi=True,
        #placeholder = 'Select regions'
    ),
    ],
    style={"width": "48%", "display": "inline-block"}),
            
    dcc.Graph(
        id='heatmap',

         figure = {
                 'data' : [go.Heatmap(
                     #z=df_default,
                     #x=x_labels,
                     #y=['Germany','Spain','France','UK','Italy','Poland'],
                     showscale = True,
                     colorscale = [[0, 'rgb(246,5,5)'], [1, 'rgb(9,230,50)']],
                     xgap = 2,
                     ygap = 5,
                     zmin=60,
                     zmax=120,
                     hovertemplate='%{x} : %{z:.2f}% <extra></extra>',
                     hoverongaps=False
                       )],
                 }        

            )
]) 

# - - - - - - - - - - - - 

@app.callback(
        Output(component_id='heatmap',component_property='figure'),
        [Input(component_id='dropdown',component_property='value')]  
 )

# - - - - - - - - - -

def update_graph(dropdown):
    dff_week = df_week
    new_dff = dff_week[dff_week.index.isin(dropdown)]
        
    figure = go.Figure(data=go.Heatmap(
                    z=new_dff,
                    x=x_labels,
                    y=new_dff.index,
                    showscale = True,
                    colorscale = [[0, 'rgb(246,5,5)'], [1, 'rgb(9,230,50)']],
                    xgap = 2,
                    ygap = 5,
                    zmin=60,
                    zmax=120,
                    hovertemplate='%{y}, %{x} : %{z:.0f}% <extra></extra>',
                    hoverongaps=False
                         ))
    figure.update_layout(
    #margin = dict(t=200,r=200,b=200,l=200),
    #width = 700, height = 700,
    autosize = False,
    )
    
    return (figure) 


if __name__ == '__main__':
    app.run_server()
