from asset import Asset


class Portfolio:
    def __init__(self):
        self.equity = 0
        self.assets = {}

    def deposit(self, amount):
        self.equity += amount

    def withdraw(self, amount):
        self.equity -= amount

    def add_asset(self, asset):
        if asset.name not in self.assets:
            self.assets[asset.name] = asset

    def get_asset(self, name):
        return self.assets[name]

    def get_assets(self):
        return self.assets.values()

    def get_equity(self):
        return self.equity

    def get_portfolio_value(self):
        total = 0
        for ticker, asset in self.assets.items():
            total += asset.value

        return total

    def __str__(self):
        return f"Assets: {len(self.assets)}\n" \
               f"Total value: {self.get_portfolio_value()}\n" \
               f"Cash: {self.equity}"
