import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.figure_factory as ff
import numpy as np

#######Clean data
url = 'https://raw.githubusercontent.com/benmcwilliams/flying-dog-beers/master/df_week.csv'
df_week = pd.read_csv(url, index_col=0)
df_week=df_week.sort_values(['23'],ascending=False)

z_labels_df=df_week.fillna(999)
z_labels=z_labels_df.applymap(lambda x: round(x))
z_labels=z_labels.astype(str)+'%'
z_labels=z_labels.replace('999%', np.NaN)

default=['Hokkaido','Tohoku','Tokyo','Hokuriku','Chubu','Kansai','Chugoku','Shikoku','Kyushu','Okinawa']
df_default = df_week[df_week.index.isin(default)]
z_labels_default = z_labels[z_labels.index.isin(default)]

x_labels=['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8',
          'Week 9', 'Week 10','Week 11','Week 12','Week 13','Week 14']

dict ={'AT': 'Austria',
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
    'NL': 'Netherlands',
    'NO': 'Norway',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'RS': 'Serbia',
    'SE': 'Sweden',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
    'UA': 'Ukraine',
       
    'CAL':'California',
    'CAR':'Carolinas',
    'CENT':'Central',
    'FLA':'Florida',
    'MIDA':'Mid-Atlantic',
    'MIDW':'Mid-West',
    'NE':'Northeast',
    'NY':'New York',
    'NW':'Northwest',
    'SW':'Southwest',
    'TEN':'Tennessee',
    'TEX':'Texas',
    'USA':'USA average',
       
    'NSW':'New South Wales',
    'QLD':'Queensland',
    'SA':'South Australia',
    'VIC':'Victoria',
    'TAS':'Tasmania',
    'AUS':'Australian average',
       
    'NER': 'India: North-East Region',
    'ER' : 'India: East Region',
    'WR' : 'India: West Region',
    'SR' : 'India: South Region',
    'NR' : 'India: North Region',
    'India':'Indian average',
       
    'Hokkaido':'Hokkaido',
    'Tohoku':'Tohoku',
    'Tokyo':'Tokyo',
    'Hokuriku':'Hokuriku',
    'Chubu':'Chubu',
    'Kansai ':'Kansai ',
    'Chugoku':'Chugoku',
    'Shikoku':'Shikoku',
    'Kyushu':'Kyushu',
    'Okinawa':'Okinawa',
    'Japan':'Japan'
       }

y_labels = []
for i in df_default.index.tolist():
    value=dict[i]
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
    html.H1('Bruegel global electricity tracker'),
    html.H2('Change in 2020 consumption relative to 2019'),
    html.Div([
    dcc.Dropdown(
        id = 'dropdown',
        options=[{'label': i, 'value': i} for i in df_week.index],
        value=['FR','DE','IT','PL','ES','GB'],
        multi=True,
        placeholder = 'Select regions'
    ),
              
    dcc.Dropdown(
        id='colour',
        options=[
            {'label': 'Greyscale', 'value': 'grey'},
            {'label': 'Traffic lights', 'value': 'red'},
        ],
        placeholder='Select colour scheme'
    ),             
    ],
    style={"width": "48%", "display": "inline-block"}),
          
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
        value=dict[i]
        y_labels.append(value)
    
    z = new_dff.values
    x = x_labels
    y=y_labels
    z_text = new_z_labels.values
    
    if colour == "red":
        scale=[[0, 'rgb(250,5,5)'], [1, 'rgb(9,230,50)']]
    else:
        scale=[[0, 'rgb(100,100,100)'], [1, 'rgb(300,300,300)']]
        
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
    autosize=True,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_showgrid=False, yaxis_showgrid=False)
    return(figure)

if __name__ == '__main__':
    app.run_server()
