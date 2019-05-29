import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
data = r'../food_coded.csv'
df = pd.DataFrame.from_csv(data)
df.reset_index(inplace=True)
df.GPA = pd.to_numeric(df['GPA'], errors='coerce')

app.layout = html.Div([
    html.Div([
        html.Span('How food choices determinate your GPA?', className='app-title'),
    ],
        className="row header"
    ),
    html.Div(className="wrapper",
             style={'display': 'grid',
                    'grid-template-columns': '100%',
                    'grid-column-gap': '1em',
                    'grid-row-gap': '1em',
                    'margin-left': '50px',
                    'margin-top': '20px',
                    'margin-right': '50px'},
             children=[
                 html.Div(className='wrapper',
                          style={'display': 'grid',
                                 'grid-template-columns': '30% 30% 30%'},
                          children=[
                              html.Div([
                                  html.Label('Gender'),
                                  dcc.Dropdown(
                                      id='gender',
                                      options=[
                                          {'label': 'Man', 'value': 1},
                                          {'label': u'Woman', 'value': 2}
                                      ],
                                      value=2
                                  )], style={'width': '80%', 'display': 'inline-block',
                                             'float': 'left'}),
                              html.Div(
                                  children=[
                                      html.Label('Healthy Habits'),
                                      dcc.Dropdown(
                                          id='healthy_habits',
                                          options=[
                                              {'label': 'How likely one eats fruits', 'value': 'fruit_day'},
                                              {'label': u'Does one check the nutritional information of a product',
                                               'value': 'nutritional_check'},
                                              {'label': 'Does one do any sport', 'value': 'sports'},
                                              {'label': 'How likely one eats veggies', 'value': 'veggies_day'},
                                              {'label': 'How many calories per day', 'value': 'calories_day'}
                                          ],
                                          value='fruit_day'
                                      )], style={'width': '100%', 'display': 'inline-block',
                                                 'float': 'left'})
                          ]),
                 html.Div(style={'display': 'grid',
                                 'grid-template-columns': '50% 50%',
                                 'grid-column-gap': '1.5em',
                                 'grid-row-gap': '1em'},
                          children=[
                              html.Div(children=[
                                  dcc.Graph(
                                      id='gender_histogram'
                                  )], style={'float': 'left', 'width': '100%', 'display': 'inline-block',
                                             'margin-right': '150px'}),
                              html.Div(children=[
                                  dcc.Graph(
                                      id='habits_barpl'
                                  )],
                                  style={'float': 'right', 'width': '100%', 'display': 'inline-block',
                                         'margin-right': '150px'}
                              )]),
                 html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css", rel="stylesheet"),
                 html.Link(
                     href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
                     rel="stylesheet"),
                 html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
                 html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
                 html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
                 html.Link(
                     href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css",
                     rel="stylesheet")
             ])

])


@app.callback(
    Output('gender_histogram', 'figure'),
    [Input('gender', 'value')]
)
def update(selected_gender):
    filtered_df = df[df.Gender == float(selected_gender)]
    trace = go.Histogram(x=filtered_df["GPA"], opacity=0.7, name="Male",
                         marker={"line": {"color": "#42cef4", "width": 0.2}},
                         nbinsx=16, customdata=filtered_df["GPA"], )
    layout = go.Layout(title=f"GPA Distribution", xaxis={"title": "GPA", "showgrid": False},
                       yaxis={"title": "Count", "showgrid": False}, )
    figure = {"data": [trace], "layout": layout}
    return figure


@app.callback(
    Output('habits_barpl', 'figure'),
    [Input('healthy_habits', 'value')])
def update_barplot(selected_habit):
    selected_var_man = df[df['Gender'] == 2].groupby(str(selected_habit))[str(selected_habit)].count()
    selected_var_woman = df[df['Gender'] == 1].groupby(str(selected_habit))[str(selected_habit)].count()

    healthy_habits_names = {'fruit_day': 'Nb. of fruits per day',
                            'nutritional_check': 'Nutritional facts checking',
                            'sports': 'Sport practicing',
                            'veggies_day': 'Nb. of veggies per dat',
                            'calories_day': 'Amount of calories per day'}

    names_m = selected_var_man.index
    y_m = list(selected_var_man)
    names_w = selected_var_woman.index
    y_w = list(selected_var_woman)

    man = go.Bar(x=names_m,
                 y=y_m,
                 textposition='auto',
                 name='man',
                 marker=dict(
                     color='rgb(8,48,107)',
                     line=dict(
                         color='rgb(8,48,107)',
                         width=1.5),
                 ),
                 opacity=0.6
                 )

    woman = go.Bar(x=names_w,
                   y=y_w,
                   textposition='auto',
                   name='woman',
                   marker=dict(
                       color='rgb(58,200,225)',
                       line=dict(
                           color='rgb(58,200,225)',
                           width=1.5),
                   ),
                   opacity=0.6
                   )
    layout = go.Layout(title=healthy_habits_names.get(selected_habit),
                       yaxis={"title": "Count"}, )
    figure = {"data": [man, woman], "layout": layout}
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
