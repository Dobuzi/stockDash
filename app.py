import dash
from dash import dcc, html, Input, Output
import yfinance as yf
import pandas as pd
from plotly import graph_objs as go
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='multiprocessing')

# Set up the database
engine = create_engine('sqlite:///assets.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define the Asset model
class Asset(Base):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True)
    label = Column(String)
    value = Column(Float)

Base.metadata.create_all(engine)

# Define sample asset allocation data
def get_asset_allocation():
    return {
        'labels': ['US Stocks', 'Korea Stocks', 'US Treasury Bonds', 'Cash USD', 'Cash KRW'],
        'values': [40, 20, 20, 10, 10],  # Example percentages
    }

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Stock Dashboard'),
    dcc.Graph(id='asset-allocation'),
    html.Div(children=[
        html.H3('Asset Allocation Input'),
        html.Div([
            dcc.Dropdown(
                id='asset-type-1',
                options=[
                    {'label': 'Stock', 'value': 'Stock'},
                    {'label': 'Bonds', 'value': 'Bonds'},
                    {'label': 'Cash', 'value': 'Cash'}
                ],
                value='Stock'
            ),
            dcc.Input(id='asset-label-1', type='text', placeholder='Label 1', value='TSLA'),
            dcc.Input(id='asset-value-1', type='number', placeholder='Value 1', value=40),
            dcc.Dropdown(
                id='asset-unit-1',
                options=[
                    {'label': 'USD', 'value': 'USD'},
                    {'label': 'KRW', 'value': 'KRW'}
                ],
                value='USD'
            ),
        ], style={'display': 'flex', 'align-items': 'center', 'padding': '10px 10px'}),
        html.Div([
            dcc.Dropdown(
                id='asset-type-2',
                options=[
                    {'label': 'Stock', 'value': 'Stock'},
                    {'label': 'Bonds', 'value': 'Bonds'},
                    {'label': 'Cash', 'value': 'Cash'}
                ],
                value='Stock'
            ),
            dcc.Input(id='asset-label-2', type='text', placeholder='Label 2', value='AAPL'),
            dcc.Input(id='asset-value-2', type='number', placeholder='Value 2', value=20),
            dcc.Dropdown(
                id='asset-unit-2',
                options=[
                    {'label': 'USD', 'value': 'USD'},
                    {'label': 'KRW', 'value': 'KRW'}
                ],
                value='USD'
            ),
        ], style={'display': 'flex', 'align-items': 'center', 'padding': '10px 10px'}),
        html.Div([
            dcc.Dropdown(
                id='asset-type-3',
                options=[
                    {'label': 'Stock', 'value': 'Stock'},
                    {'label': 'Bonds', 'value': 'Bonds'},
                    {'label': 'Cash', 'value': 'Cash'}
                ],
                value='Stock'
            ),
            dcc.Input(id='asset-label-3', type='text', placeholder='Label 3', value='CPNG'),
            dcc.Input(id='asset-value-3', type='number', placeholder='Value 3', value=20),
            dcc.Dropdown(
                id='asset-unit-3',
                options=[
                    {'label': 'USD', 'value': 'USD'},
                    {'label': 'KRW', 'value': 'KRW'}
                ],
                value='USD'
            ),
        ], style={'display': 'flex', 'align-items': 'center', 'padding': '10px 10px'}),
        html.Div([
            dcc.Dropdown(
                id='asset-type-4',
                options=[
                    {'label': 'Stock', 'value': 'Stock'},
                    {'label': 'Bonds', 'value': 'Bonds'},
                    {'label': 'Cash', 'value': 'Cash'}
                ],
                value='Stock'
            ),
            dcc.Input(id='asset-label-4', type='text', placeholder='Label 4', value='BRK-B'),
            dcc.Input(id='asset-value-4', type='number', placeholder='Value 4', value=10),
            dcc.Dropdown(
                id='asset-unit-4',
                options=[
                    {'label': 'USD', 'value': 'USD'},
                    {'label': 'KRW', 'value': 'KRW'}
                ],
                value='USD'
            ),
        ], style={'display': 'flex', 'align-items': 'center', 'padding': '10px 10px'}),
        html.Div([
            dcc.Dropdown(
                id='asset-type-5',
                options=[
                    {'label': 'Stock', 'value': 'Stock'},
                    {'label': 'Bonds', 'value': 'Bonds'},
                    {'label': 'Cash', 'value': 'Cash'}
                ],
                value='Stock'
            ),
            dcc.Input(id='asset-label-5', type='text', placeholder='Label 5', value='Cash KRW'),
            dcc.Input(id='asset-value-5', type='number', placeholder='Value 5', value=10),
            dcc.Dropdown(
                id='asset-unit-5',
                options=[
                    {'label': 'USD', 'value': 'USD'},
                    {'label': 'KRW', 'value': 'KRW'}
                ],
                value='USD'
            ),
        ], style={'display': 'flex', 'align-items': 'center', 'padding': '10px 10px'}),
        html.Button('Update Allocation', id='update-allocation-button', n_clicks=0),
    ]),
    html.Div(children=[
        html.H3('Add New Asset'),
        dcc.Input(id='new-asset-label', type='text', placeholder='New Asset Label'),
        dcc.Input(id='new-asset-value', type='number', placeholder='New Asset Value'),
        dcc.Dropdown(
            id='new-asset-type',
            options=[
                {'label': 'Stock', 'value': 'Stock'},
                {'label': 'Bonds', 'value': 'Bonds'},
                {'label': 'Cash', 'value': 'Cash'}
            ],
            placeholder='Select Asset Type'
        ),
        dcc.Dropdown(
            id='new-asset-unit',
            options=[
                {'label': 'USD', 'value': 'USD'},
                {'label': 'KRW', 'value': 'KRW'}
            ],
            placeholder='Select Asset Unit'
        ),
        html.Button('Add Asset', id='add-asset-button', n_clicks=0),
    ], style={'padding': '10px 10px'}),
    dcc.Input(id='ticker-input', type='text', placeholder='Enter stock ticker', value='TSLA, AAPL, CPNG, BRK-B'),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='output-data'),
    dcc.Graph(id='example-graph'),
])

