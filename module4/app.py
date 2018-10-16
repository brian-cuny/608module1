import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np

mapbox_access_token = 'pk.eyJ1IjoiYnJpYW4tY3VueSIsImEiOiJjam5ha3h0MWw1M3h1M3huMW5iMnNjN2FxIn0.EC3dchAkxGcJJfixv0zNNw'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css']

# trees = pd.read_csv('trees.csv')
trees = pd.read_json('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=30000')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(style={'backgroundColor': 'white'}, children=[
    html.Div([
       html.H1('Tree Location and Health by Borough and Stewardship'),
       html.H2('Aggregated from 2015 Street Tree Census'),
       html.H3('By Brian Weinfeld')
    ], className='jumbotron'),
    dcc.Dropdown(
       id='my-dropdown',
       options=[
            {'label': 'All', 'value':'all' },
            {'label': 'Bronx', 'value': 'bronx'},
            {'label': 'Brooklyn', 'value': 'brooklyn'},
            {'label': 'Manhattan', 'value': 'manhattan'},
            {'label': 'Queens', 'value': 'queens'},
            {'label': 'Staten Island', 'value': 'staten'}
        ],
        value='all'
    ),
    html.Div([
        html.Div([
            html.H2('Location of Trees'),
            dcc.Graph(id='g1')
        ], className='six columns'),
        html.Div([
            html.H2('Health by Species'),
            dcc.Graph(id='g3')
        ], className='six columns'),
    ], className='row'),
    html.Div([
        html.Div([
            html.H2('Health by Borough'),
            dcc.Graph(id='g2')
        ], className='offset-by-two columns, four columns'),
        html.Div([
            html.H2('Health by Steward'),
            dcc.Graph(id='g4')
        ], className='four columns'),
    ], className='row'),
    html.Div(id='intermediate-value', style={'display': 'none'})
], className='container-fluid')


@app.callback(
    dash.dependencies.Output('intermediate-value', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')]
)
def clean_data(value):
    if value == 'bronx':
        trees_copy = trees[trees['boroname'] == 'Bronx'].copy()
    elif value == 'brooklyn':
        trees_copy = trees[trees['boroname'] == 'Brooklyn'].copy()
        # trees_copy = pd.read_json('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=30000&boroname=Brooklyn')
    elif value == 'queens':
        trees_copy = trees[trees['boroname'] == 'Queens'].copy()
        # trees_copy = pd.read_json('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=30000&boroname=Queens')
    elif value == 'staten':
        trees_copy = trees[trees['boroname'] == 'Staten Island'].copy()
        # trees_copy = pd.read_json('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=30000&boroname=Staten%20Island')
    elif value == 'manhattan':
        trees_copy = trees[trees['boroname'] == 'Manhattan'].copy()
    #     trees_copy = pd.read_json('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=30000&boroname=Manhattan')
    else:
        trees_copy = trees.copy()

    return trees_copy.to_json(date_format='iso', orient='split')


@app.callback(
    dash.dependencies.Output('g1', 'figure'),
    [dash.dependencies.Input('intermediate-value', 'children')]
)
def update_map(data):
    trees_copy = pd.read_json(data, orient='split')

    return {
        'data': [
            go.Scattermapbox(
                lat=trees_copy['latitude'],
                lon=trees_copy['longitude'],
                mode='markers',
                marker=dict(
                    size=8,
                    opacity=0.1,
                    color=trees['health'].map({'Poor': 'red', 'Fair': 'yellow', 'Good': 'green'}),
                ),
                text=trees['health'],
            ),
        ],
        'layout': go.Layout(
            autosize=False,
            width=1000,
            height=1000,
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=40.7128,
                    lon=-74.0060
                ),
                pitch=0,
                zoom=10,
            ),
        )
    }



