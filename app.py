import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd 

#######My data
url = 'https://raw.githubusercontent.com/benmcwilliams/flying-dog-beers/master/bruegel_electricity_data_2.csv'
df = pd.read_csv(url, index_col=0)
df['date_20'] = pd.to_datetime(df['date_20'])
df['Week_Number'] = df['date_20'].dt.week
df = df[df.holiday != 1]
df_week=df['adj_ratio'].groupby([df['ccode'],df['Week_Number']]).mean()
df_week=df_week.unstack()
df_week=df_week.mul(100)

df_default=df_week[df_week.index.isin(['FR','DE','IT','PL','ES','GB'])]

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
            
]) 


if __name__ == '__main__':
    app.run_server()