# Callback to fetch and display data
def fetch_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        if hist.empty:
            return f"No data found for ticker: {ticker}"
        return hist
    except Exception as e:
        return f"Error fetching data for ticker: {ticker}. Please check if the ticker is valid."

@app.callback(
    Output('output-data', 'children'),
    Input('submit-button', 'n_clicks'),
    Input('ticker-input', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0 and value:
        data = fetch_data(value)
        if isinstance(data, pd.DataFrame):
            return html.Div([
                html.H4(f'Data for {value}'),
                dcc.Graph(
                    figure={
                        'data': [
                            go.Candlestick(
                                x=data.index,
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close'],
                                name=value
                            )
                        ],
                        'layout': {
                            'title': f'Stock Price for {value} (Candlestick)'
                        }
                    }
                )
            ])
        else:
            return html.Div(f'Error: {data}')
    return html.Div('Enter a ticker and press submit.')

def parse_ticker_to_name(ticker):
    # Allow hyphens in tickers
    if ' ' in ticker or ticker.isdigit() or not ticker.replace('-', '').isalnum():
        return ticker
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return info.get('longName', ticker)
    except Exception:
        return ticker

@app.callback(
    Output('asset-allocation', 'figure'),
    Input('update-allocation-button', 'n_clicks'),
    Input('add-asset-button', 'n_clicks'),
    Input('asset-label-1', 'value'),
    Input('asset-value-1', 'value'),
    Input('asset-label-2', 'value'),
    Input('asset-value-2', 'value'),
    Input('asset-label-3', 'value'),
    Input('asset-value-3', 'value'),
    Input('asset-label-4', 'value'),
    Input('asset-value-4', 'value'),
    Input('asset-label-5', 'value'),
    Input('asset-value-5', 'value'),
    Input('new-asset-label', 'value'),
    Input('new-asset-value', 'value'),
    Input('new-asset-type', 'value'),
    Input('new-asset-unit', 'value')
)
def update_allocation(update_clicks, add_clicks, label1, value1, label2, value2, label3, value3, label4, value4, label5, value5, new_label, new_value, new_type, new_unit):
    labels = [label1, label2, label3, label4, label5]
    values = [value1, value2, value3, value4, value5]
    parsed_labels = [parse_ticker_to_name(label) for label in labels]

    session.rollback()  # Rollback any previous transaction errors
    session.query(Asset).delete()  # Clear existing data
    session.commit()  # Commit the deletion before adding new data
    for label, value in zip(parsed_labels, values):
        asset = Asset(label=label, value=value)  # Ensure id is not set manually
        session.add(asset)
    session.commit()  # Commit after adding all new data

    # Add new asset if the add button is clicked
    if add_clicks > 0 and new_label and new_value is not None:
        new_asset = Asset(label=new_label, value=new_value)
        session.add(new_asset)
        session.commit()
        labels.append(new_label)
        values.append(new_value)
    
    # Update the pie chart with the new data
    return {
        'data': [
            go.Pie(
                labels=labels,
                values=values,
                hole=.3
            )
        ],
        'layout': {
            'title': 'Asset Allocation'
        }
    }

# Run the app
if __name__ == '__main__':
    app.run(debug=True) 