# stockDash

Dashboard for stock portfolio

# Tools
- python
- yfinance lib
- dash framework

# Types
- Current Holdings
    - Stocks: US Stock, Korea Stock
    - Bonds: US Treasury
    - Cash: USD, KRW
- Annual Realized Profits
    - USD, KRW

# User Interface
- User can do input Tickers for Stocks, Amount for all, Select Unit (USD, KRW).
- Dashboard show the pie graph with possession of assets.
- Dashboard show the graph with annual profit.

## Recent Updates

- **Dynamic Asset Addition**: Users can now add new assets dynamically through the app interface. This feature allows users to input new asset details such as label, value, type, and unit, and see them reflected in the asset allocation chart.

- **.gitignore File**: A `.gitignore` file has been added to exclude unnecessary files from the repository. This includes Python cache files, virtual environments, and the `assets.db` database file.

## Running the Application

To run the application, use the following command:

```bash
python app.py
```

Ensure that you have all the necessary dependencies installed and that your environment is set up correctly.

## Troubleshooting

- If you encounter warnings related to leaked semaphore objects, these are typically benign and can be ignored. The application includes a warning filter to suppress these messages.

- If new assets are not appearing in the asset allocation chart, ensure that all input fields are correctly filled and that the "Add Asset" button is clicked to update the chart.