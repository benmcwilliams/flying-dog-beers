import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd 

#######My data
url = 'https://raw.githubusercontent.com/benmcwilliams/flying-dog-beers/master/df_week.csv'
df_week = pd.read_csv(url, index_col=0)
df_week=df_week.set_index('ccode')

default=['Hokkaido','Tohoku','Tokyo','Hokuriko','Chubu','Kansai','Chugoku','Shikoku','Kyushu','Okinawa']
df_default = df_week[df_week.index.isin(default)]

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
    'Hokuriko':'Hokuriko',
    'Chubu':'Chubu',
    'Kansai':'Kansai',
    'Chugoku':'Chugoku',
    'Shikoku':'Shikoku',
    'Kyushu':'Kyushu',
    'Okinawa':'Okinawa',
    'JPN':'Japan'
       }

y_labels = []
for i in df_default.index.tolist():
    value=dict[i]
    y_labels.append(value)

z = df_default.values
x = x_labels
y=y_labels
z_text = np.around(z,decimals=0)

x_labels=['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8',
          'Week 9', 'Week 10','Week 11','Week 12','Week 13','Week 14']

########### Initiate the app
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)
server = app.server
#app.title=tabtitle

########### Set up the layout
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

         figure = ff.create_annotated_heatmap(z,
                    x=x,
                    y=y,
                    annotation_text=z_text, 
                    colorscale = [[0, 'rgb(250,5,5)'], [1, 'rgb(9,230,50)']],
                    xgap = 2,
                    ygap = 5,
                    zmin=-30,
                    zmax=10,),
            )
            
]) 


if __name__ == '__main__':
    app.run_server()
