import numpy as np
from scipy.stats import norm
import yfinance as yf


# Define the option base class, on which we will build the rest
# Define the option base class, on which we will build the rest
class Option:
    def __init__(self, S0, K, T, r, sigma, ticker=None):
        self.S0 = S0  # Initial stock price
        self.K = K    # Strike price
        self.T = T    # Time to maturity
        self.r = r    # Risk-free rate
        self.sigma = sigma  # Volatility
        self.ticker = ticker

        if ticker:
            try:
                self.fetch_data(ticker)
                self.calculate_volatility()
            except:
                print("Error fetching data for ticker:"+ticker)
            

    def fetch_data(self, ticker):
        stock_data = yf.download(ticker, period='1y')
        self.S0 = stock_data['Close'].iloc[-1]
        self.stock_data = stock_data['Close']

    def calculate_volatility(self):
        log_returns = np.log(self.stock_data / self.stock_data.shift(1)).dropna()
        self.sigma = np.std(log_returns) * np.sqrt(252)  # Annualize the volatility

    def d1(self):
        return (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))

    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.T)

    def N(self, x):
        return norm.cdf(x)

    def N_prime(self, x):
        return norm.pdf(x)

    def price(self):
        raise NotImplementedError("Subclasses should implement this method")

    def delta(self):
        raise NotImplementedError("Subclasses should implement this method")

    def gamma(self):
        return self.N_prime(self.d1()) / (self.S0 * self.sigma * np.sqrt(self.T))

    def theta(self):
        raise NotImplementedError("Subclasses should implement this method")

    def vega(self):
        return self.S0 * self.N_prime(self.d1()) * np.sqrt(self.T)

    def rho(self):
        raise NotImplementedError("Subclasses should implement this method")