@app.callback(
    dash.dependencies.Output('g3', 'figure'),
    [dash.dependencies.Input('intermediate-value', 'children')]
)
def update_species(data):
    trees_copy = pd.read_json(data, orient='split')

    species = trees_copy.groupby(['spc_common', 'health'])[['tree_id']].count().reset_index().copy()
    species_poor = species[species['health'] == 'Poor']
    species_fair = species[species['health'] == 'Fair']
    species_good = species[species['health'] == 'Good']

    return {
        'data': [
            go.Bar(x=species['spc_common'].unique(),
                   y=species_poor['tree_id'],
                   name='Poor',
                   marker=dict(
                       color='red'
                   )
                   ),
            go.Bar(x=species['spc_common'].unique(),
                   y=species_fair['tree_id'],
                   name='Fair',
                   marker=dict(
                       color='yellow'
                   )
                   ),
            go.Bar(x=species['spc_common'].unique(),
                   y=species_good['tree_id'],
                   name='Good',
                   marker=dict(
                       color='green'
                   )
                   )
        ],
        'layout': go.Layout(
            autosize=False,
            width=800,
            height=1000,
            barmode='stack',
            xaxis=dict(
                fixedrange=True
            ),
            yaxis=dict(
                fixedrange=True
            ),
            showlegend=False
        )
    }

@app.callback(
    dash.dependencies.Output('g2', 'figure'),
    [dash.dependencies.Input('intermediate-value', 'children')]
)
def update_borough(data):
    trees_copy = pd.read_json(data, orient='split')

    count = trees_copy.groupby(['boroname', 'health'])['tree_id'].count().reset_index().copy()
    count_poor = count[count['health'] == 'Poor']
    count_fair = count[count['health'] == 'Fair']
    count_good = count[count['health'] == 'Good']

    return {
        'data': [
            go.Bar(
                x=count['boroname'].unique(),
                y=count_poor['tree_id'],
                name='Poor',
                marker=dict(
                    color='red'
                )
            ),
            go.Bar(
                x=count['boroname'].unique(),
                y=count_fair['tree_id'],
                name='Fair',
                marker=dict(
                    color='yellow'
                )
            ),
            go.Bar(
                x=count['boroname'].unique(),
                y=count_good['tree_id'],
                name='Good',
                marker=dict(
                    color='green'
                )
            )
        ],
        'layout': go.Layout(
            autosize=False,
            width=600,
            height=600,
            barmode='stack',
            xaxis=dict(
                fixedrange=True
            ),
            yaxis=dict(
                fixedrange=True
            ),
            showlegend=False
        )
    }


@app.callback(
    dash.dependencies.Output('g4', 'figure'),
    [dash.dependencies.Input('intermediate-value', 'children')]
)
def update_steward(data):
    trees_copy = pd.read_json(data, orient='split')

    steward_copy = trees_copy.groupby(['steward', 'health'])['tree_id'].count().reset_index().copy()
    steward_copy['steward'] = steward_copy['steward'].map(
        {'None': 'None', '1or2': 'Some', '3or4': 'Many', '4orMore': 'Most', np.nan: 'None'})
    steward_copy['steward'] = pd.Categorical(steward_copy['steward'], ['None', 'Some', 'Many', 'Most'])
    steward_copy = steward_copy.sort_values(['steward', 'health'])
    steward_poor = steward_copy[steward_copy['health'] == 'Poor']
    steward_fair = steward_copy[steward_copy['health'] == 'Fair']
    steward_good = steward_copy[steward_copy['health'] == 'Good']

    return {
        'data': [
            go.Bar(
                x=trees['steward'].unique(),
                y=steward_poor['tree_id'],
                name='Poor',
                marker=dict(
                    color='red'
                )
            ),
            go.Bar(
                x=trees['steward'].unique(),
                y=steward_fair['tree_id'],
                name='Fair',
                marker=dict(
                    color='yellow'
                )
            ),
            go.Bar(
                x=trees['steward'].unique(),
                y=steward_good['tree_id'],
                name='Good',
                marker=dict(
                    color='green'
                )
            )
        ],
        'layout': go.Layout(
            autosize=False,
            width=600,
            height=600,
            barmode='stack',
            xaxis=dict(
                fixedrange=True
            ),
            yaxis=dict(
                fixedrange=True
            ),
            showlegend=False
        )
    }


if __name__ == '__main__':
    app.run_server()