import plotly.graph_objects as go
from .option_definitions import VanillaOption, BarrierOption, AsianOption, AmericanOption
from .OptionPositionClass import OptionPosition
import numpy as np

# this is the class that will calculate the properties of the portfolio
class OptionPortfolio:
    def __init__(self, positions_dict=None):
        self.positions = []
        self.dictionary = []
        if positions_dict is not None and len(positions_dict)>0:
            for pos in positions_dict:
                self.add_position_dict(pos)

    def empty_portfolio(self):
        self.positions = []
        self.dictionary = []

        return "Emptied portfolio"


    def add_position_dict(self, position_dict):
        # Add the position to the dictionary
        self.dictionary.append(position_dict)

        # Extract the info from the position dictionary
        option_flavour = position_dict["option_flavour"]
        option_type = position_dict["option_type"]
        strike_price = float(position_dict["strike_price"])
        quantity = int(position_dict["quantity"])
        position = position_dict["position"]
        underlying_ticker = position_dict["underlying_ticker"]
        barrier = float(position_dict["barrier_level"]) if position_dict["barrier_level"] else None
        barrier_type = position_dict["barrier_type"]

    
        if option_flavour == "vanilla":
            option = VanillaOption(S0=None, K=strike_price, T=1, r=0.05, sigma=None, option_type=option_type, ticker=underlying_ticker)
            option_position = OptionPosition(option, position, quantity)
            self.add_position(option_position)
            print(f"Added {quantity} {option_flavour} to the portfolio, the underlying stock: {underlying_ticker} has price ${option.S0} and calculated volatility of {option.sigma}")
            return f"Added {quantity} {option_flavour} to the portfolio, the underlying stock: {underlying_ticker} has price ${option.S0} and calculated volatility of {option.sigma}"
        
        if option_flavour == "barrier":
            barrier_option = BarrierOption(S0=None, K=strike_price, T=1, r=0.05, sigma=None, H = barrier, barrier_type = barrier_type, option_type=option_type, ticker=underlying_ticker)
            option_position = OptionPosition(barrier_option, position, quantity)
            self.add_position(option_position)
            print(f"Added {quantity} {option_flavour} to the portfolio, the underlying stock: {underlying_ticker} has price ${option.S0} and calculated volatility of {option.sigma}")
            return f"Added {quantity} {option_flavour} to the portfolio, the underlying stock: {underlying_ticker} has price ${option.S0} and calculated volatility of {option.sigma}"


        if option_flavour == "asian":
            asian_option = AsianOption(S0 = None, K = strike_price, T=1, r=0.05, sigma=None, option_type=option_type, asian_type="geometric", ticker = underlying_ticker)
            option_position = OptionPosition(asian_option, position, quantity)
            self.add_position(option_position)
            print(f"Added {quantity} {option_flavour} to the portfolio, the underlying stock: {underlying_ticker} has price ${option.S0} and calculated volatility of {option.sigma}")
            return f"Added {quantity} {option_flavour} to the portfolio, the underlying stock: {underlying_ticker} has price ${option.S0} and calculated volatility of {option.sigma}"

        
        if option_flavour == "american":
            american_option = AmericanOption(S0 = None, K = strike_price, T=1, r=0.05, sigma=None, option_type=option_type, ticker = underlying_ticker)
            option_position = OptionPosition(american_option, position, quantity)
            self.add_position(option_position)
            print(f"Added {quantity} {option_flavour} to the portfolio, the underlying stock: {underlying_ticker} has price ${option.S0} and calculated volatility of {option.sigma}")
            return f"Added {quantity} {option_flavour} to the portfolio, the underlying stock: {underlying_ticker} has price ${option.S0} and calculated volatility of {option.sigma}"

    def add_position(self, position):
        self.positions.append(position)

    def remove_position(self, position):
        self.positions.remove(position)

    def total_value(self):
        return sum(position.value() for position in self.positions)

    def total_value_at(self, S):
        return sum(position.value_at(S) for position in self.positions)

    def total_delta(self):
        return sum(position.delta() for position in self.positions)

    def total_delta_at(self, S):
        return sum(position.delta_at(S) for position in self.positions)

    def total_gamma(self):
        return sum(position.gamma() for position in self.positions)

    def total_gamma_at(self, S):
        return sum(position.gamma_at(S) for position in self.positions)

    def total_theta(self):
        return sum(position.theta() for position in self.positions)

    def total_vega(self):
        return sum(position.vega() for position in self.positions)

    def total_rho(self):
        return sum(position.rho() for position in self.positions)

    
    def S_range(self):
        # Find the min and max S0 in the portfolio
        min_S0 = min(pos.option.S0 for pos in self.positions)
        max_S0 = max(pos.option.S0 for pos in self.positions)

        # Set a range around these values
        S_range = np.linspace(min_S0 * 0.1, max_S0 * 3, 50)

        return S_range

    def payoff(self, S):
        return sum(position.payoff(S) for position in self.positions)

    def plot_payoff(self, return_html = False):
        S_range = self.S_range()
        payoffs = [self.payoff(S) for S in S_range]

        layout = go.Layout(
            title='Dark Theme Example',
            paper_bgcolor='rgb(17,17,17)',  # Plot background color
            plot_bgcolor='rgb(17,17,17)',   # Inner plot background color
            font=dict(color='white'),       # Text color
            xaxis=dict(
                gridcolor='rgb(50, 50, 50)',  # Grid color
                zerolinecolor='rgb(50, 50, 50)',  # Zero line color
                color='white'  # Axis line and tick labels color
            ),
            yaxis=dict(
                gridcolor='rgb(50, 50, 50)',
                zerolinecolor='rgb(50, 50, 50)',
                color='white'
            )
        )

        fig = go.Figure(layout=layout)
        fig.add_trace(go.Scatter(x=S_range, y=payoffs, mode='lines', name='Portfolio Payoff'))
        fig.update_layout(
            title='Option Portfolio Payoff',
            xaxis_title='Underlying Asset Price at Expiration',
            yaxis_title='Payoff',
            legend=dict(x=0, y=1),
            hovermode="x unified"
        )

        if return_html:
            return fig.to_json()
        else:
          fig.show()


    def plot_value(self, return_html = False):
        S_range = self.S_range()
        portfolio_values = [self.total_value_at(S) for S in S_range]

        layout = go.Layout(
            title='Dark Theme Example',
            paper_bgcolor='rgb(17,17,17)',  # Plot background color
            plot_bgcolor='rgb(17,17,17)',   # Inner plot background color
            font=dict(color='white'),       # Text color
            xaxis=dict(
                gridcolor='rgb(50, 50, 50)',  # Grid color
                zerolinecolor='rgb(50, 50, 50)',  # Zero line color
                color='white'  # Axis line and tick labels color
            ),
            yaxis=dict(
                gridcolor='rgb(50, 50, 50)',
                zerolinecolor='rgb(50, 50, 50)',
                color='white'
            )
        )

        fig = go.Figure(layout=layout)
        fig.add_trace(go.Scatter(x=S_range, y=portfolio_values, mode='lines', name='Portfolio Value'))
        fig.update_layout(
            title='Option Portfolio Value Now',
            xaxis_title='Underlying Asset Price at Expiration',
            yaxis_title='Value',
            legend=dict(x=0, y=1),
            hovermode="x unified"
        )

        if return_html:
            return fig.to_json()
        else:
          fig.show()


    def plot_delta(self, return_html = False):
        S_range = self.S_range()
        portfolio_delta = [self.total_delta_at(S) for S in S_range]

        layout = go.Layout(
            title='Dark Theme Example',
            paper_bgcolor='rgb(17,17,17)',  # Plot background color
            plot_bgcolor='rgb(17,17,17)',   # Inner plot background color
            font=dict(color='white'),       # Text color
            xaxis=dict(
                gridcolor='rgb(50, 50, 50)',  # Grid color
                zerolinecolor='rgb(50, 50, 50)',  # Zero line color
                color='white'  # Axis line and tick labels color
            ),
            yaxis=dict(
                gridcolor='rgb(50, 50, 50)',
                zerolinecolor='rgb(50, 50, 50)',
                color='white'
            )
        )

        fig = go.Figure(layout=layout)
        fig.add_trace(go.Scatter(x=S_range, y=portfolio_delta, mode='lines', name='Portfolio Delta', line=dict(color="green")))
        fig.update_layout(
            title='Option Portfolio Delta Over Underlying S',
            xaxis_title='Underlying Asset Price at Expiration',
            yaxis_title='Delta',
            legend=dict(x=0, y=1),
            hovermode="x unified"
        )

        if return_html:
            return fig.to_json()
        else:
          fig.show()

    def plot_gamma(self, return_html = False):
        S_range = self.S_range()
        portfolio_gamma = [self.total_gamma_at(S) for S in S_range]

        layout = go.Layout(
            title='Dark Theme Example',
            paper_bgcolor='rgb(17,17,17)',  # Plot background color
            plot_bgcolor='rgb(17,17,17)',   # Inner plot background color
            font=dict(color='white'),       # Text color
            xaxis=dict(
                gridcolor='rgb(50, 50, 50)',  # Grid color
                zerolinecolor='rgb(50, 50, 50)',  # Zero line color
                color='white'  # Axis line and tick labels color
            ),
            yaxis=dict(
                gridcolor='rgb(50, 50, 50)',
                zerolinecolor='rgb(50, 50, 50)',
                color='white'
            )
        )

        fig = go.Figure(layout=layout)
        fig.add_trace(go.Scatter(x=S_range, y=portfolio_gamma, mode='lines', name='Portfolio Gamma', line=dict(color="red")))
        fig.update_layout(
            title='Option Portfolio Gamma Over Underlying S',
            xaxis_title='Underlying Asset Price at Expiration',
            yaxis_title='Gamma',
            legend=dict(x=0, y=1),
            hovermode="x unified"
        )

        if return_html:
            return fig.to_json()
        else:
          fig.show()

    



    def describe_portfolio(self):
        descriptions = []
        for position in self.positions:
            option = position.option
            position_type = "Long" if position.position == "long" else "Short"
            description = f"{position.quantity} {position_type} {option.option_type.capitalize()} Option(s) on stock with "
            if option.ticker:
                description += f"ticker {option.ticker} (price and volatility fetched from yfinance)."
            else:
                description += f"initial price ${option.S0}, strike price {option.K}, maturity {option.T} years, risk-free rate {option.r}, and volatility {option.sigma}."
            descriptions.append(description)
        return "\n".join(descriptions)