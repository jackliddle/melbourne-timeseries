import os
import pickle
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np

# Get the data (it was pickled by the notebook)
with open(os.path.join('temp', 'x.pickle'), 'rb') as file:
    x = pickle.load(file)
with open(os.path.join('temp', 'y.pickle'), 'rb') as file:
    y = pickle.load(file)

print(f"Loaded data:\n\tx: {x}\n\ty:{y}")


# Start your Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='scatter-plot',
        figure={
            'data': [
                go.Scatter(
                    x=x,
                    y=y,
                    mode='markers',
                    marker=dict(size=10, opacity=0.5),
                    selected=dict(marker=dict(color='red', size=12)),
                    unselected=dict(marker=dict(opacity=0.3)),
                )
            ],
            'layout': go.Layout(
                dragmode='lasso',  # Set drag mode to lasso for selection
                hovermode='closest',
                title='Select Points'
            )
        },
        style={'width': '1400px', 'height': '800px'}
    ),
    html.Pre(id='selected-data')
])

@app.callback(
    Output('selected-data', 'children'),
    [Input('scatter-plot', 'selectedData')]
)
def display_selected_data(selectedData):
    if selectedData is None:
        return 'No points selected'
    indices = [point['pointIndex'] for point in selectedData['points']]
    return f'Selected indices: {indices}'

if __name__ == '__main__':
    app.run_server(debug=True)
#%%

#%%
