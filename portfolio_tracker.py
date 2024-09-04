import yfinance as yf
import pandas as pd
import os

class Portfolio:
    def __init__(self, file_name="portfolio.csv"):
        self.file_name = file_name
        self.stocks = self.load_portfolio()

    def load_portfolio(self):
        if os.path.exists(self.file_name):
            return pd.read_csv(self.file_name, index_col="Symbol").to_dict('index')
        else:
            return {}

    def save_portfolio(self):
        df = pd.DataFrame.from_dict(self.stocks, orient='index')
        df.index.name = 'Symbol'
        df.to_csv(self.file_name)

    def add_stock(self, symbol, shares):
        symbol = symbol.upper()
        if symbol in self.stocks:
            self.stocks[symbol]['Shares'] += shares
        else:
            stock_info = yf.Ticker(symbol).info
            self.stocks[symbol] = {
                'Shares': shares,
                'Company Name': stock_info['shortName']
            }
        self.save_portfolio()

    def remove_stock(self, symbol):
        symbol = symbol.upper()
        if symbol in self.stocks:
            del self.stocks[symbol]
            self.save_portfolio()
        else:
            print(f"Stock {symbol} not found in portfolio.")

    def get_portfolio_value(self):
        total_value = 0.0
        for symbol, data in self.stocks.items():
            price = yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1]
            total_value += data['Shares'] * price
        return total_value

    def display_portfolio(self):
        portfolio_data = []
        for symbol, data in self.stocks.items():
            price = yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1]
            value = data['Shares'] * price
            portfolio_data.append({
                "Symbol": symbol,
                "Company Name": data['Company Name'],
                "Shares": data['Shares'],
                "Current Price": price,
                "Value": value
            })

        df = pd.DataFrame(portfolio_data)
        print(df)
        print(f"\nTotal Portfolio Value: ${self.get_portfolio_value():.2f}")

def main():
    portfolio = Portfolio()

    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            portfolio.add_stock(symbol, shares)
        elif choice == '2':
            symbol = input("Enter stock symbol: ").upper()
            portfolio.remove_stock(symbol)
        elif choice == '3':
            portfolio.display_portfolio()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
