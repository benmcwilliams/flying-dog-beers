import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.figure_factory as ff
import numpy as np

#######Clean data
url = 'https://raw.githubusercontent.com/benmcwilliams/flying-dog-beers/master/df_week_37.csv'
df_week = pd.read_csv(url, index_col=0)
df_week=df_week.sort_values(['46'],ascending=False)

z_labels_df=df_week.fillna(999)
z_labels=z_labels_df.applymap(lambda x: round(x))
z_labels=z_labels.astype(str)+'%'
z_labels=z_labels.replace('999%', np.NaN)

default=['Europe','USA','Japan','India','Australia','Russia']
df_default = df_week[df_week.index.isin(default)]
z_labels_default = z_labels[z_labels.index.isin(default)]

x_labels=['(Mar) Week 1', 'Week 2', 'Week 3', 'Week 4', '(Apr) Week 5', 'Week 6', 'Week 7', 'Week 8',
          'Week 9', '(May) Week 10','Week 11','Week 12','Week 13','(Jun) Week 14','Week 15','Week 16','Week 17',
         '(July) Week 18','Week 19','Week 20','Week 21','Week 22','(Aug) Week 23','Week 24','Week 25','Week 26',
         '(Sep) Week 27','Week 28','Week 29','Week 30','(Oct) Week 31','Week 32','Week 33','Week 34','Week 35',
          '(Nov) Week 36','Week 37']

ctry_labels ={
    'Europe':'European Average',
    'USA':'USA Average',
    'Japan': 'Japan Average',
    'India': 'India Average',
    'Australia': 'Australia Average',
    'Russia': 'Russian Average',
    
    'AT': 'Austria',
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'CH': 'Switzerland',
    'CZ': 'Czechia',
    'DE': 'Germany',
    'DK': 'Denmark',
    'EE': 'Estonia',
    'ES': 'Spain',
    'FI': 'Finland',
    'FR': 'France',
    'GB': 'UK',
    'GR': 'Greece',
    'HR': 'Croatia',
    'HU': 'Hungary',
    'IE': 'Ireland',
    'IT': 'Italy',
    'LT': 'Lithuania',
    'LV': 'Latvia',
    'NO': 'Norway',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'RS': 'Serbia',
    'SE': 'Sweden',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
    'UA': 'Ukraine',
    'TR': 'Turkey',
       
    'CAL':'California (USA)',
    'CAR':'Carolinas (USA)',
    'CENT':'Central (USA)',
    'FLA':'Florida (USA)',
    'MIDA':'Mid-Atlantic (USA)',
    'MIDW':'Mid-West (USA)',
    'NE':'Northeast (USA)',
    'NY':'New York (USA)',
    'NW':'Northwest (USA)',
    'SW':'Southwest (USA)',
    'TEN':'Tennessee (USA)',
    'TEX':'Texas (USA)',
       
    'NSW':'New South Wales (Aus)',
    'QLD':'Queensland (Aus)',
    'SA':'South Australia (Aus)',
    'VIC':'Victoria (Aus)',
    'TAS':'Tasmania (Aus)',
       
    'NER': 'North-East Region (India)',
    'ER' : 'East Region (India)',
    'WR' : 'West Region (India)',
    'SR' : 'South Region (India)',
    'NR' : 'North Region (India)',
       
    'Hokkaido':'Hokkaido (Japan)',
    'Tohoku':'Tohoku (Japan)',
    'Tokyo':'Tokyo (Japan)',
    'Hokuriku':'Hokuriku (Japan)',
    'Chubu':'Chubu (Japan)',
    'Kansai ':'Kansai (Japan) ',
    'Chugoku':'Chugoku (Japan)',
    'Shikoku':'Shikoku (Japan)',
    'Kyushu':'Kyushu (Japan)',
    'Okinawa':'Okinawa (Japan)',
          
    'Centre': 'Centre (Russia)',
    'East': 'East (Russia)',
    'Northwest': 'Northwest (Russia)',
    'Siberia': 'Siberia (Russia)',
    'South': 'South (Russia)',
    'Urals': 'Urals (Russia)',
    'Volga': 'Volga (Russia)'
       }

y_labels = []
for i in df_default.index.tolist():
    value=ctry_labels[i]
    y_labels.append(value)

y=y_labels
z = df_default.values
x = x_labels
z_text = z_labels_default.values

########### Initiate the app
app = dash.Dash(__name__)
server = app.server

########### Set up the layout
app.layout = html.Div([
          
    html.H1('Figure 2: global electricity tracker'),
    html.H2('Change in 2020 consumption relative to 2019'),
          
    html.Div([
    html.Div([          
    dcc.Dropdown(
        id='colour',
        options=[
            {'label': 'Greyscale', 'value': 'grey'},
            {'label': 'Traffic lights', 'value': 'red'},
            {'label': 'Blues', 'value': 'blue'},
            {'label': 'Reds', 'value': 'reds'}
        ],
        value = 'red',
        placeholder='Select colour scheme'
    )],
    style={"width": "30%"}),
              
    dcc.Dropdown(
        id = 'dropdown',
        options=[{'label': value, 'value': key} for key,value in ctry_labels.items()],
        value=['Europe','USA','Japan','India','Australia','Russia'],
        multi=True,
        placeholder = 'Select regions'
    ),                       
    ],
    style={"fontFamily" : "Georgia", "display": "inline-block", "width": "87%"}
    ),
          
    dcc.Graph(
        id='heatmap',

         figure = ff.create_annotated_heatmap(z,
                    x=x,
                    y=y,
                    colorscale = [[0, 'rgb(250,5,5)'], [1, 'rgb(9,230,50)']],
                    annotation_text=z_text, 
                    xgap = 2,
                    ygap = 5,
                    zmin=-30,
                    zmax=10,
                    hoverinfo='skip'),
         config={
        'displayModeBar': False}
    )            
]) 

@app.callback(
        Output(component_id='heatmap',component_property='figure'),
        [Input(component_id='dropdown',component_property='value'),
        Input('colour', 'value')]  
 )

# - - - - - - - - - -

def update_graph(dropdown,colour):
    dff_week = df_week
    zz_labels = z_labels
          
    new_dff = dff_week[dff_week.index.isin(dropdown)]
    new_z_labels = zz_labels[zz_labels.index.isin(dropdown)]
    
    y_labels = []
    for i in new_dff.index.tolist():
        value=ctry_labels[i]
        y_labels.append(value)
    
    z = new_dff.values
    x = x_labels
    y=y_labels
    z_text = new_z_labels.values
    
    if colour == "red":
        scale=[[0, 'rgb(250,5,5)'], [1, 'rgb(9,230,50)']]
    elif colour == 'grey':
        scale=[[0, 'rgb(100,100,100)'], [1, 'rgb(300,300,300)']]
    elif colour == 'blue':
        scale = [0, 'rgb(123,104,238)'], [1, 'rgb(240,248,255)']
    elif colour == 'reds':
        scale = [0, 'rgb(220, 7, 0)'], [1, 'rgb(249, 236, 123)']
        
    figure = ff.create_annotated_heatmap(z,
                    x=x,
                    y=y,
                    annotation_text=z_text, 
                    colorscale = scale,
                    xgap = 2,
                    ygap = 5,
                    zmin=-30,
                    zmax=10,
                    hoverinfo='skip')

    figure.update_layout(
    autosize=False,
    font=dict(
      family="Georgia"
    ),
    height=500 + 12.5*len(dropdown),
    width=1100,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_showgrid=False, yaxis_showgrid=False)
          
    return(figure)

if __name__ == '__main__':
    app.run_server()
