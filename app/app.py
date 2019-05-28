import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
markdown_text = '''
To check it out, please use those interactive graphs!  
**Have fun**
'''

data = r'../food_coded.csv'
df = pd.DataFrame.from_csv(data)
df.reset_index(inplace=True)
df.GPA = pd.to_numeric(df['GPA'], errors='coerce')

app.layout = html.Div(children=[
    html.H1(children='How food choices determinate your GPA?'),
    html.Div(dcc.Markdown(children=markdown_text)),

    html.Label('Dropdown'),
    dcc.Dropdown(
        id='gender',
        options=[
            {'label': 'Man', 'value': 1},
            {'label': u'Woman', 'value': 2}
        ],
        value=2
    ),

    dcc.Graph(
        id='gender_histogram'
    )
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


if __name__ == '__main__':
    app.run_server(debug=True)