# Define the option position class, which stores the number of options and long-short positions
class OptionPosition:
    def __init__(self, option, position="long", quantity=1):
        self.option = option
        self.position = position
        self.quantity = quantity

    def value(self):
        multiplier = 1 if self.position == "long" else -1
        return multiplier * self.quantity * self.option.price()

    def value_at(self, S):
        # Temporarily change the stock price to compute the value
        original_price = self.option.S0
        self.option.S0 = S
        value = self.value()
        self.option.S0 = original_price  # Reset the stock price
        return value

    def delta(self):
        multiplier = 1 if self.position == "long" else -1
        return multiplier * self.quantity * self.option.delta()


    def delta_at(self, S):
        original_price = self.option.S0
        self.option.S0 = S
        delta = self.delta()
        self.option.S0 = original_price  # Reset the stock price
        return delta

    def gamma(self):
        multiplier = 1 if self.position == "long" else -1
        return multiplier * self.quantity * self.option.gamma()

    def gamma_at(self, S):
        original_price = self.option.S0
        self.option.S0 = S
        gamma = self.gamma()
        self.option.S0 = original_price  # Reset the stock price
        return gamma

    def theta(self):
        multiplier = 1 if self.position == "long" else -1
        return multiplier * self.quantity * self.option.theta()

    def vega(self):
        multiplier = 1 if self.position == "long" else -1
        return multiplier * self.quantity * self.option.vega()

    def rho(self):
        multiplier = 1 if self.position == "long" else -1
        return multiplier * self.quantity * self.option.rho()

    def payoff(self, S):
        multiplier = 1 if self.position == "long" else -1
        return multiplier * self.quantity * self.option.payoff(S)

    
