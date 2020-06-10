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

########### Define your variables
beers=['Chesapeake Stout', 'Snake Dog IPA', 'Imperial Porter', 'Double Dog IPA']
ibu_values=[35, 60, 85, 75]
abv_values=[5.4, 7.1, 9.2, 4.3]
color1='lightblue'
color2='darkgreen'
mytitle='Beer Comparison'
tabtitle='beer!'
myheading='Flying Dog Beers'
label1='IBU'
label2='ABV'
githublink='https://github.com/austinlasseter/flying-dog-beers'
sourceurl='https://www.flyingdog.com/beers/'

########### Set up the chart
bitterness = go.Bar(
    x=beers,
    y=ibu_values,
    name=label1,
    marker={'color':color1}
)
alcohol = go.Bar(
    x=beers,
    y=abv_values,
    name=label2,
    marker={'color':color2}
)

beer_data = [bitterness, alcohol]
beer_layout = go.Layout(
    barmode='group',
    title = mytitle
)

beer_fig = go.Figure(data=beer_data, layout=beer_layout)


########### Initiate the app
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)
server = app.server
#app.title=tabtitle

########### Set up the layout
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

         figure = {
                 'data' : [go.Heatmap(
                     z=df_default,
                     x=x_labels,
                     y=['Germany','Spain','France','UK','Italy','Poland'],
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


if __name__ == '__main__':
    app.run_server()
