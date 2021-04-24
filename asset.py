class Asset:
    def __init__(self, name):
        self.name = name
        self.amount = 0
        self.value = 0

    def buy(self, amount, price):
        self.amount += amount
        self.value += price * amount

    def sell(self, amount, price):
        self.amount -= amount
        self.value -= price * amount

    def __str__(self):
        return f"Ticker: {self.name}\n" \
               f"Amount: {self.amount}\n" \
               f"Value:  {self.value}\n"
