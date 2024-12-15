import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import yfinance as yf

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"])
app.title = "Stock Screener"

# Sample watchlist variable
watchlist = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

# Layout
app.layout = html.Div([
    html.H1("Stock Screener", style={"textAlign": "center"}),

    # Filters
    html.Div([
        html.Label("Price Range (Min - Max):"),
        dcc.RangeSlider(
            id='price-range',
            min=0, max=1000, step=10,
            marks={0: '0', 1000: '1000'},
            value=[0, 1000]
        ),
        html.Label("Minimum Volume:"),
        dcc.Input(id='min-volume', type='number', placeholder="e.g., 1000000", value=1000000),
    ], style={"marginBottom": "20px"}),

    # Submit button
    html.Button("Screen Stocks", id="screen-button", n_clicks=0, className="btn btn-primary"),

    # Data table
    html.Div(id='output-data', style={"marginTop": "20px"})
])

# Callbacks
@app.callback(
    Output('output-data', 'children'),
    [Input('screen-button', 'n_clicks')],
    [State('price-range', 'value'), State('min-volume', 'value')]
)
def update_output(n_clicks, price_range, min_volume):
    try:
        data = []

        # Fetch stock data using yfinance
        for ticker in watchlist:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                data.append({
                    "Ticker": ticker,
                    "Price": info.get('regularMarketPrice', None),
                    "Volume": info.get('regularMarketVolume', None),
                    "Market Cap": info.get('marketCap', None),
                    "P/E Ratio": info.get('trailingPE', None)
                })
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")

        stock_df = pd.DataFrame(data)

        # Filter data
        filtered_df = stock_df
        # filtered_df = stock_df[(stock_df['Price'] >= price_range[0]) &
        #                        (stock_df['Price'] <= price_range[1]) &
        #                        (stock_df['Volume'] >= min_volume)]

        # Display table
        return dash_table.DataTable(
            data=filtered_df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in filtered_df.columns],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
            page_size=10
        )

    except Exception as e:
        return html.Div(f"Error processing data: {e}", style={"color": "red"})

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
